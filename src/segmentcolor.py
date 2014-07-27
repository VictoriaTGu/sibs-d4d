import cv2 as cv
#import pymeanshift as ms
import numpy as np
from matplotlib import pyplot as plt
import utils

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

def mask(img, xdim, ydim):

  utils.plot_histogram(img)

  [B,G,R] = cv.split(img)
  blue = B.astype(float)
  green = G.astype(float)
  red = R.astype(float)

  meanR = np.mean(red)
  stdR = np.std(red)
  print meanR + 1.6 * stdR
  meanB = np.mean(blue)
  stdB = np.std(blue)
  print meanB + 1.1 * stdB

  mode_pixel = utils.get_mode(img, xdim, ydim)

  # separate into roads and houses
  for i in xrange(xdim):
    for j in xrange(ydim):
      # road: red value is at least 2 std above the mean
      if red[i,j] > meanR + 1.6 * stdR: # red[i,j] > 180
        img[i,j] = mode_pixel
      # houses: blue value is at least 1 std above the mean
      if blue[i,j] > meanB + 1.1 * stdB: # 182: #and blue[i,j] <= 238:
        img[i,j] = (0,0,0)

  utils.show_image(img, 'mask')

  return img

  #seg, labels, num_regions = \
    # ms.segment(im, spatial_radius=6, range_radius=4.5, min_density=50)
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
