#!/usr/bin/env python

""" Performs vegetation detection on pixels and sets 
    vegetation pixels to background.
"""

import cv2 as cv
import numpy as np
import utils

def detect(img, xdim, ydim):
	# convert to grayscale
	gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
	utils.show_image(gray, 'gray')
	
	# threshold to convert to binary image
	ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
	utils.show_image(thresh, 'threshold')

	# erode image to isolate the sure foreground
	kernel = np.ones((3,3),np.uint8)
	opening = cv.morphologyEx(thresh,cv.MORPH_OPEN, kernel, iterations=3)
	utils.show_image(opening, 'opening')

	# get the median pixel value (should be background)
	mode = utils.get_mode(img, xdim, ydim)
	
	# replace the foreground (trees) with the median pixel
	for i in xrange(xdim):
		for j in xrange(ydim):
    		# if it's white in the eroded image, then it's vegetation
			if opening[i,j] == 255:
    			# set to black
				img[i,j] = mode
				
	utils.show_image(img, 'color-overlay')
	return img
	
	# sure background area
	# sure_bg = cv.dilate(opening2,kernel,iterations=3)
	# show_image(sure_bg, 'sure_bg')

	# Finding sure foreground area
	# dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
	# ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)

	# Finding unknown region
	# sure_fg = np.uint8(sure_fg)
	# unknown = cv.subtract(sure_bg,sure_fg)

if __name__ == "__main__":
	main()


