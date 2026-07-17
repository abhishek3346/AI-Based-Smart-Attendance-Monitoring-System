import subprocess
import sys

import numpy as np

try:
    import cv2
except ImportError:  # pragma: no cover - fallback for environments without OpenCV
    cv2 = None


def _ensure_cv2() -> None:
    global cv2
    if cv2 is not None:
        return

    try:
        import cv2 as imported_cv2  # type: ignore
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
            import cv2 as imported_cv2  # type: ignore
        except Exception:
            imported_cv2 = None

    cv2 = imported_cv2


def extract_embedding_from_frame(frame: np.ndarray) -> list[float]:
    if cv2 is not None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (64, 64), interpolation=cv2.INTER_AREA)
        normalized = resized.astype(np.float32) / 255.0
        flat = normalized.reshape(-1)
        return [float(value) for value in flat[:128]]

    gray = np.mean(frame, axis=2)
    resized = np.array(gray, dtype=np.float32)
    resized = np.resize(resized, (64, 64))
    normalized = resized / 255.0
    flat = normalized.reshape(-1)
    return [float(value) for value in flat[:128]]


def capture_frame(camera_index: int = 0) -> np.ndarray:
    _ensure_cv2()
    if cv2 is None:
        raise RuntimeError("OpenCV is not installed. Please run '.\\.venv\\Scripts\\python.exe -m pip install opencv-python' and try again.")

    backends = []
    if hasattr(cv2, "CAP_DSHOW"):
        backends.append(cv2.CAP_DSHOW)
    if hasattr(cv2, "CAP_MSMF"):
        backends.append(cv2.CAP_MSMF)
    backends.append(cv2.CAP_ANY)

    for backend in backends:
        for index in [camera_index, 0, 1, 2, 3, -1]:
            cap = cv2.VideoCapture(index, backend)
            if not cap.isOpened():
                cap.release()
                continue

            try:
                ret, frame = cap.read()
                if ret and frame is not None:
                    return frame
            finally:
                cap.release()

    raise RuntimeError("Unable to access a camera. Please connect a webcam, allow camera permissions, or try using a different camera app first.")
