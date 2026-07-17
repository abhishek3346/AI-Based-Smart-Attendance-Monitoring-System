import csv
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.attendance_system import SmartAttendanceSystem


def test_register_and_mark_attendance():
    with tempfile.TemporaryDirectory() as tmpdir:
        system = SmartAttendanceSystem(storage_path=os.path.join(tmpdir, "attendance.csv"))

        system.register_student("S001", "Alice", [0.1, 0.2, 0.3])
        system.register_student("S002", "Bob", [0.8, 0.9, 1.0])

        result = system.mark_attendance("S001", [0.1, 0.2, 0.3], threshold=0.99)
        assert result["status"] == "present"
        assert result["student_id"] == "S001"

        summary = system.get_summary()
        assert summary["total_records"] == 1
        assert summary["present_count"] == 1

        with open(system.storage_path, newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        assert len(rows) == 1
        assert rows[0]["student_id"] == "S001"


if __name__ == "__main__":
    test_register_and_mark_attendance()
    print("Attendance test passed")
