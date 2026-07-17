import os
from datetime import datetime

import cv2
import numpy as np


class FaceCapture:
    def __init__(self, save_dir: str = "captured_faces") -> None:
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def capture(self, student_id: str, name: str) -> str:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Camera could not be opened")

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    raise RuntimeError("Failed to read from camera")

                cv2.putText(frame, f"Student: {name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, "Press SPACE to capture, Q to quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.imshow("Capture Face", frame)

                key = cv2.waitKey(30) & 0xFF
                if key == ord(" "):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{student_id}_{name.replace(' ', '_')}_{timestamp}.jpg"
                    path = os.path.join(self.save_dir, filename)
                    cv2.imwrite(path, frame)
                    cv2.destroyAllWindows()
                    return path
                if key == ord("q"):
                    cv2.destroyAllWindows()
                    raise RuntimeError("Capture cancelled")
        finally:
            cap.release()
