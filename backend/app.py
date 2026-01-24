from flask import Flask, jsonify, request
from flask_cors import CORS
import serial
import json
import threading
import time
from database import insert_reading, get_recent_readings
from validation import validate_reading, get_sensor_health

"""
Environmental monitoring REST API

Reads realtime sensor data from DHT22 and MQ135 connected to a ESP3 via serial connection and 
makes JSON endpoints for it to connect to a dashboard.
"""

app = Flask(__name__)
CORS(app) # Enable CORS for the react frontend (allows requests from one domain to another)

#stores most recent sensor reading in the memory
latest_reading = {
    "temp": 0,
    "humidity": 0,
    "air_quality": 0,
    "timestamp": 0
}
#track current recs state for hysteresis
current_state = "UNKNOWN" #OPEN / CLOSE / UNKNOWN

#serial port config
SERIAL_PORT = '/dev/cu.usbserial-022AF20E' #update to whatever local port is
BAUD_RATE = 115200 #how fast the data is transmitted, this is a standard number (115200 bits per sec)

def read_serial_continuously():
    """Background thread that reads serial data"""
    global latest_reading

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}")

        while True:
            #checks if data is available from serial port
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()

                try:
                    #parses the json from esp32
                    data = json.loads(line)
                    #validate readings
                    validation = validate_reading(
                        data['temp'],
                        data['humidity'],
                        data['air_quality']
                    )
                    #add variation info to data
                    data['validation'] = validation

                    latest_reading = data

                    #log readings with validation status
                    if validation['valid']:
                        print(f"Updated: Temp={data['temp']}°F, Humidity={data['humidity']}%, AQ={data['air_quality']}")
                    else:
                        print(f"Warning: {', '.join(validation['issues'])}")
                    #still store in database (even if invalid still want for analysis)
                    insert_reading(data)

                except json.JSONDecodeError:
                    pass

            time.sleep(0.1)

    except Exception as e:
        print(f"Serial error: {e}")
        import traceback
        traceback.print_exc() #show full error
        print("Attempting to reconnect in 5 seconds...")
        time.sleep(5)
        #retries connection
        read_serial_continuously()



@app.route('/api/latest')
def get_latest():
    """Return the most recent sensor reading"""
    
    #calculate recommendation based on the current readings
    recommendation = calculate_recommendation(
        latest_reading.get('temp', 0),
        latest_reading.get('humidity', 0),
        latest_reading.get('air_quality', 0)
    )
    #merges sensor data with recommendations
    return jsonify({
        **latest_reading,
        **recommendation
    })


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

def calculate_recommendation(temp, humidity, air_quality):
    """Simple decision logic"""
    global current_state

    #defines the environmental thesholds (can change to whatever)
    TEMP_MIN = 60
    TEMP_MAX = 78
    HUMIDITY_MAX = 70
    AQ_MIN = 500

    #hysterisis windows (stability buffers)
    TEMP_WINDOW = 2 # +- 2 degrees F
    HUMIDITY_WINDOW = 5 # +- 5%
    AQ_WINDOW = 50 # +- 50 units

    #calc if conditions favor OPEN or CLOSE
    reasons_close = []
    reasons_open = []

    #check each condition with hysterisis
    if current_state == "CLOSE":
        #current closed - need good conditions to open
        if air_quality < AQ_MIN - AQ_WINDOW:
            reasons_close.append("Poor air quality")
        if temp > TEMP_MAX + TEMP_WINDOW:
            reasons_close.append("Temperature too high")
        if temp < TEMP_MIN - TEMP_WINDOW:
            reasons_close.append("Temperature too low")
        if humidity > HUMIDITY_MAX + HUMIDITY_WINDOW:
            reasons_close.append("Humidity too high")
    elif current_state == "OPEN":
        #current open - need clearly bad conditions to close
        if air_quality < AQ_MIN + AQ_WINDOW:
            reasons_close.append("Poor air quality")
        if temp > TEMP_MAX - TEMP_WINDOW:
            reasons_close.append("Temperature too high")
        if temp < TEMP_MIN + TEMP_WINDOW:
            reasons_close.append("Temperature too low")
        if humidity > HUMIDITY_MAX - HUMIDITY_WINDOW:
            reasons_close.append("Humidity too high")
    else:
        #unknown state (first run) - use standard thesholds
        if air_quality < AQ_MIN:
            reasons_close.append("Poor air quality")
        if temp > TEMP_MAX:
            reasons_close.append("Temperature too high")
        if temp < TEMP_MIN:
            reasons_close.append("Temperature too low")
        if humidity > HUMIDITY_MAX:
            reasons_close.append("Humidity too high")

    #makes decisions and gives reason
    if reasons_close:
        current_state = "CLOSE"
        return {
            "recommendation": "CLOSE",
            "reason": ", ".join(reasons_close)
        }
    else:
        current_state = "OPEN"
        return {
            "recommendation": "OPEN",
            "reason": "All conditions favorable"
        }

