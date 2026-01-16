#include <Arduino.h>
#include "DHT.h"
#include "sensors.h"
#include "config.h"

// create DHT sensor object
DHT dht(DHTPIN, DHTTYPE);

void initSensors() {
  // init DHT22
  pinMode(DHTPIN, INPUT_PULLUP);
  dht.begin();
  
  // init MQ-135
  pinMode(MQ135_PIN, INPUT);
  
  Serial.println("✓ Sensors initialized");
}

float readTemperature() {
  return dht.readTemperature(true); // true = Fahrenheit
}

float readHumidity() {
  return dht.readHumidity();
}

int readAirQuality() {
  return analogRead(MQ135_PIN);
}

bool isSensorDataValid(float temp, float humidity) {
  return !isnan(temp) && !isnan(humidity);
}