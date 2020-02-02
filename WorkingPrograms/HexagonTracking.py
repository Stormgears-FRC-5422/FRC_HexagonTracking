import math
import time

import cv2
import imutils
import numpy as np


def get_angle(a, b, c):
    ang = int(abs(math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))))
    return ang


start_time = time.time()
i = 0
cap = cv2.VideoCapture("/dev/video0")
# cap = cv2.VideoCapture("/dev/video2")
while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    low_green = np.array([0, 150, 20])
    high_green = np.array([210, 270, 130])
    green_mask = cv2.inRange(frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, _, mask=green_mask)
    thresh = cv2.threshold(green, 140, 180, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    threshold_area = 0
    (h, w) = frame.shape[:2]
    w1 = w // 2
    h1 = h // 2
    cv2.circle(frame, (w1, h1), 2, (0, 0, 255), 4)
    cv2.circle(frame, (w1, h), 2, (0, 0, 255), 4)
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area > threshold_area:
            cv2.drawContours(frame, cnts, -1, (0, 255, 0), 2)
            rect = cv2.boundingRect(cnt)
            cv2.contourArea(cnt)
            assert isinstance(rect, object)
            x, y, w2, h2 = rect
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.rectangle(frame, (x, y), (x + w2, y + h2), (0, 255, 0), 2)
            cv2.putText(frame, 'Hexagon Detected', (x + w2 + 10, y + h2), 0, 0.3, (0, 255, 0))
            cv2.circle(frame, (cX, cY), 2, (0, 0, 255), 4)
            print("Angle: " + str(get_angle((w1, h1), (w1, h), (cX, cY))))

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