@app.route('/api/readings')
def get_readings():
    """Return history sensor readings from the database"""
    #gets limit from query parameter, defaults 100 and max 1000

    limit = request.args.get('limit', default=100, type=int)
    limit = min(limit, 1000) #caps at 1000 to prevent giant responses

    readings = get_recent_readings(limit)

    return jsonify({
        'count': len(readings),
        'readings': readings
    })

@app.route('/api/stats')
def get_stats():
    """Return stats summary of sensor data"""

    #get limit from query paramter (lastt 100 readings)
    limit = request.args.get('limit', default=100, type=int)
    limit = min(limit, 1000)

    readings = get_recent_readings(limit)

    if not readings:
        return jsonify({
            'error': 'No data available'
        })

    #filters out invalid readings for better calculated averages
    valid_readings = [r for r in readings if r.get('is_valid', True)]

    if not valid_readings:
        return jsonify({'error': 'No valid data available'})

    #extract values
    temps = [r['temperature'] for r in valid_readings]
    humidities = [r['humidity'] for r in valid_readings]
    aqs = [r['air_quality'] for r in valid_readings]

    #calc stats
    stats = {
        'count': len(valid_readings),
        'temperature': {
            'min': min(temps),
            'max': max(temps),
            'avg': sum(temps) / len(temps)
        },
        'humidity': {
            'min': min(humidities),
            'max': max(humidities),
            'avg': sum(humidities) / len(humidities)
        },
        'air_quality': {
            'min': min(aqs),
            'max': max(aqs),
            'avg': sum(aqs) / len(aqs)
        },
        'time_range': {
            'start': readings[-1]['timestamp'],
            'end': readings[0]['timestamp']
        },
    }

    return jsonify(stats)

@app.route('/api/sensor-health')
def sensor_health():
    """Return current sensor health status"""
    health = get_sensor_health()

    return jsonify(health)

@app.route('/api/export')
def export_data():
    """Export sensor data as CSV"""
    import csv
    from io import StringIO

    #get limit from query parameter
    limit = request.args.get('limit', default=100, type=int)
    limit = min(limit, 10000) #caps at 10k rows

    #get readings
    readings = get_recent_readings(limit)

    if not readings:
        return jsonify({'error': 'No data available'}), 404

    #create CSV in memory
    output = StringIO()
    writer = csv.writer(output)

    #write header
    writer.writerow(['Timestamp', 'Temperature (°F)', 'Humidity (%)', 'Air Quality', 'Valid'])

    #write data rows (reverse oldest first)
    for reading in reversed(readings):
        writer.writerow([
            reading['timestamp'],
            f"{reading['temperature']:.1f}",
            f"{reading['humidity']:.1f}",
            reading['air_quality'],
            'Yes' if reading.get('is_valid', True) else 'No'
        ])

    #prepare response
    output.seek(0)

    from flask import make_response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=sensor_data.csv'

    return response


if __name__ == '__main__':

    #starts serial readings in background thread, daemon True makes it exit with main program?
    serial_thread = threading.Thread(target=read_serial_continuously, daemon=True)
    serial_thread.start()

    print("Starting API server on http://localhost:5001") #5001 because mac often uses 5000 for other stuff and breaks
    app.run(debug=True, port=5001)