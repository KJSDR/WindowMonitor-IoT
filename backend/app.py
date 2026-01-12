from flask import Flask

app = Flask(__name__)



latest_reading = {
    "temp": 0,
    "humidity": 0,
    "air_quality": 0,
    "timespamp": 0
}

SERIAL_PORT = '/dev/cu.usbserial-XXXX'