import cv2 as cv
import numpy as np

fname = '../images/chibombo1.png'
fseg = fname[:-4] + '-veg-subtract2.png'

# load color image and segmentation
orig = cv.imread(fname)
im = cv.imread(fseg)
xdim, ydim, nchannels = im.shape

# morphological opening and closing
kernel = np.ones((3,3), np.uint8)
im = cv.morphologyEx(im, cv.MORPH_OPEN, kernel)
im = cv.morphologyEx(im, cv.MORPH_CLOSE, kernel)

imcopy = im.copy()
gray = cv.cvtColor(im, cv.COLOR_RGB2GRAY)
#thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
WINDOW_NAME = "win"

cv.imshow('image', orig)
cv.waitKey(0)

num_buildings = 0

for i in xrange(255):
  # threshold the grayscale image at that value
  #ret, binary = cv.threshold(gray, i, 255, cv.THRESH_BINARY)
  binary = np.zeros((xdim, ydim), np.uint8)
  binary[gray == i] = 255

  # find contours, fit to polygon, and determine if rectangular
  contours, hierarchy = cv.findContours(binary, mode=cv.RETR_LIST, method=cv.CHAIN_APPROX_SIMPLE)

  for c in contours:
    poly = cv.approxPolyDP(np.array(c), 0.07*cv.arcLength(c,True), True)
    carea = cv.contourArea(c)
    polyarea = cv.contourArea(poly)
    hull = cv.convexHull(c)
    hullarea = cv.contourArea(hull)

    # bounding box
    rect = cv.minAreaRect(c)
    box = cv.cv.BoxPoints(rect)
    box = np.int0(box)

    if polyarea < 2048 and carea < 2048:
      cv.drawContours(im, [c], 0, (0,0,255), 1)
    if len(poly) == 4 and carea < 2048 and carea > 5 \
        and abs(polyarea/carea - 1) < 0.25:
      num_buildings += 1
      cv.drawContours(imcopy, [poly], 0, (0,0,255), 1)

# show images
cv.imshow('all bounding boxes', im)
cv.waitKey(0)

cv.imshow('with some filtering', imcopy)
cv.waitKey(0)
cv.destroyAllWindows()

fout = fname[:-4] + '-detect.png'
cv.imwrite(fout, imcopy)

print num_buildings


