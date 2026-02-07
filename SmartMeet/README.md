# SmartMeet – AI Intelligent Scheduling System

## Overview
SmartMeet is an intelligent scheduling optimizer that compresses calendar data and reduces meeting conflicts using interval-merging algorithms with a modern web interface.

## Features
- **Conflict Detection** - Identifies overlapping meetings
- **Interval Compression** - Optimizes schedule layout
- **Priority-Based Rescheduling** - Preserves high-priority meetings
- **Efficiency Scoring** - AI-powered optimization algorithm
- **Interactive Web UI** - Real-time meeting management
- **REST API Backend** - Flask-powered scheduling engine

## Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation & Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start the Flask backend** (Terminal 1):
```bash
python3 scheduler.py
```
The API will be available at `http://localhost:5000`

3. **Open the web interface** (Terminal 2):
```bash
# Navigate to the web directory and serve it
cd web
python3 -m http.server 8000
```
Then open your browser to `http://localhost:8000`

### Or use a simple alternative for the web server:
```bash
# If you have Node.js with http-server
npx http-server web -p 8000
```

## How to Use

1. **Add Meetings**: Fill in meeting details (title, date, time, priority)
2. **Set Working Hours**: Define your preferred working hours
3. **Click Optimize**: Get AI-powered schedule optimization
4. **View Results**: See conflicts and optimized schedule with efficiency scores

## API Endpoints

### POST `/api/optimize`
Optimizes meeting schedule

**Request:**
```json
{
  "meetings": [
    {
      "title": "Team Sync",
      "start": 9,
      "end": 10,
      "priority": 2,
      "date": "2026-02-07"
    }
  ],
  "preferred_hours": {
    "start": 9,
    "end": 17
  }
}
```

**Response:**
```json
{
  "conflicts": [],
  "optimized_meetings": [...],
  "total_meetings": 1,
  "average_score": 105,
  "has_conflicts": false
}
```

### GET `/api/health`
Health check endpoint

## Tech Stack
- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Algorithm**: Interval-based optimization with priority weighting

## Project Structure
```
SmartMeet/
├── scheduler.py          # Flask API backend
├── web/
│   ├── index.html       # Main interface
│   ├── script.js        # Frontend logic & API calls
│   └── style.css        # Styling
├── sample_calendar.json  # Example data
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Project-Specific Conventions

### Time Format
- Times are stored as decimal hours (9.5 = 9:30, 14.75 = 14:45)
- Frontend converts between time input and decimal format
- API accepts and returns decimal hours

### Efficiency Score Calculation
- Base: 100 points
- Penality for meetings outside preferred hours: -20
- Penalty per hour duration: -5 per hour
- Bonus per priority level: +10 per level
- Minimum score: 0

### Meeting Data Structure
```javascript
{
  "title": string,
  "start": number (decimal hours),
  "end": number (decimal hours),
  "priority": number (1-3),
  "date": string (YYYY-MM-DD),
  "efficiency_score": number (calculated)
}
```

## Troubleshooting

**"Cannot connect to backend" error?**
- Make sure Flask server is running: `python3 scheduler.py`
- Check that port 5000 is not in use

**CORS errors?**
- Flask-CORS is enabled in the backend
- Ensure web server is on different port than backend

**Time format issues?**
- Use HH:MM format in time inputs
- The application converts to decimal hours internally

## Run the Project
```bash
# Terminal 1: Start backend
python3 scheduler.py

# Terminal 2: Start web server
cd web && python3 -m http.server 8000
```

Then visit `http://localhost:8000` in your browser!
