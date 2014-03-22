import cv2 as cv
import pymeanshift as ms
import numpy as np


def vegetationMask(im, xdim, ydim):
  # compute color invariant
  [R,G,B] = cv.split(im)
  blue = B.astype(float)
  green = G.astype(float)

  colInvarIm = np.zeros(shape=(xdim, ydim))

  for i in xrange(xdim):
    for j in xrange(ydim):
      if (green[i,j] + blue[i,j]) < np.finfo(float).eps:
        colInvarIm[i,j] = 2
      else:
        colInvarIm[i,j] = (4./np.pi)*np.arctan((green[i,j] - blue[i,j])/(green[i,j] + blue[i,j]))

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
  cv.destroyAllWindows()

  return vegetation

def main():
  im = cv.imread('../images/chibombo1.png', cv.CV_LOAD_IMAGE_COLOR)
  xdim, ydim, nchannels = im.shape
  im = cv.bilateralFilter(im, 15, 41, 41)

  seg, labels, num_regions = ms.segment(im, spatial_radius=6, range_radius=4.5, min_density=100)
  seg2 = np.copy(seg)

  hists = np.bincount(np.reshape(labels, xdim*ydim))
  hmean = np.mean(hists)
  hstd = np.std(hists)
  print hmean

  for i in xrange(num_regions):
    if hists[i] < 15 or hists[i] > 2*hstd + hmean:
      seg2[labels == i, :] = 0


  cv.imshow('image', im)
  cv.waitKey(0)
  cv.imshow('segmented1', seg)
  cv.waitKey(0)

  cv.imshow('segmented2', seg2)
  cv.waitKey(0)
  cv.destroyAllWindows()

  cv.imwrite('../images/chibombo1-seg.png', seg)

if __name__ == '__main__':
  main()
