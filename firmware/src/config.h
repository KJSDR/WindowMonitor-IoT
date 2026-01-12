#ifndef CONFIG_H
#define CONFIG_H

// Pin Definitions
#define DHTPIN 15          // DHT22 data pin
#define MQ135_PIN 34       // MQ-135 analog pin (use A2 on Feather)
#define LED_RED 13         // Red LED pin
#define LED_GREEN 12       // Green LED pin

// LCD I2C Address (will add later)
#define LCD_ADDRESS 0x27
#define LCD_COLS 16
#define LCD_ROWS 2

// Sensor Type
#define DHTTYPE DHT22

// Environmental Thresholds
#define TEMP_MIN 60.0      // Minimum comfortable temperature (°F)
#define TEMP_MAX 78.0      // Maximum comfortable temperature (°F)
#define HUMIDITY_MAX 70.0  // Maximum acceptable humidity (%)
#define AIR_QUALITY_MIN 500 // Minimum acceptable air quality

// Serial Configuration
#define SERIAL_BAUD 115200

// Update Interval
#define UPDATE_INTERVAL 3000  // milliseconds between readings

#endif