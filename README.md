SmartMeet – Intelligent Scheduling System
Overview

SmartMeet is a small but thoughtful scheduling project built to solve a common problem: messy calendars.
When meetings overlap or fill up working hours inefficiently, it becomes hard to decide what really matters.

This project takes a simple, practical approach. It accepts meeting details from the user, checks for conflicts, and creates a cleaner schedule by giving importance to higher-priority meetings.

The goal is not to replace full calendar apps, but to show how intelligent scheduling logic can improve everyday planning.

Why This Project Exists

While working with calendars, I noticed that most tools:

Don’t explain why conflicts happen

Treat all meetings the same

Don’t help users understand scheduling quality

SmartMeet was built to experiment with:

Clear conflict detection

Priority-based decisions

Easy-to-understand output

What SmartMeet Does

Detects overlapping meetings

Optimizes time blocks using simple interval logic

Protects important meetings during conflicts

Scores meetings to show how well they fit the schedule

Accepts human-friendly time formats like 9:30 or 14:45

Everything happens through a guided command-line interface, so the user always knows what’s going on.

How It Works (Simple Flow)

The user enters meeting details one by one

Preferred working hours are defined

The system checks for conflicts

Meetings are optimized based on priority

A clean scheduling report is displayed

Creative Feature: Priority Protection

Each meeting is assigned a priority level:

High priority meetings are preserved

Lower priority meetings adjust during conflicts

This mirrors how people naturally plan their day and makes the output feel more realistic.

Technology Used

Python for core logic

Simple data structures (no external libraries)

Sorting and interval-based decision logic

The focus is on readability and logic, not heavy frameworks.

How to Run

Make sure Python 3 is installed, then run:

python3 scheduler.py


You’ll be guided through the entire process interactively.

Future Improvements

Some ideas I would like to explore next:

Natural language meeting input

Saving schedules to files

A small web interface

Calendar API integration

About the Project

This project was created as part of a challenge to demonstrate:

Clean problem solving

User-friendly CLI design

Practical scheduling logic

Clear and readable code

Author

Bezalel RM
B.Tech – Computer Science (AI & ML)
