from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

def parse_time(time_str):
    """
    Converts human-friendly time formats to float hours.
    Examples:
    9      -> 9.0
    9.5    -> 9.5
    9:30   -> 9.5
    14:45  -> 14.75
    """
    time_str = str(time_str).strip()
    if ":" in time_str:
        hour, minute = time_str.split(":")
        return int(hour) + int(minute) / 60
    return float(time_str)


def detect_conflicts(meetings):
    meetings = sorted(meetings, key=lambda x: x["start"])
    conflicts = []

    for i in range(len(meetings) - 1):
        if meetings[i]["end"] > meetings[i + 1]["start"]:
            conflicts.append(
                f"{meetings[i]['title']} overlaps with {meetings[i + 1]['title']}"
            )
    return conflicts


def efficiency_score(meeting, preferred_hours):
    score = 100
    duration = meeting["end"] - meeting["start"]

    if meeting["start"] < preferred_hours["start"] or meeting["end"] > preferred_hours["end"]:
        score -= 20

    score -= duration * 5
    score += meeting["priority"] * 10

    return max(int(score), 0)


def optimize_schedule(meetings, preferred_hours):
    meetings = sorted(meetings, key=lambda x: (x["start"], -x["priority"]))
    optimized = []

    for meeting in meetings:
        meeting["efficiency_score"] = efficiency_score(meeting, preferred_hours)

        if not optimized:
            optimized.append(meeting)
        else:
            last = optimized[-1]

            if meeting["start"] < last["end"]:
                if meeting["priority"] > last["priority"]:
                    optimized[-1] = meeting
            else:
                optimized.append(meeting)

    return optimized


def print_report(conflicts, optimized):
    print("\n" + "=" * 60)
    print("🧠 SMARTMEET – AI SCHEDULING REPORT")
    print("=" * 60)

    print("\n🔎 Conflict Analysis")
    if conflicts:
        for c in conflicts:
            print(f"  ⚠️  {c}")
    else:
        print("  ✅ No conflicts detected")

    print("\n⚡ Optimized Schedule")
    for i, m in enumerate(optimized, 1):
        print(f"""
  {i}. 📌 {m['title']}
     ⏰ Time     : {m['start']} – {m['end']}
     ⭐ Priority : {m['priority']}
     📊 AI Score : {m['efficiency_score']}/100
        """)

    avg = sum(m["efficiency_score"] for m in optimized) / len(optimized)
    print("📈 Summary")
    print(f"  • Meetings Scheduled : {len(optimized)}")
    print(f"  • Average AI Score   : {round(avg, 2)}")

    print("\n✅ Scheduling optimized successfully")
    print("=" * 60)


def format_time(hours):
    """Convert float hours back to HH:MM format"""
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h:02d}:{m:02d}"


@app.route('/api/optimize', methods=['POST'])
def api_optimize():
    """API endpoint for optimizing schedule"""
    try:
        data = request.json
        meetings = data.get('meetings', [])
        preferred_hours = data.get('preferred_hours', {'start': 9, 'end': 17})
        
        # Validate input
        if not meetings:
            return jsonify({'error': 'No meetings provided'}), 400
        
        conflicts = detect_conflicts(meetings)
        optimized = optimize_schedule(meetings, preferred_hours)
        
        # Calculate average efficiency score
        avg_score = sum(m["efficiency_score"] for m in optimized) / len(optimized) if optimized else 0
        
        # Format response
        result = {
            'conflicts': conflicts,
            'optimized_meetings': optimized,
            'total_meetings': len(optimized),
            'average_score': round(avg_score, 2),
            'has_conflicts': len(conflicts) > 0
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'SmartMeet backend is running'}), 200


# 🚀 MAIN EXECUTION
if __name__ == "__main__":
    app.run(debug=True, port=5050)
