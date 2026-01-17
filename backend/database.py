import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'readings.db')

def init_db():
    """Create database and table if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            air_quality INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_timestamp
        ON readings(timestamp)    
    ''')

    conn.commit()
    conn.close()
    print("Database initialized")

def insert_reading(data):
    '''Insert sensor reading into database'''
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO readings (timestamp, temperature, humidity, air_quality)
        VALUES (?, ?, ?, ?)
    ''', (
        data.get('server_time', datetime.now().isoformat()),
        data.get('temp'),
        data.get('humidity'),
        data.get('air_quality')
    ))

    conn.commit()
    conn.close()

def get_recent_readings(limit=100):
    """Get most recent readings"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT timestamp, temperature, humidity, air_quality
        FROM readings
        ORDER BY created_at DESC
        LIMIT ?
    ''', (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            'timestamp': row[0],
            'temperature': row[1],
            'humidity': row[2],
            'air_quality': row[3]
        }
        for row in rows
    ]

init_db()