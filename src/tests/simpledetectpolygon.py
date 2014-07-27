import cv2 as cv
import numpy as np

# load color image
im = cv.imread('../images/shapes.png')
imcopy = im.copy()
gray = cv.cvtColor(im, cv.COLOR_RGB2GRAY)
#thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

# find contours, fit to polygon, and determine if rectangular
contours, hierarchy = cv.findContours(gray, mode=cv.RETR_LIST, method=cv.CHAIN_APPROX_SIMPLE)

for c in contours:
  poly = cv.approxPolyDP(np.array(c), 0.02*cv.arcLength(c,True), True)

  # bounding box
  rect = cv.minAreaRect(c)
  box = cv.cv.BoxPoints(rect)
  box = np.int0(box)

  cv.drawContours(im, [box], 0, (0,0,255), 1)
  if len(poly) == 4:
    cv.drawContours(imcopy, [box], 0, (0,0,255), 1)

# show images
cv.imshow('all bounding boxes', im)
cv.waitKey(0)

cv.imshow('rectangles only', imcopy)
cv.waitKey(0)
cv.destroyAllWindows()

cv.imwrite('../images/shapes-test.png', imcopy)



