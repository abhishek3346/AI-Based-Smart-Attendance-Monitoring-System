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


##Screenshots
### Register face
<img width="1918" height="1067" alt="Screenshot 2026-07-18 005452" src="https://github.com/user-attachments/assets/4d268626-1b34-467c-aea0-f23f901cc964" />

### Mark Attendance 
<img width="1918" height="1071" alt="Screenshot 2026-07-18 005812" src="https://github.com/user-attachments/assets/cdd31328-29e8-4762-a122-cf86e4254820" />

### Attendance Marked 
<img width="630" height="287" alt="Screenshot 2026-07-18 005946" src="https://github.com/user-attachments/assets/dc74dd2b-b0b8-47b0-9a17-abe3f43eaf77" />



