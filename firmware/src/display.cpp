#include <Arduino.h>
#include "display.h"
#include "config.h"

void initDisplay() {
  // Initialize LEDs
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  
  // Turn off both LEDs initially
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_GREEN, LOW);
  
  Serial.println("✓ Display initialized");
}

void printHeader() {
  Serial.println("\n╔═══════════════════════════════════════╗");
  Serial.println("║  SMART WINDOW MONITORING SYSTEM v1.0  ║");
  Serial.println("║     Multi-Sensor Environmental Demo   ║");
  Serial.println("╚═══════════════════════════════════════╝\n");
}

void printReadings(float temp, float humidity, int airQuality) {
  Serial.println("══════════════ READINGS ══════════════");
  
  Serial.print("Temperature: ");
  Serial.print(temp, 1);
  Serial.println("°F");
  
  Serial.print("Humidity:    ");
  Serial.print(humidity, 1);
  Serial.println("%");
  
  Serial.print("Air Quality: ");
  Serial.println(airQuality);
  
  Serial.println("═════════════════════════════════════\n");
}

void updateLEDs(bool alert) {
  if (alert) {
    digitalWrite(LED_RED, HIGH);
    digitalWrite(LED_GREEN, LOW);
  } else {
    digitalWrite(LED_RED, LOW);
    digitalWrite(LED_GREEN, HIGH);
  }
}