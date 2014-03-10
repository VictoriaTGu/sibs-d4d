import cv2 as cv
import pymeanshift as ms
import numpy as np

im = cv.imread('../images/chibombo1.png')
cv.imshow('image', im)
cv.waitKey(0)
cv.destroyAllWindows()

im = cv.bilateralFilter(im, 15, 41, 41)
seg, labels, num_regions = ms.segment(im, spatial_radius=6, range_radius=4.5, min_density=50)

cv.imshow('segmented', seg)
cv.waitKey(0)
cv.destroyAllWindows()

cv.imwrite('../images/chibombo1-seg.png', seg)

