# MK.1 – Environmental Monitoring & Decision System

## Overview
Monitors temperature, humidity, and air quality to recommend when to open or close your window. Built to explore full-stack IoT architecture - from embedded firmware to web dashboard.

## Tech Stack
- **Firmware:** Embedded C++ on ESP32 (PlatformIO)
- **Backend:** Python Flask REST API with multi-threading
- **Frontend:** React/Vite + Chart.js
- **Hardware:** DHT22 (temp/humidity), MQ-135 (air quality)

## Architecture
ESP32 → USB Serial → Flask Backend REST API  → SQLite DB → React/Vite Dashboard

## Features
- Real-time sensor readings (2s intervals)
- Live trend graphs (60s of data)
- Threshold-based OPEN/CLOSE recommendations
- Error handling and reconnection logic

## Decision Logic
**Thresholds:**
- Temperature: 60-78°F
- Humidity: < 70%
- Air Quality: > 500

- If any threshold violated -> **CLOSE**
- All favorable -> **OPEN**

**Stability Window:**
- To do

## How to Run Locally
- backend: cd backend -> pip3 install -r requirements.txt -> python3 app.py
- frontend: cd frontend -> npm install -> npm run dev
- firmware: upload via PlatformIO to ESP32

## ESP32 / Breadboard / Sensors / Wiring
<img src="esp32.jpg" alt="ESP32 wiring" height="700" width="400">

## Build notes

### Completed (Scope for intensive)
- ESP32 firmware reading 2 sensors (3 readings)
- Python Flask REST API
- Real-time React/Vite dashboard
- Live sensor values
- 3 live-updating graphs
- OPEN/CLOSE recommendation logic
- UI

### To Do

### To Do

- Add SQLite DB
- Historical Data / Analytics Page:
    - /dashboard - current live view
    - /history - filterable historical data table
    - /analytics - aggregated statistics
- Trend arrows (rising/falling indicators)
- Rolling averages (5min-30min)
- Better threshold logic (hysteresis and stability windows)
- Export data feature
- Dark mode toggle
- Related health tips?
- Weather API connection for better predictions / recommendations
- More REST endpoints beyond /api/latest
    - FastAPI
    - Proper HTTP status codes
    - Rate limiting

#### Additional for Green Energy/Industrial Systems:
- Data validation & anomaly detection (detect sensor failures, stuck readings)
- Sensor health monitoring & connectivity status
- Multi-level data aggregations (1min → hourly → daily rollups)
- Background workers for automated processing (APScheduler)
- Data retention & downsampling policy
- Alert rules engine (configurable thresholds)
- Alert history & management
- System diagnostics dashboard (API response times, error rates)
- Structured logging (JSON format with log levels)
- Simulation mode (mock sensor data for testing)
- Metrics endpoint (Prometheus format)
- Docker + Docker Compose setup
- OpenAPI documentation
- Unit tests (pytest) for decision logic