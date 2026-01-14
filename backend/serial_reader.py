import serial
import json
import time
from datetime import datatime
from database import insert_reading

SERIAL_PORT = 'dev/cu.usbserial-XXXX' #get my right port number
BAUD_RATE = 115200

def read_serial():
    """Reads from ESP32 serial port continuously"""
    print(f"Connecting to {SERIAL_PORT}...")

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("Connected. Reading data...\n")

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8'),strip()

                try:
                    data = json.loads(line)

                    data['server_time'] = datetime.now().isoformat()

                    print(f"Temp: {data.get('temp')}°F | "
                          f"Humidity: {data.get('humidity')}% | "
                          f"AQ: {data.get('air_quality')}")

                    instert_reading(data)

                except json.JSONDecodeError:
                    print(f"{line}")

            time.sleep(0.1)








if __name__ == "__main__":
    read_serial()