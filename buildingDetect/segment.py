import cv2 as cv
#import pymeanshift as ms
import numpy as np

fname = '../images/chibombo3.png'

def vegetationMask(im, xdim, ydim):
  # compute color invariant
  [R,G,B] = cv.split(im)
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
  #cv.destroyAllWindows()

  cinvar_fname = fname[:-4] + '-col-invar.png'
  #cv.imwrite(cinvar_fname, colInvarIm)
  mask_fname = fname[:-4] + '-veg-mask.png'
  #cv.imwrite(mask_fname, vegetation)

  return vegetation

def main():
  im = cv.imread(fname, cv.CV_LOAD_IMAGE_COLOR)

  xdim, ydim, nchannels = im.shape
  im = cv.bilateralFilter(im, 15, 41, 41)

  cv.imshow('image', im)
  cv.waitKey(0)

  #seg, labels, num_regions = ms.segment(im, spatial_radius=6, range_radius=4.5, min_density=50)
  #seg2 = np.copy(seg)

  veg = vegetationMask(im, xdim, ydim)

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
