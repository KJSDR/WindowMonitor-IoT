#ifndef SENSORS_H
#define SENSORS_H

// init all sensors
void initSensors();

// DHT22 functions
float readTemperature();
float readHumidity();

// MQ-135 function
int readAirQuality();

// check if readings are valid
bool isSensorDataValid(float temp, float humidity);

#endif