import cv2

cap = cv2.VideoCapture("/dev/video0")
while True:
    _, frame = cap.read()

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break