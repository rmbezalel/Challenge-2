# SmartMeet Setup & Deployment Guide

## 🚀 Quick Start (2 Steps)

### Step 1: Install Dependencies
```bash
cd /Users/bezalelrm/Documents/Project_CLG/SmartMeet
pip install -r requirements.txt
```

### Step 2: Run Both Services

**Terminal 1 - Start Flask Backend (API Server)**
```bash
cd /Users/bezalelrm/Documents/Project_CLG/SmartMeet
python3 scheduler.py
```
Output should show:
```
 * Serving Flask app 'scheduler'
 * Running on http://127.0.0.1:5000
```

**Terminal 2 - Start Web Server (Frontend)**
```bash
cd /Users/bezalelrm/Documents/Project_CLG/SmartMeet/web
python3 -m http.server 8000
```
Output should show:
```
Serving HTTP on 0.0.0.0 port 8000
```

### Step 3: Open in Browser
Go to: **http://localhost:8000**

## ✅ Verification

### Check Backend Health
```bash
curl http://localhost:5000/api/health
# Expected: {"status": "SmartMeet backend is running"}
```

### Check Frontend
- Open http://localhost:8000 in browser
- You should see the SmartMeet interface with:
  - "Add Meeting" form
  - "Working Hours" settings
  - Meeting list
  - Optimize button

## 📋 How to Use

1. **Add a Meeting**:
   - Title: Enter meeting name
   - Date: Select date
   - Start/End Time: Set times
   - Priority: 1 (Low), 2 (Medium), 3 (High)
   - Click "➕ Add Meeting"

2. **Set Working Hours**:
   - Start Hour: Default 09:00
   - End Hour: Default 17:00

3. **Optimize**:
   - Click "🚀 Optimize Schedule"
   - View results with AI scores

## 🔧 Architecture

```
Frontend (HTML/CSS/JS)  ←→  Backend (Flask API)
Port 8000                     Port 5000
├── index.html           ├── scheduler.py
├── script.js            └── Python Functions
└── style.css
```

### Frontend Flow:
1. User adds meetings via form
2. Clicks "Optimize Schedule"
3. JavaScript sends POST to `http://localhost:5000/api/optimize`
4. Receives optimized results
5. Displays results with efficiency scores

### Backend Flow:
1. Receives meeting data
2. Detects conflicts
3. Optimizes schedule by priority
4. Calculates efficiency scores
5. Returns JSON response

## 🐛 Troubleshooting

### "Cannot connect to backend"
- Check Flask is running on Terminal 1
- Verify port 5000 is available: `lsof -i :5000`
- Restart if needed: Kill process and run `python3 scheduler.py` again

### "Frontend not loading"
- Check web server is running on Terminal 2
- Verify port 8000 is available: `lsof -i :8000`
- Clear browser cache (Cmd+Shift+Delete on macOS)

### CORS Errors
- Flask-CORS is configured to allow all origins
- If issues persist, restart backend with `python3 scheduler.py`

### Time format issues
- Input uses HH:MM format
- Internally converted to decimal hours (9.5 = 9:30)
- Check meetings list to confirm format

## 📊 Sample Data

You can also test with `sample_calendar.json`:
```json
{
  "meetings": [
    {"title": "Team Sync", "start": 9, "end": 10, "priority": 2},
    {"title": "Client Call", "start": 9.5, "end": 11, "priority": 3},
    {"title": "Project Review", "start": 16, "end": 18, "priority": 1}
  ],
  "preferred_hours": {"start": 9, "end": 17}
}
```

## 🎯 Success Indicators

✅ Backend running: Flask server shows "Running on http://127.0.0.1:5000"
✅ Frontend running: Web server shows "Serving HTTP on 0.0.0.0 port 8000"
✅ Browser access: http://localhost:8000 loads without errors
✅ API working: Can add meetings and click optimize
✅ Results display: Shows optimized meetings with efficiency scores

## 📞 Need Help?

- Check README.md for API documentation
- Verify all files are in correct locations
- Ensure Python 3.7+ is installed: `python3 --version`
- Ensure Flask installed correctly: `pip list | grep -i flask`
