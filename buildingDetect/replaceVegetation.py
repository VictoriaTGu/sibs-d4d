import cv2 as cv
import numpy as np
from scipy import stats
from collections import defaultdict

fname = '../images/chibombo1.png'

def show_image(img, label='image'):
	cv.imshow(label, img)
	cv.waitKey(0)

# smoothing using filter
def smooth(img):
	blur = cv.blur(img, (5,5))
	#show_image(blur, 'Average Blur')
	gaussian_blur = cv.GaussianBlur(img, (5,5), 0)
	#show_image(gaussian_blur, 'Gaussian Blur')
	median_blur = cv.medianBlur(img, 5)
	#show_image(median_blur, 'Median Blur')
	bilateral_filter = cv.bilateralFilter(img, 9, 75, 75)
	show_image(bilateral_filter, 'Bilateral Filter')
	#cv.destroyAllWindows()
	return bilateral_filter

def invert_image(img):
	inverted = (255-img)
	show_image(inverted, 'inverted')
	return inverted

def get_median(img, xdim, ydim):
	[R,G,B] = cv.split(img)
	red = R.astype(float)
  	blue = B.astype(float)
  	green = G.astype(float)
	r, g, b = [], [], []
	pixels = []
	counter=0
	d = defaultdict(int)
	for i in xrange(xdim):
		for j in xrange(ydim):
			d[(R[i,j], G[i,j], B[i,j])] += 1
	print d.values()
	maxval = 0
	returnval = (0,0,0)
	for k,v in d.items():
		if v > maxval:
			returnval = k
			maxval = v
	print maxval
	return returnval

def main():
	original = cv.imread(fname)
	show_image(original, 'original')
	img = smooth(original)
	gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
	show_image(gray, 'gray')
	#cv.imwrite('chibombo1-gray.png', gray)
	ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
	show_image(thresh, 'threshold')

	# noise removal
	kernel = np.ones((3,3),np.uint8)
	opening1 = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel, iterations = 1)
	show_image(opening1, 'opening1')
	opening2 = cv.morphologyEx(thresh,cv.MORPH_OPEN,kernel, iterations = 2)
	show_image(opening2, 'opening2')

	# get image dimensions
	xdim, ydim, nchannels = img.shape

	# get the median pixel value (should be background)
	median_pixel = get_median(img, xdim, ydim)
	print median_pixel
	
	for i in xrange(xdim):
		for j in xrange(ydim):
    		# if it's white in the eroded image, then it's vegetation
			if opening2[i,j] == 255:
    			# set to black
				img[i,j] = (median_pixel[0], median_pixel[1], median_pixel[2])
				
	show_image(opening2, 'bw-overlay')
	show_image(img, 'color-overlay')
	cv.imwrite(fname[:-4] + '-veg-subtract.png', img)
	img = invert_image(img)
	show_image(img, 'inverted')
	#img = invert_image(img)
	#cv.imwrite(fname[:-4] + '-veg-subtract2.png', img)
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


