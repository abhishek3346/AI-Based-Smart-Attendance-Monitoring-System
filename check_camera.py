import cv2

for idx in range(5):
    cap = cv2.VideoCapture(idx)
    opened = cap.isOpened()
    print(idx, opened)
    if opened:
        ret, frame = cap.read()
        print('frame', ret, frame is not None)
    cap.release()
