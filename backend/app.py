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

SERIAL_PORT = '/dev/cu.usbserial-XXXX'
BAUD_RATE = 115200

def read_serial_continuously():
    """placeholder"""
    global latest_reading