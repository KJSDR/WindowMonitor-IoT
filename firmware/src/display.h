#ifndef DISPLAY_H
#define DISPLAY_H

// Initialize display outputs (LEDs, Serial, LCD later)
void initDisplay();

// Print sensor readings to serial
void printReadings(float temp, float humidity, int airQuality);

// Update LED status
void updateLEDs(bool alert);

// Print system header
void printHeader();

#endif