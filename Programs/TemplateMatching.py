import cv2 as cv

# img = cv.imread('PicOfHexagon.png', 0)
template = cv.imread('template.png', 0)
w, h = template.shape[::-1]
# Apply template Matching
cap = cv.VideoCapture("/dev/video0")
while True:
    _, frame = cap.read()
    img = cv.imread(frame, 0)
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img, top_left, bottom_right, 255, 2)

    cv.imshow("Frame", img)
    key = cv.waitKey(1)
    if key == 27:
        break
