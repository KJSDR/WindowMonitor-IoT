from flask import Flask, jsonify, request
from flask_cors import CORS
import serial
import json
import threading
import time
from database import insert_reading, get_recent_readings

"""
Environmental monitoring REST API

Reads realtime sensor data from DHT22 and MQ135 connected to a ESP3 via serial connection and 
makes JSON endpoints for it to connect to a dashboard.
"""

app = Flask(__name__)
CORS(app) # Enable CORS for the react frontend (allows requests from one domain to another)

# tores most recent sensor reading in the memory
latest_reading = {
    "temp": 0,
    "humidity": 0,
    "air_quality": 0,
    "timestamp": 0
}

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
                    latest_reading = data
                    print(f"Updated: Temp={data['temp']}°F, Humidity={data['humidity']}%, AQ={data['air_quality']}")
                    insert_reading(data) #stores reading in db
                except json.JSONDecodeError:
                    pass

            time.sleep(0.1)

    except Exception as e:
        print(f"Serial error: {e}")
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
    #validate sensor reading to make sure they are within reasonable range
    if not (0 <= latest_reading.get('temp', 0) <= 150):
        latest_reading['temp'] = 0
    if not (0 <= latest_reading.get('humidity', 0) <= 100):
        latest_reading['humidity'] = 0

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

    #defines the environmental thesholds (can change to whatever)
    TEMP_MIN = 60
    TEMP_MAX = 78
    HUMIDITY_MAX = 70
    AQ_MIN = 500

    reasons = []

    #checks each condition and collects reasons for the alerts
    if air_quality < AQ_MIN:
        reasons.append("Poor air quality")
    if temp > TEMP_MAX:
        reasons.append("Temperature too high")
    if temp < TEMP_MIN:
        reasons.append("Temperature too low")
    if humidity > HUMIDITY_MAX:
        reasons.append("Humidity too high")

    #returns the recommendation based on if any alerts came up
    if reasons:
        return {
            "recommendation": "CLOSE",
            "reason": ", ".join(reasons)
        }
    else:
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

    #extract values
    temps = [r['temperature'] for r in readings]
    humidities = [r['humidity'] for r in readings]
    aqs = [r['air_quality'] for r in readings]

    #calc stats
    stats = {
        'count': len(readings),
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

if __name__ == '__main__':

    #starts serial readings in background thread, daemon True makes it exit with main program?
    serial_thread = threading.Thread(target=read_serial_continuously, daemon=True)
    serial_thread.start()

    print("Starting API server on http://localhost:5001") #5001 because mac often uses 5000 for other stuff and breaks
    app.run(debug=True, port=5001)