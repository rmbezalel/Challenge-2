def parse_time(time_str):
    """
    Converts human-friendly time formats to float hours.
    Examples:
    9      -> 9.0
    9.5    -> 9.5
    9:30   -> 9.5
    14:45  -> 14.75
    """
    time_str = time_str.strip()
    if ":" in time_str:
        hour, minute = time_str.split(":")
        return int(hour) + int(minute) / 60
    return float(time_str)


def get_meetings():
    meetings = []
    print("\n📅 Welcome to SmartMeet – AI Scheduling Assistant")
    print("Enter your meetings below\n")

    while True:
        title = input("📌 Meeting title: ").strip()

        start = parse_time(
            input("⏰ Start time (e.g., 9, 9.5, 9:30): ")
        )
        end = parse_time(
            input("⏰ End time   (e.g., 10, 10.5, 10:30): ")
        )

        priority = int(
            input("⭐ Priority (1 = Low, 2 = Medium, 3 = High): ")
        )

        meetings.append({
            "title": title,
            "start": start,
            "end": end,
            "priority": priority
        })

        more = input("\n➕ Add another meeting? (y/n): ").lower()
        if more != "y":
            break

        print("-" * 40)

    return meetings


def get_preferred_hours():
    print("\n🕘 Preferred Working Hours")

    start = parse_time(
        input("Start hour (e.g., 9 or 9:30): ")
    )
    end = parse_time(
        input("End hour   (e.g., 17 or 17:30): ")
    )

    return {"start": start, "end": end}


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


# 🚀 MAIN EXECUTION
if __name__ == "__main__":
    meetings = get_meetings()
    preferred_hours = get_preferred_hours()

    conflicts = detect_conflicts(meetings)
    optimized = optimize_schedule(meetings, preferred_hours)

    print_report(conflicts, optimized)
