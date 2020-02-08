import cv2
import imutils
import numpy as np



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
    low_yellow = np.array([20, 100, 110])
    high_yellow = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(frame, low_yellow, high_yellow)
    yellow = cv2.bitwise_and(frame, frame, _, mask=yellow_mask)
    thresh = cv2.threshold(yellow, 140, 180, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    min_threshold_area = 0
    max_threshold_area = 5000
    (h, w) = frame.shape[:2]

    w1 = w // 2
    if calibrateCounter:
        calibrateW = w1
        calibrateH = h
    h1 = h // 2
    cv2.circle(frame, (w1, h1), 2, color, 4)
    cv2.circle(frame, (w1, h), 2, color, 4)
    if len(cnts) == 1:
        print("CONTOURS: ", len(cnts))
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            print("Countour Area: ", area)
            if area > min_threshold_area:
                cv2.drawContours(frame, cnts, -1, color, 2)
                rect = cv2.boundingRect(cnt)
                cv2.contourArea(cnt)
                assert isinstance(rect, object)
                x, y, w2, h2 = rect
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(frame, (x, y), color, 2)
                cv2.putText(frame, 'Ball Detected', (x + w2 + 10, y + h2), 0, 0.3, color)
                cv2.circle(frame, (cX, cY), 2, color, 4)
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
                if area > min_threshold_area:
                    cv2.drawContours(frame, last_cnts, -1, color, 2)
                    rect1 = cv2.boundingRect(i)
                    cv2.contourArea(i)
                    assert isinstance(rect1, object)
                    x1, y1, w3, h3 = rect1
                    M = cv2.moments(i)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.cirlce(frame, (x1, y1), color, 2)
                    cv2.putText(frame, 'Hexagon Detected', (x1 + w3 + 10, y1 + h3), 0, 0.3, color)
                    cv2.circle(frame, (cX, cY), 2, color, 4)

            f += 1
        else:
            pass
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
