#ifndef CONFIG_H
#define CONFIG_H

// pin definitions
#define DHTPIN 15
#define MQ135_PIN 34
#define LED_RED 13
#define LED_GREEN 12

// LCD I2C
#define LCD_ADDRESS 0x27
#define LCD_COLS 16
#define LCD_ROWS 2

// sensor type
#define DHTTYPE DHT22

// environment thresholds
#define TEMP_MIN 60.0
#define TEMP_MAX 78.0
#define HUMIDITY_MAX 70.0
#define AIR_QUALITY_MIN 500

// serial config
#define SERIAL_BAUD 115200

// update interval 3s
#define UPDATE_INTERVAL 3000

#endif