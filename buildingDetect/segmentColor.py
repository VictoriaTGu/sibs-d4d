import cv2 as cv
#import pymeanshift as ms
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict

fname = '../images/chibombo1-veg-subtract.png'

def show_image(img, label='image'):
  cv.imshow(label, img)
  cv.waitKey(0)

def vegetationMask(im, xdim, ydim):
  # compute color invariant
  [B,G,R] = cv.split(im)
  red = R.astype(float)
  blue = B.astype(float)
  green = G.astype(float)

  colInvarIm = np.zeros(shape=(xdim, ydim))

  # iterate over the image
  for i in xrange(xdim):
    for j in xrange(ydim):
      # if there are no blue or green at thix pixel, turn it black
      if (green[i,j] + blue[i,j]) < np.finfo(float).eps:
        colInvarIm[i,j] = 2
      else:
        if blue[i,j] > 130 and blue[i,j] < 150:
          im[i,j] = blue[i,j] #(4./np.pi)*np.arctan((blue[i,j] - green[i,j])/(green[i,j] + blue[i,j]))
        else:
          im[i,j] = 2

  show_image(im, 'blue threshold')
  # normalize to [0,255]
  colInvarIm += abs(colInvarIm.min())
  colInvarIm *= 255.0/colInvarIm.max()
  colInvarIm = colInvarIm.astype('uint8')

  # threshold to detect vegetation
  thresh, vegetation = cv.threshold(colInvarIm, 0, 255, cv.THRESH_OTSU)

  cv.imshow('color invariant image', colInvarIm)
  cv.waitKey(0)
  cv.imshow('vegetation', vegetation)
  cv.waitKey(0)
  #cv.destroyAllWindows()

  cinvar_fname = fname[:-4] + '-col-invar.png'
  #cv.imwrite(cinvar_fname, colInvarIm)
  mask_fname = fname[:-4] + '-veg-mask.png'
  #cv.imwrite(mask_fname, vegetation)

  return vegetation

def plotHistogram(img):
  color = ('b','g','r')
  for i,col in enumerate(color):
      histr = cv.calcHist([img],[i],None,[256],[0,256])
      plt.plot(histr,color = col)
      plt.xlim([0,256])
  plt.show()

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
  im = cv.imread(fname, cv.CV_LOAD_IMAGE_COLOR)


  xdim, ydim, nchannels = im.shape
  im = cv.bilateralFilter(im, 15, 41, 41)

  plotHistogram(im)

  cv.imshow('image', im)
  cv.waitKey(0)

  [B,G,R] = cv.split(im)
  red = R.astype(float)
  blue = B.astype(float)
  green = G.astype(float)
  r = []
  b = []

  median_pixel = get_median(im, xdim, ydim)

  lst = []
  for i in xrange(xdim):
    for j in xrange(ydim):
      b.append(blue[i,j])
      r.append(red[i,j])
      # road: 2 std
      if red[i,j] > 235: # red[i,j] > 180
        im[i,j] = median_pixel # (255, 255, 255)
      # blue: 1 std
      elif blue[i,j] > 182: #and blue[i,j] <= 238:
        im[i,j] = (0,0,0)
  print np.median(r)
  print np.mean(r)
  print np.std(r)
  print np.median(b)
  print np.mean(b)
  print np.std(b)
           #(4./np.pi)*np.arctan((blue[i,j] - green[i,j])/(green[i,j] + blue[i,j]))
  show_image(im, 'red threshold')

  mask_fname = fname[:-4] + '-veg-mask.png'
  cv.imwrite(mask_fname, im)

  #seg, labels, num_regions = ms.segment(im, spatial_radius=6, range_radius=4.5, min_density=50)
  #seg2 = np.copy(seg)

  #veg = vegetationMask(im, xdim, ydim)

  #hists = np.bincount(np.reshape(labels, xdim*ydim))
  #hmean = np.mean(hists)
  #hstd = np.std(hists)

  #for i in xrange(num_regions):
  #  if hists[i] < 15 or hists[i] > 2*hstd + hmean:
  #    seg2[labels == i, :] = 0


  
  #cv.imshow('segmented1', seg)
  #cv.waitKey(0)

  #fout = fname[:-4] + '-seg.png'
  #cv.imwrite(fout, seg)

if __name__ == '__main__':
  main()
