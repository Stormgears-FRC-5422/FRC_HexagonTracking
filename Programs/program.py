import imutils
import cv2
import numpy as np

cap = cv2.VideoCapture("/dev/video2")
while True:
    _, frame = cap.read()
    low_green = np.array([157, 218, 101])
    high_green = np.array([116,217,35])
    green_mask = cv2.inRange(frame, low_green, high_green)
    green = cv2.bitwise_and(frame, green_mask, mask = green_mask)
    cv2.imshow("Frame", green)
    key = cv2.waitKey(1)
    if key == 27:
        break

'''
ret,image = cv2.threshold(img,140,144,cv2.THRESH_BINARY)


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cv2.drawContours(image, cnts, -1, (0,255,0), 10)

# loop over the contours
for c in cnts:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # draw the contour and center of the shape on the image
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, "center", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
 
'''
