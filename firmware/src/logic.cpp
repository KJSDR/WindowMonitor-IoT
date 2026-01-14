#include <Arduino.h>
#include "logic.h"
#include "config.h"

bool shouldCloseWindow(float temp, float humidity, int airQuality) {
  bool tempAlert = (temp > TEMP_MAX || temp < TEMP_MIN);
  bool humidityAlert = (humidity > HUMIDITY_MAX);
  bool airAlert = (airQuality < AIR_QUALITY_MIN);
  
  return (tempAlert || humidityAlert || airAlert);
}

void printRecommendation(bool alert) {
  Serial.print("RECOMMENDATION: ");
  
  if (alert) {
    Serial.println("CLOSE WINDOW");
    Serial.println("   Environmental conditions not optimal\n");
  } else {
    Serial.println("WINDOW CAN STAY OPEN");
    Serial.println("   All conditions acceptable\n");
  }
}