from flask import Flask, jsonify
from flask_cors import CORS
import serial
import json
import threading
import time

app = Flask(__name__)
CORS(app)


latest_reading = {
    "temp": 0,
    "humidity": 0,
    "air_quality": 0,
    "timestamp": 0
}

SERIAL_PORT = '/dev/cu.usbserial-022AF20E' #update to corredct name
BAUD_RATE = 115200

def read_serial_continuously():
    """Background thread that reads serial data"""
    global latest_reading

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}")

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()

                try:
                    data = json.loads(line)
                    latest_reading = data
                    print(f"Updated: Temp={data['temp']}°F, Humidity={data['humidity']}%, AQ={data['air_quality']}")
                except json.JSONDecodeError:
                    pass

            time.sleep(0.1)

    except Exception as e:
        print(f"Serial error: {e}")



@app.route('/api/latest')
def get_latest():
    """Return the most recent sensor reading"""
    
    recommendation = calculate_recommendation(
        latest_reading.get('temp', 0),
        latest_reading.get('humidity', 0),
        latest_reading.get('air_quality', 0)
    )
    
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

    TEMP_MIN = 60
    TEMP_MAX = 78
    HUMIDITY_MAX = 70
    AQ_MIN = 500

    reasons = []

    if air_quality < AQ_MIN:
        reasons.append("Poor air quality")
    if temp > TEMP_MAX:
        reasons.append("Temperature too high")
    if temp < TEMP_MIN:
        reasons.append("Temperature too low")
    if humidity > HUMIDITY_MAX:
        reasons.append("Humidity too high")

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

if __name__ == '__main__':

    serial_thread = threading.Thread(target=read_serial_continuously, daemon=True)
    serial_thread.start()

    print("Starting API server on http://localhost:5001")
    app.run(debug=True, port=5001)