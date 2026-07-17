import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.camera_utils import extract_embedding_from_frame


def test_extract_embedding_from_frame_returns_vector():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    frame[20:80, 20:80] = 255

    embedding = extract_embedding_from_frame(frame)

    assert len(embedding) > 0
    assert all(0.0 <= value <= 1.0 for value in embedding)


def test_capture_frame_returns_fallback_when_camera_unavailable():
    frame = capture_frame(camera_index=999)

    assert frame.shape[0] > 0
    assert frame.shape[1] > 0


if __name__ == "__main__":
    test_extract_embedding_from_frame_returns_vector()
    test_capture_frame_returns_fallback_when_camera_unavailable()
    print("Camera utility test passed")
