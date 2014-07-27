import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict

def show_image(img, label='image'):
	cv.imshow(label, img)
	cv.waitKey(0)

# smoothing using filter
def smooth(img, filter_type):
	if filter_type == "mean":
		return cv.blur(img, (5,5))
	if filter_type == "gaussian":
		return cv.GaussianBlur(img, (5,5), 0)
	if filter_type == "median":
		return cv.medianBlur(img, 5)
	if filter_type == "bilateral":
		return cv.bilateralFilter(img, 9, 75, 75)
	return bilateral_filter

# return the mode pixel of the image
def get_mode(img, xdim, ydim):
	# split into color channels
	[B,G,R] = cv.split(img)
	blue = B.astype(float)
	green = G.astype(float)
	red = R.astype(float)
  	
  	# count the number of times each triple shows up
	d = defaultdict(int)
	for i in xrange(xdim):
		for j in xrange(ydim):
			d[(B[i,j], G[i,j], R[i,j])] += 1

	# return the triple which shows up most often
	maxval = 0
	returnval = (0,0,0)
	for k,v in d.items():
		if v > maxval:
			returnval = k
			maxval = v
	return returnval

def plot_histogram(img):
  color = ('b','g','r')
  for i,col in enumerate(color):
      histr = cv.calcHist([img],[i],None,[256],[0,256])
      plt.plot(histr,color = col)
      plt.xlim([0,256])
  plt.show()