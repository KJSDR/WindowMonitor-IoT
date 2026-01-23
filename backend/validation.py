"""
Sensor data validation and quality checking

(cheap sensors = readings aren't the best)
"""

#recent readings buffer for stuck sensor detection
recent_values = {
    'temp': [],
    'humidity': [],
    'air_quality': []
}

MAX_HISTORY = 10 #tracks last 10 readings

def validate_reading(temp, humidity, air_quality):
    """
    Validate sensor reading and return the status
    Returns:
        dict with 'valid', 'issues', and 'health' keys
    """
    issues = []

    #check for out-of-range values
    if not (0 <= temp <= 150):
        issues.append(f"Temperature out of range: {temp}°F")

    if not (0 <= humidity <= 100):
        issues.append(f"Humidity out of range: {humidity}%")

    if not (0 <= air_quality <= 4095):
        issues.append(f"Air Quality out of range: {air_quality}")

    #updates the hisotry
    recent_values['temp'].append(temp)
    recent_values['humidity'].append(humidity)
    recent_values['air_quality'].append(air_quality)

    #keeps only last MAX_HISTORY readings
    if len(recent_values['temp']) > MAX_HISTORY:
        recent_values['temp'].pop(0)
        recent_values['humidity'].pop(0)
        recent_values['air_quality'].pop(0)

    #check for stuck sensors (given enough history)
    if len(recent_values['temp']) >= MAX_HISTORY:
        if len(set(recent_values['temp'])) == 1:
            issues.append("Temperature sensor stuck (no variation)")

        if len(set(recent_values['humidity'])) == 1:
            issues.append("Humidity sensor stuck (no variation)")

        if len(set(recent_values['air_quality'])) == 1:
            issues.append("Air quality sensor stuck (no variation)")

    #determine overall health status
    if len(issues) == 0:
        health = "good"
    elif len(issues) <= 2:
        health = "degraded"
    else:
        health = "failed"

    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'health': health
    }

def get_sensor_health():
    """Return current sensor health summary"""
    if len(recent_values['temp']) < 3:
        return {
            'status': 'initializing',
            'message': 'Collection baseline data...'
        }

    #checks for recent variations
    temp_variation = max(recent_values['temp']) - min(recent_values['temp'])
    humidity_variation = max(recent_values['humidity']) - min(recent_values['humidity'])

    if temp_variation < 0.1 and humidity_variation < 0.1:
        return {
            'status': 'warning',
            'message': 'Sensors may be stuck - no variation detected'
        }
    return {
        'status': 'healthy',
        'message': 'All sensors responding normally'
    }

        