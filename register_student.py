from src.attendance_system import SmartAttendanceSystem
from src.face_capture import FaceCapture


def main() -> None:
    system = SmartAttendanceSystem(storage_path="attendance.csv", student_storage_path="students.csv")
    capture = FaceCapture()

    student_id = input("Enter student ID: ").strip()
    name = input("Enter student name: ").strip()

    if not student_id or not name:
        print("Student ID and name are required.")
        return

    try:
        image_path = capture.capture(student_id, name)
    except RuntimeError as exc:
        print(str(exc))
        return

    system.register_student(student_id, name, [0.0, 0.0, 1.0])
    print(f"Student {name} registered successfully. Image saved to {image_path}")


if __name__ == "__main__":
    main()
