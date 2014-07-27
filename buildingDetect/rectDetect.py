import cv2 as cv
import numpy as np

fname = '../images/chibombo1.png'
fseg = fname[:-4] + '-veg-subtract-veg-mask.png'

def show_image(img, label='image'):
  cv.imshow(label, img)
  cv.waitKey(0)

# load color image and segmentation
orig = cv.imread(fname)
im = cv.imread(fseg)
xdim, ydim, nchannels = im.shape

show_image(orig, 'orig')
show_image(im, 'veg-mask')

# morphological opening and closing
kernel = np.ones((3,3), np.uint8)
im = cv.morphologyEx(im, cv.MORPH_OPEN, kernel)
im = cv.morphologyEx(im, cv.MORPH_CLOSE, kernel)

show_image(im, 'open-close')

imcopy = im.copy()
gray = cv.cvtColor(im, cv.COLOR_RGB2GRAY)
#thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
WINDOW_NAME = "win"



num_buildings = 0

for i in xrange(255):
  # threshold the grayscale image at that value
  binary = np.zeros((xdim, ydim), np.uint8)
  ret, binary = cv.threshold(gray, dst=binary, thresh=i, maxval=255, type=cv.THRESH_OTSU)
  #binary[gray == i] = 255
  #show_image(binary, 'binary')

  # find contours, fit to polygon, and determine if rectangular
  contours, hierarchy = cv.findContours(binary, mode=cv.RETR_LIST, method=cv.CHAIN_APPROX_SIMPLE)

  for c in contours:
    #print str(i) + "th round, " + str(len(c)) + " contours"
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
      cv.drawContours(im, [c], 0, (0,0,255), 1)
    if len(poly) < 6 and carea > 30: #and carea > 5: #\
        #and abs(polyarea/carea - 1) < 0.25:
      num_buildings += 1
      cv.drawContours(imcopy, [poly], 0, (0,0,255), 1)
      cv.drawContours(orig, [poly], 0, (0,0,255), 1)

# show images
cv.imshow('all bounding boxes', im)
cv.waitKey(0)

cv.imshow('with some filtering', imcopy)
cv.waitKey(0)
cv.destroyAllWindows()

show_image(orig)

fout = fname[:-4] + '-detect.png'
cv.imwrite(fout, orig)

print num_buildings


