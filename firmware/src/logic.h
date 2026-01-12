#ifndef LOGIC_H
#define LOGIC_H

// Analyze sensor data and determine if alert is needed
bool shouldCloseWindow(float temp, float humidity, int airQuality);

// Print recommendation based on analysis
void printRecommendation(bool alert);

#endif