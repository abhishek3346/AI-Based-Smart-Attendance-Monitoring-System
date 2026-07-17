from src.attendance_system import SmartAttendanceSystem
from src.face_capture import FaceCapture


def main() -> None:
    system = SmartAttendanceSystem(storage_path="attendance.csv", student_storage_path="students.csv")
    capture = FaceCapture()

    student_id = input("Enter student ID: ").strip()
    threshold_input = input("Enter similarity threshold (default 0.95): ").strip() or "0.95"

    if not student_id:
        print("Student ID is required.")
        return

    try:
        threshold = float(threshold_input)
    except ValueError:
        print("Please enter a valid threshold.")
        return

    try:
        image_path = capture.capture(student_id, "attendance")
    except RuntimeError as exc:
        print(str(exc))
        return

    try:
        result = system.mark_attendance(student_id, [0.0, 0.0, 1.0], threshold=threshold)
        print(f"Attendance marked: {result}. Image saved to {image_path}")
    except ValueError as exc:
        print(str(exc))


if __name__ == "__main__":
    main()
