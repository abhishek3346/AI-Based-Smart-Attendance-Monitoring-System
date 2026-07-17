import csv
import os
from typing import Dict, List


class SmartAttendanceSystem:
    def __init__(self, storage_path: str | None = None, student_storage_path: str | None = None) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir)
        data_dir = os.path.join(project_root, "data")
        os.makedirs(data_dir, exist_ok=True)
        self.storage_path = storage_path or os.path.join(data_dir, "attendance.csv")
        self.student_storage_path = student_storage_path or os.path.join(data_dir, "students.csv")
        self.students: Dict[str, Dict[str, object]] = {}
        self._ensure_storage_file()
        self._ensure_student_storage_file()
        self._load_students()

    def _ensure_storage_file(self) -> None:
        directory = os.path.dirname(self.storage_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["student_id", "name", "timestamp", "status"])
                writer.writeheader()

    def _ensure_student_storage_file(self) -> None:
        directory = os.path.dirname(self.student_storage_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.student_storage_path):
            with open(self.student_storage_path, "w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["student_id", "name", "embedding"])
                writer.writeheader()

    def register_student(self, student_id: str, name: str, embedding: List[float]) -> Dict[str, object]:
        self.students[student_id] = {"student_id": student_id, "name": name, "embedding": embedding}
        self._save_student(student_id, name, embedding)
        return self.students[student_id]

    def mark_attendance(self, student_id: str, embedding: List[float], threshold: float = 0.95) -> Dict[str, object]:
        student = self.students.get(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        similarity = self._cosine_similarity(student["embedding"], embedding)
        status = "present" if similarity >= threshold else "absent"

        record = {
            "student_id": student_id,
            "name": student["name"],
            "timestamp": self._now(),
            "status": status,
        }

        self._append_record(record)
        return record

    def get_summary(self) -> Dict[str, int]:
        with open(self.storage_path, newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        present_count = sum(1 for row in rows if row.get("status") == "present")
        return {"total_records": len(rows), "present_count": present_count, "absent_count": len(rows) - present_count}

    def _load_students(self) -> None:
        if not os.path.exists(self.student_storage_path):
            return
        with open(self.student_storage_path, newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            if not row.get("student_id"):
                continue
            self.students[row["student_id"]] = {
                "student_id": row["student_id"],
                "name": row["name"],
                "embedding": self._parse_embedding(row.get("embedding", "")),
            }

    def _save_student(self, student_id: str, name: str, embedding: List[float]) -> None:
        try:
            with open(self.student_storage_path, "a", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["student_id", "name", "embedding"])
                writer.writerow({"student_id": student_id, "name": name, "embedding": ",".join(str(value) for value in embedding)})
        except PermissionError:
            print("Warning: could not save student data due to file permission issues.")

    def _parse_embedding(self, value: str) -> List[float]:
        if not value:
            return []
        return [float(item.strip()) for item in value.split(",") if item.strip()]

    def _append_record(self, record: Dict[str, object]) -> None:
        try:
            with open(self.storage_path, "a", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["student_id", "name", "timestamp", "status"])
                writer.writerow(record)
        except PermissionError:
            print("Warning: could not save attendance record due to file permission issues.")

    def _cosine_similarity(self, source: List[float], target: List[float]) -> float:
        if len(source) != len(target):
            raise ValueError("Embedding lengths must match")
        if not source:
            return 0.0

        dot = sum(a * b for a, b in zip(source, target))
        norm_source = sum(a * a for a in source) ** 0.5
        norm_target = sum(b * b for b in target) ** 0.5
        if norm_source == 0 or norm_target == 0:
            return 0.0
        return dot / (norm_source * norm_target)

    def _now(self) -> str:
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
