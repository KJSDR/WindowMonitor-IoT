import sqlite3
from datetime import datetime
import os

#db path relative to file location
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'readings.db')

def init_db():
    """Create database and table if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    #creats the readings table and data fields for sensors
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            air_quality INTEGER NOT NULL,
            is_valid INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    #indexs on timestamp for faster query when it is filter by time
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_timestamp
        ON readings(timestamp)    
    ''')

    #add is_valid column in DB if it doesn't exist
    try:
        cursor.execute('ALTER TABLE readings ADD COLUMN is_valid INTEGER DEFAULT 1')
        print("Added is_valid column to existing database")
    except sqlite3.OperationalError:
        #it already exist from new CREATE TABLE or prev migration
        pass

    conn.commit()
    conn.close()
    print("Database initialized")

def insert_reading(data):
    '''Insert sensor reading into database'''
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #get validation status
    validate = data.get('validation', {})
    is_valid = validation.get('valid', True)

    #inserts new reading by using server_time if it is there, otherise it is current time
    cursor.execute('''
        INSERT INTO readings (timestamp, temperature, humidity, air_quality, is_valid)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data.get('server_time', datetime.now().isoformat()),
        data.get('temp'),
        data.get('humidity'),
        data.get('air_quality')
        is_valid
    ))

    conn.commit()
    conn.close()

def get_recent_readings(limit=100):
    """Get most recent readings"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    #fetches latest readings and is ordered by insert time
    cursor.execute('''
        SELECT timestamp, temperature, humidity, air_quality, is_valid
        FROM readings
        ORDER BY created_at DESC
        LIMIT ?
    ''', (limit,))

    rows = cursor.fetchall()
    conn.close()
    
    #converts rows to a dictionary format for easy access
    return [
        {
            'timestamp': row[0],
            'temperature': row[1],
            'humidity': row[2],
            'air_quality': row[3],
            'is_valid': bool(row[4]) if len(row) > 4 else True
        }
        for row in rows
    ]
#init database on module import
init_db()