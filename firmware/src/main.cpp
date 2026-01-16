#include <Arduino.h>
#include "config.h"
#include "sensors.h"

/*
*envionmental monitoring firmware
*reads DHT22 abd MQ135 sensors
*outputs JSON via serial every 3s
*/

unsigned long lastReading = 0;

void setup() {
  Serial.begin(115200);
  delay(2000);
  
  initSensors();
  
  Serial.println("{\"status\":\"System initialized\"}");
}

void loop() {
  // Read every 3 seconds
  if (millis() - lastReading < 3000) {
    return;
  }
  lastReading = millis();
  
  // Read sensors
  float temp = readTemperature();
  float humidity = readHumidity();
  int airQuality = readAirQuality();
  
  // Check validity
  if (isnan(temp) || isnan(humidity)) {
    Serial.println("{\"error\":\"Sensor read failed\"}");
    return;
  }
  
  // Output JSON
  Serial.print("{");
  Serial.print("\"temp\":");
  Serial.print(temp, 1);
  Serial.print(",\"humidity\":");
  Serial.print(humidity, 1);
  Serial.print(",\"air_quality\":");
  Serial.print(airQuality);
  Serial.print(",\"timestamp\":");
  Serial.print(millis());
  Serial.println("}");
}