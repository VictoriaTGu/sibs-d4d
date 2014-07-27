#!/usr/bin/env python
import cv2 as cv
import utils
import detectvegetation
import segmentcolor
import detectpolygon

def main():
	fname = '../images/original/chibombo1.png'
	original = cv.imread(fname)
	utils.show_image(original, 'original')
	img = utils.smooth(original, 'bilateral')
	utils.show_image(img, 'bilateral filter')

	# get image dimensions
	xdim, ydim, nchannels = img.shape

	veg_to_background = detectvegetation.detect(img, xdim, ydim)

	segmented = segmentcolor.mask(veg_to_background, xdim, ydim)

	detect = detectpolygon.detect(segmented, original, xdim, ydim)

if __name__ == "__main__":
	main()