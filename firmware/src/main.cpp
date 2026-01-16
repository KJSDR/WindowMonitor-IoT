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
  // read every 3s
  if (millis() - lastReading < 3000) {
    return;
  }
  lastReading = millis();
  
  // read sensors
  float temp = readTemperature();
  float humidity = readHumidity();
  int airQuality = readAirQuality();
  
  // check their validity
  if (isnan(temp) || isnan(humidity)) {
    Serial.println("{\"error\":\"Sensor read failed\"}");
    return;
  }
  
  // outputs in JSON format
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