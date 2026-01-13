from flask import Flask
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
    "timespamp": 0
}

SERIAL_PORT = '/dev/cu.usbserial-XXXX' #dont forget o update this to correct name
BAUD_RATE = 115200

def read_serial_continuously():
    """placeholder"""
    global latest_reading

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}")

        while True:
            if ser.in_Waiting > 0:
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

@app.route('/api/health')