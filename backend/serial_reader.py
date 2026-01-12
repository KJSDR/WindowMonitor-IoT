import serial
import json
import time
from datetime import datetime
from database import insert_reading

# Find your serial port
SERIAL_PORT = '/dev/cu.usbserial-0001'  # Change this to your port
BAUD_RATE = 115200

def read_serial():
    """Continuously read from ESP32 serial port"""
    print(f"Connecting to {SERIAL_PORT}...")
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("✓ Connected! Reading data...\n")
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                
                # Try to parse JSON
                try:
                    data = json.loads(line)
                    
                    # Add server timestamp
                    data['server_time'] = datetime.now().isoformat()
                    
                    # Print to console
                    print(f"📊 Temp: {data.get('temp')}°F | "
                          f"Humidity: {data.get('humidity')}% | "
                          f"AQ: {data.get('air_quality')}")
                    
                    # Store in database
                    insert_reading(data)
                    
                except json.JSONDecodeError:
                    # Not JSON, just print it
                    print(f"ℹ️  {line}")
            
            time.sleep(0.1)
    
    except serial.SerialException as e:
        print(f"❌ Error: {e}")
        print("\nAvailable ports:")
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        for port in ports:
            print(f"  - {port.device}")
    
    except KeyboardInterrupt:
        print("\n\n👋 Stopped by user")
        ser.close()

if __name__ == "__main__":
    read_serial()