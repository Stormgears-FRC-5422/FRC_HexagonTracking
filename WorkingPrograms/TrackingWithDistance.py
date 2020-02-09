import math
import xml.etree.ElementTree as ET
from ast import literal_eval as make_tuple

import cv2
import imutils
import numpy as np

tree = ET.parse('Settings.xml')
root = tree.getroot()

min_threshold_area = int(root[0][0].text)
max_threshold_area = int(root[0][1].text)
color = make_tuple(root[0][2].text)
frameSize = make_tuple(root[0][3].text)
lowGreenRange = make_tuple(root[0][4].text)
highGreenRange = make_tuple(root[0][5].text)

cap = cv2.VideoCapture("/dev/video0")

last_cnts = []
returnArray = []
i = 0
OldContourCounter = 0


def get_angle(a, b, c):
    ang = int(abs(math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))))
    return ang


def initFrame():
    _, yframe = cap.read()
    frame = cv2.cvtColor(yframe, cv2.COLOR_BGR2HSV)
    frame = cv2.resize(frame, frameSize)
    low_green = np.array(lowGreenRange)
    high_green = np.array(highGreenRange)
    green_mask = cv2.inRange(frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, _, mask=green_mask)
    thresh = cv2.threshold(green, 140, 180, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    (h, w) = frame.shape[:2]
    w1 = w // 2
    h1 = h // 2
    cv2.circle(yframe, (w1, h1), 2, color, 4)
    cv2.circle(yframe, (w1, h), 2, color, 4)
    returnArray.clear()
    returnArray.append(cnts)
    returnArray.append(frame)
    returnArray.append(yframe)


def analyzeFrame(usePreviousCnt, OldPositionCounter):
    if not usePreviousCnt:
        current = returnArray[0]
    else:
        current = last_cnts
    for cnt in current:
        area = cv2.contourArea(cnt)
        if min_threshold_area < area < max_threshold_area:
            cv2.drawContours(returnArray[2], current, -1, color, 2)
            rect = cv2.minAreaRect(cnt)
            cv2.contourArea(cnt)
            assert isinstance(rect, object)
            (x, y), (h2, w2), angle = rect
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(returnArray[2], [box], 0, color, 3)
            cv2.circle(returnArray[2], (cX, cY), 2, color, 4)
            print("Angle of the Hexagon: ", int(angle))
            if angle <= 1 or angle <= -1:
                print("Distance: ", int(960 / w2 * 12))
            else:
                print("Distance: ", int(960 / h2 * 12))
            if usePreviousCnt == False:
                if len(last_cnts) == 1:
                    last_cnts.pop()
                else:
                    pass
                last_cnts.extend(returnArray[0])
                OldPositionCounter = 0
            else:
                OldPositionCounter += 1


while True:
    initFrame()
    if len(returnArray[0]) == 1:
        analyzeFrame(usePreviousCnt=False, OldPositionCounter=OldContourCounter)
    else:
        if OldContourCounter < 500:
            analyzeFrame(usePreviousCnt=True, OldPositionCounter=OldContourCounter)
        else:
            pass
    cv2.imshow("Frame", returnArray[2])
    key = cv2.waitKey(1)
    if key == 27:
        break
