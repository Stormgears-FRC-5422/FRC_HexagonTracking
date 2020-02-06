import math

import cv2
import imutils
import numpy as np


def get_angle(a, b, c):
    ang = int(abs(math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))))
    return ang


def distance_calc(height, magic):
    distance = int(((magic * 56) / height))
    return distance


def height_calc(centerX, w1, centerY, h):
    distance = math.sqrt(((centerX - w1) ** 2) + ((centerY - h) ** 2))
    return distance


f = 0
color = (0, 0, 255)
i = 0
cap = cv2.VideoCapture("/dev/video0")
# cap = cv2.VideoCapture("/dev/video2")
last_cnts = []
calibrateCounter = True
while True:
    _, yframe = cap.read()
    frame = cv2.cvtColor(yframe, cv2.COLOR_BGR2HSV)
    frame = cv2.resize(frame, (640, 480))
    low_green = np.array([49, 87, 103])
    high_green = np.array([85, 244, 255])
    green_mask = cv2.inRange(frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, _, mask=green_mask)
    thresh = cv2.threshold(green, 140, 180, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    threshold_area = 10
    (h, w) = frame.shape[:2]
    if calibrateCounter:
        calibrateH = h
    w1 = w // 2
    if calibrateCounter:
        calibrateW = w1
    h1 = h // 2
    cv2.circle(frame, (w1, h1), 2, color, 4)
    cv2.circle(frame, (w1, h), 2, color, 4)
    if len(cnts) == 1:
        print("CONTOURS: ", len(cnts))
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            if area > threshold_area:
                cv2.drawContours(frame, cnts, -1, color, 2)
                rect = cv2.boundingRect(cnt)
                cv2.contourArea(cnt)
                assert isinstance(rect, object)
                x, y, w2, h2 = rect
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if calibrateCounter:
                    calibrateCx = cX
                if calibrateCounter:
                    calibrateCy = cY
                if calibrateCounter:
                    magic = (height_calc(calibrateCx, calibrateW, calibrateCy, calibrateH) * 20) / 56
                    calibrateCounter = False
                cv2.rectangle(frame, (x, y), (x + w2, y + h2), color, 2)
                cv2.putText(frame, 'Hexagon Detected', (x + w2 + 10, y + h2), 0, 0.3, color)
                cv2.circle(frame, (cX, cY), 2, color, 4)
                print("Angle: " + str(get_angle((w1, h1), (w1, h), (cX, cY))))
                print("Distance: ", distance_calc(height_calc(cX, w1, cY, h), magic))
                if len(last_cnts) == 1:
                    last_cnts.pop()
                else:
                    pass
                last_cnts.extend(cnts)
                f = 0
    else:
        if f < 500:
            for i in last_cnts:
                usePreviousLocation = True
                area = cv2.contourArea(i)
                if area > threshold_area:
                    cv2.drawContours(frame, last_cnts, -1, color, 2)
                    rect1 = cv2.boundingRect(i)
                    cv2.contourArea(i)
                    assert isinstance(rect1, object)
                    x1, y1, w3, h3 = rect1
                    M = cv2.moments(i)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.rectangle(frame, (x1, y1), (x1 + w3, y1 + h3), color, 2)
                    cv2.putText(frame, 'Hexagon Detected', (x1 + w3 + 10, y1 + h3), 0, 0.3, color)
                    cv2.circle(frame, (cX, cY), 2, color, 4)
                    print("Angle: " + str(get_angle((w1, h1), (w1, h), (cX, cY))))
                    print("Distance: ", distance_calc(w3))

            f += 1
        else:
            pass
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
