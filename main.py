from src.attendance_system import SmartAttendanceSystem


def main() -> None:
    system = SmartAttendanceSystem(storage_path="attendance.csv")

    system.register_student("S001", "Alice", [0.1, 0.2, 0.3])
    system.register_student("S002", "Bob", [0.8, 0.9, 1.0])

    system.mark_attendance("S001", [0.1, 0.2, 0.3], threshold=0.99)
    system.mark_attendance("S002", [0.2, 0.3, 0.4], threshold=0.95)

    print("Attendance summary:")
    print(system.get_summary())


if __name__ == "__main__":
    main()
