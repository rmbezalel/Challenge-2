# SmartMeet Architecture & Data Flow Diagram

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT BROWSER                          │
│                    (http://localhost:8000)                      │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                     index.html                         │   │
│  │  ┌──────────────────────────────────────────────────┐  │   │
│  │  │         SmartMeet Meeting Scheduler UI           │  │   │
│  │  │                                                  │  │   │
│  │  │  Add Meeting Card:                              │  │   │
│  │  │  ├─ Title input field                           │  │   │
│  │  │  ├─ Date picker                                 │  │   │
│  │  │  ├─ Start time input (HH:MM)                    │  │   │
│  │  │  ├─ End time input (HH:MM)                      │  │   │
│  │  │  ├─ Priority selector (1-3)                     │  │   │
│  │  │  └─ ➕ Add Meeting Button                       │  │   │
│  │  │                                                  │  │   │
│  │  │  Working Hours Card:                            │  │   │
│  │  │  ├─ Start hour input (09:00)                    │  │   │
│  │  │  └─ End hour input (17:00)                      │  │   │
│  │  │                                                  │  │   │
│  │  │  Meetings List Card:                            │  │   │
│  │  │  ├─ Dynamic list of added meetings              │  │   │
│  │  │  ├─ Remove button for each                      │  │   │
│  │  │  └─ Clear All button                            │  │   │
│  │  │                                                  │  │   │
│  │  │  🚀 Optimize Schedule Button                    │  │   │
│  │  └──────────────────────────────────────────────────┘  │   │
│  │                                                          │   │
│  │  ┌──────────────────────────────────────────────────┐   │   │
│  │  │  Optimized Results Section (Hidden until submit) │   │   │
│  │  │  ├─ Conflicts Alert (if any)                    │   │   │
│  │  │  ├─ ✅ No conflicts message (if clean)          │   │   │
│  │  │  ├─ Optimized Meetings List:                    │   │   │
│  │  │  │  ├─ Meeting 1: Team Sync                     │   │   │
│  │  │  │  │  ├─ Time: 9:00 - 10:00                   │   │   │
│  │  │  │  │  ├─ Priority: 2                           │   │   │
│  │  │  │  │  └─ AI Score: 95/100                      │   │   │
│  │  │  │  └─ Meeting 2: ...                          │   │   │
│  │  │  │                                              │   │   │
│  │  │  └─ Summary:                                    │   │   │
│  │  │     ├─ Total Meetings: 2                        │   │   │
│  │  │     └─ Average AI Score: 97/100                │   │   │
│  │  └──────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  style.css: Responsive design, animations, colors      │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                  │
│  script.js:                                                     │
│  ├─ Event handlers (addMeeting, optimizeSchedule, etc.)      │
│  ├─ Time conversion (HH:MM ↔ decimal hours)                  │
│  ├─ API communication (fetch to localhost:5000)              │
│  ├─ Results rendering (display optimization output)          │
│  └─ Error handling (network, validation, backend errors)     │
│                                                                  │
│              ┌─────────────────────────────┐                    │
│              │   Fetch API Call (JSON)     │                    │
│              │  POST /api/optimize         │                    │
│              │  Port 5000                  │                    │
│              └────────────┬────────────────┘                    │
└─────────────────────────────┼────────────────────────────────────┘
                              │
                    NETWORK CONNECTION
                              │
┌─────────────────────────────┼────────────────────────────────────┐
│                    FLASK SERVER                                  │
│              (http://localhost:5000)                             │
│                                                                  │
│  Flask Application (scheduler.py):                              │
│  ├─ Request Handler: @app.route('/api/optimize', POST)        │
│  │  ├─ Parse incoming JSON                                    │
│  │  ├─ Extract meetings[] and preferred_hours{}               │
│  │  │                                                         │
│  │  └─ Processing Pipeline:                                  │
│  │     │                                                      │
│  │     ├─[1] detect_conflicts(meetings)                       │
│  │     │    ├─ Sort meetings by start time                   │
│  │     │    ├─ Compare adjacent meetings                      │
│  │     │    ├─ Check if end > next.start                     │
│  │     │    └─ Return list of conflict strings               │
│  │     │                                                      │
│  │     ├─[2] optimize_schedule(meetings, preferred_hours)     │
│  │     │    ├─ Sort by start time + priority                 │
│  │     │    ├─ For each meeting:                              │
│  │     │    │  ├─ Calculate efficiency_score()               │
│  │     │    │  ├─ Add to optimized list                      │
│  │     │    │  └─ Handle conflicts (higher priority wins)    │
│  │     │    └─ Return optimized_meetings[]                   │
│  │     │                                                      │
│  │     ├─[3] Calculate Statistics                             │
│  │     │    ├─ Count total_meetings                          │
│  │     │    ├─ Sum efficiency scores                         │
│  │     │    └─ Average = sum / count                         │
│  │     │                                                      │
│  │     └─[4] Construct JSON Response                          │
│  │         ├─ conflicts: [...]                                │
│  │         ├─ optimized_meetings: [...]                       │
│  │         ├─ total_meetings: N                               │
│  │         ├─ average_score: X.XX                             │
│  │         └─ has_conflicts: boolean                          │
│  │                                                            │
│  ├─ Response Handler:                                        │
│  │  ├─ Status: 200 OK                                        │
│  │  ├─ Content-Type: application/json                        │
│  │  └─ Body: JSON response object                            │
│  │                                                            │
│  ├─ Health Endpoint: @app.route('/api/health', GET)         │
│  │  └─ Returns: {"status": "SmartMeet backend is running"}  │
│  │                                                            │
│  └─ Error Handler:                                           │
│     ├─ Missing fields → 400 Bad Request                      │
│     ├─ Server errors → 500 Internal Server Error            │
│     └─ Return: {"error": "error message"}                   │
│                                                                  │
│  Supporting Functions:                                          │
│  ├─ parse_time(str): HH:MM or decimal → float                │
│  ├─ efficiency_score(meeting, hours): int 0-100+             │
│  └─ detect_conflicts(meetings): list of strings              │
│                                                                  │
│  Python Algorithm Details:                                      │
│  ├─ Efficiency Scoring:                                       │
│  │  score = 100                                              │
│  │  - 20 if outside preferred hours                         │
│  │  - 5 * duration (hours)                                  │
│  │  + 10 * priority                                         │
│  │  minimum: 0                                              │
│  │                                                           │
│  └─ Conflict Resolution:                                      │
│     if meeting overlaps with next:                           │
│       if current.priority > next.priority:                   │
│         keep current, remove next                            │
│       else:                                                  │
│         keep next, remove current                           │
│                                                                  │
│              ┌─────────────────────────────┐                   │
│              │  JSON Response (HTTP 200)   │                   │
│              │  Back to Browser            │                   │
│              └────────────────┬─────────────┘                   │
└───────────────────────────────┼────────────────────────────────┘
                                │
                    NETWORK CONNECTION
                                │
┌───────────────────────────────┼────────────────────────────────┐
│                    BROWSER (JavaScript)                        │
│                                                                 │
│  fetch() Promise Resolution:                                  │
│  ├─ Check response.ok (200-299)                              │
│  ├─ Parse response.json()                                    │
│  └─ Call displayResults(data)                                │
│                                                                 │
│  displayResults(data) Function:                              │
│  ├─ Check if has_conflicts                                  │
│  │  ├─ Yes: Show conflict alert + list conflicts           │
│  │  └─ No: Show ✅ "No conflicts" message                   │
│  │                                                            │
│  ├─ For each in optimized_meetings:                          │
│  │  ├─ Create result-item div                                │
│  │  ├─ Show meeting number, title                           │
│  │  ├─ Show time range (start - end)                        │
│  │  ├─ Show priority level (1-3)                            │
│  │  ├─ Show AI Score (efficiency_score/100)                │
│  │  └─ Color-code by score                                  │
│  │                                                            │
│  ├─ Update summary statistics:                               │
│  │  ├─ totalMeetings.textContent = total_meetings           │
│  │  └─ averageScore.textContent = average_score             │
│  │                                                            │
│  └─ Show output section (display = 'block')                 │
│                                                                 │
│  Error Handling:                                               │
│  ├─ If response not ok: alert(error message)                │
│  ├─ If network error: show backend not running message      │
│  └─ Hide loading indicator                                   │
│                                                                 │
│  Final UI State:                                              │
│  ├─ Loading animation gone                                   │
│  ├─ Results section visible                                  │
│  ├─ User can see optimized schedule                          │
│  ├─ Can add more meetings                                    │
│  └─ Can click Optimize again                                 │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Request-Response Flow (Detailed)

### Step 1: User Clicks "Optimize"
```
Browser: optimizeSchedule() function called
  ├─ Validate input (meetings > 0, times valid)
  ├─ Show loading indicator
  ├─ Build payload object:
  │  ├─ meetings: [
  │  │    {title, start (decimal), end (decimal), priority, date}
  │  │  ]
  │  └─ preferred_hours: {start: 9, end: 17}
  └─ Call fetch(POST, /api/optimize, payload)
```

### Step 2: Server Processes Request
```
Flask: @app.route('/api/optimize') handler
  ├─ Receive JSON from browser
  ├─ Extract meetings and preferred_hours
  ├─ validate_input()
  │  └─ If invalid → return 400 error
  │
  ├─ detect_conflicts(meetings)
  │  └─ Returns: ["Team Sync overlaps with Client Call"]
  │
  ├─ optimize_schedule(meetings, preferred_hours)
  │  └─ Returns: [{...}, {...}, ...]
  │
  ├─ Calculate average_score
  │
  └─ Return JSON response (200 OK)
```

### Step 3: Browser Displays Results
```
JavaScript: displayResults(data)
  ├─ Render conflicts section (if any)
  ├─ Render optimized meetings:
  │  ├─ Number badge
  │  ├─ Meeting title
  │  ├─ Time range
  │  ├─ Priority badge
  │  └─ Efficiency score (colored)
  │
  ├─ Update summary:
  │  ├─ Total meetings count
  │  └─ Average score
  │
  └─ Show results section (fade in animation)
```

## 📊 Example Data Transformation

### Frontend Input (Before Submission)
```javascript
const meetings = [
  {
    title: "Team Sync",
    date: "2026-02-07",
    start: "09:00",    // HH:MM format
    end: "10:00",      // HH:MM format
    priority: 2
  }
]
```

### Conversion (JavaScript)
```javascript
const converted = {
  title: "Team Sync",
  start: 9.0,         // Converted to decimal
  end: 10.0,          // Converted to decimal
  priority: 2
}
```

### Sent to Backend (JSON)
```json
{
  "meetings": [
    {
      "title": "Team Sync",
      "start": 9.0,
      "end": 10.0,
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

### Backend Processing
```python
# detect_conflicts: checks for overlaps
# optimize_schedule: sorts and deduplicates
# efficiency_score: calculates 100 - 20*outside - 5*duration + 10*priority
```

### Response from Backend
```json
{
  "conflicts": [],
  "optimized_meetings": [
    {
      "title": "Team Sync",
      "start": 9.0,
      "end": 10.0,
      "priority": 2,
      "date": "2026-02-07",
      "efficiency_score": 95
    }
  ],
  "total_meetings": 1,
  "average_score": 95,
  "has_conflicts": false
}
```

### Rendered in Frontend
```
🧠 OPTIMIZED SCHEDULE

✅ No conflicts detected

📊 OPTIMIZED MEETINGS

1. Team Sync
   ⏰ 9.0 – 10.0
   ⭐ Priority: 2
   📊 AI Score: 95/100

📈 SUMMARY
• Total Meetings: 1
• Average AI Score: 95/100
```

## 🔌 Integration Points

1. **Frontend → Backend**: 
   - Location: script.js line ~180
   - Method: `fetch()` with POST
   - Endpoint: `http://localhost:5000/api/optimize`

2. **Backend → Frontend**:
   - Location: scheduler.py line ~98-118
   - Format: JSON response with status code
   - Headers: Content-Type: application/json

3. **Error Handling**:
   - Frontend: Catches fetch errors and shows user-friendly messages
   - Backend: Returns error codes (400, 500) with error message

## 🚀 Deployment Architecture (Future)

```
┌────────────────┐
│  web/static/   │  (Frontend)
├────────────────┤
│  CDN / S3      │  (Serve HTML/CSS/JS)
└────────────────┘
        ↕️
┌────────────────────────────────────────┐
│  Heroku / AWS / Vercel                 │
├────────────────────────────────────────┤
│  scheduler.py (Flask API)              │
│  /api/optimize endpoint                │
│  /api/health endpoint                  │
├────────────────────────────────────────┤
│  (Optional) Database (PostgreSQL/SQLite)
└────────────────────────────────────────┘
```
