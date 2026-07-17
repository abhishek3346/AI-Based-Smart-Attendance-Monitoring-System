# AI Smart Attendance System

A simple Python-based smart attendance system that uses a webcam and OpenCV face detection to register people and mark attendance automatically.

## Features
- Register a face with a name
- Detect faces from the webcam in real time
- Match recognized faces against stored profiles
- Save attendance records in a CSV file

## Setup
1. Create and activate a virtual environment:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Register a person:
   - `python register_student.py`
4. Start attendance tracking:
   - `python mark_attendance.py`

## Notes
- A working webcam is required.
- The system stores face samples in the `captured_faces/` folder.
- Attendance logs are written to `attendance.csv`.
