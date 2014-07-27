import cv2 as cv
import numpy as np
import utils

# thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
# WINDOW_NAME = "win"

def detect(segmented, original, xdim, ydim):

  # morphological opening and closing
  kernel = np.ones((3,3), np.uint8)
  img = cv.morphologyEx(segmented, cv.MORPH_OPEN, kernel)
  img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

  utils.show_image(img, 'open-close')

  imgcopy = img.copy()
  gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

  num_buildings = 0

  for i in xrange(255):
    # threshold the grayscale image at that value
    binary = np.zeros((xdim, ydim), np.uint8)
    ret, binary = cv.threshold(gray, dst=binary, thresh=i, maxval=255, type=cv.THRESH_OTSU)
    #binary[gray == i] = 255
    # utils.show_image(binary, 'binary')

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

      if polyarea > 30 and carea > 30:
        cv.drawContours(img, [c], 0, (0,0,255), 1)
      if len(poly) < 6 and carea > 100: #and carea > 5: #\
          #and abs(polyarea/carea - 1) < 0.25:
        num_buildings += 1
        cv.drawContours(imgcopy, [poly], 0, (0,0,255), 1)
        cv.drawContours(original, [poly], 0, (0,0,255), 1)

  # show images
  utils.show_image(img, 'all bounding boxes')
  utils.show_image(imgcopy, 'with some filtering')
  utils.show_image(original, 'onto original')
  print num_buildings
  return original

  


