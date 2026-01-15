# MK.1 – Environmental Monitoring & Decision System

## Overview
Brief paragraph: what it does and why

## Architecture
ESP32 → USB Serial → Flask Backend REST API  → SQLite DB → React/Vite Dashboard

## Decision Logic
Thresholds + stability window

## Dashboard
Screenshots + explanation

## How to Run Locally
backend - python3 app.py
frontend - npm run dev

## Demo
Link to short screen recording

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

### To do
- Add SQLite DB
- Trend arrows (rising/falling indicators)
- Rolling averages (5min-30min)
- Better threshold logic (hystersis and stability windows)
- Export data feature
- Dark mode toggle
- Related health tips?
- Weather API connection for better predictions / recommendations