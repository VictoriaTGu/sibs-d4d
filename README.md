# Satellite Image-Based Sampling Project
The goal of this project is to detect buildings from satellite imagery of rural/semi-rural areas in Africa. Our current data source is taking screen shots from Google Maps, so the resolution is poor. However, we are looking into getting satellite imagery grants for research purposes.

# Outline of workflow:
1. Download a single satellite image (currently by taking screen shots from Google Maps)
2. Image Preprocessing: Bilateral Filter (blurs the image while keeping the edges sharp)
3. Detect vegetation and set vegetation pixels to background
4. Segment image using color invariants
5. Perform rectangle detection for buildings
6. Extract lat/lng coordinates of buildings (TODO)

# Progress from 2014 Spring Semester:

Summary: We set up a simple workflow for image preprocessing (bilateral filter) and segmentation followed by rectangle detection. It is evident that many trees are still being picked up by rectangle detection.

Next steps: Work on vegetation/road detection and masking, as well as postprocessing (extracting the building latitude/longitude coordinates)

* `segmentColor.py`: Pre-processing (bilateral filter) followed by segmentation (mean shift), which aims to separate the houses and trees by taking advantage of color invariants. 
  - [Chibombo 2 Original](https://github.com/vgu888/sibs-d4d/tree/master/images/original/chibombo2.png)
  - [Chibombo 2 Segment](https://github.com/vgu888/sibs-d4d/tree/master/images/spring2014/chibombo2-seg.png)
* In `segmentColor.py`: First attempt at detecting vegetation using color invariants (fails to exclude buildings) and then thresholding it:
  - [Chibombo 2 Color Invariants](https://github.com/vgu888/sibs-d4d/tree/master/images/spring2014/chibombo2-col-invar.png)
  - [Chibombo 2 Vegetation Detection](https://github.com/vgu888/sibs-d4d/tree/master/images/spring2014/chibombo2-veg-mask.png)
* `simpleRectDetect.py`: Simple test to verify that rectangle detection works on a set of colored shapes. 
  - [Shapes test](https://github.com/vgu888/sibs-d4d/tree/master/images/spring2014/shapes-test.png)
* `rectDetect.py`: Uses the same test from `simpleRectDetect.py` on the segmented image. It finds contours, fits polygons to it, and then excludes polygons that are not 4-sided or are smaller than a certain threshold.
  - [Chibombo 2 Detect](https://github.com/vgu888/sibs-d4d/tree/master/images/spring2014/chibombo2-detect.png)

* `testSimpleCV.py`: Tests with SimpleCV (a simplified version of OpenCV). Moving forward, we decided to work with OpenCV instead because it has more libraries and functionality built in. 

----------------------------

# Progress from Summer 2014:

Summary: We continued working on vegetation detection and were successful in turning vegetation pixels into background. Afterwards, we use color invariants to detect roads and turn road pixels into background. Finally, we bring the buildings into the foreground and perform rectangle detection. This workflow is successful at excluding vegetation from building detection, and right now detection is over-sensitive, which is what we were aiming for. 

Next steps: Obtain training data to refine and test the algorithms and their parameters.

* `replaceVegetation.py`: Turning vegetation pixels into background pixels
  1. Convert the image to grayscale.
  2. Threshold the image to produce a black and white image, where the black is vegetation (in our test images, vegetation is a much darker color than the buildings so will be picked up as foreground).
  3. Remove noise using erosion (so we're confident that what's left is indeed foreground).
  4. Go through the original image and replace the vegetation pixels with the mode pixel of the image (essentially turning vegetation into background).
    - [Chibombo 1 Detect and Replace Vegetation](https://github.com/vgu888/sibs-d4d/tree/master/images/summer2014/chibombo1-replace-veg.png)
    - [Chibombo 1 Replace Vegetation Final Result](https://github.com/vgu888/sibs-d4d/tree/master/images/summer2014/chibombo1-veg-subtract.png)

* `segmentColor.py`: Use color invariants to turn roads into background and turn the building pixels black so that they appear in the foreground.
  1. Plot a histogram of the RGB channels (after turning the vegetation into background, you see very distinct peaks in the histogram, making it easier to isolate the different elements of the picture)
  2. Threshold the pixels to segment them into road and buildings (for the road, red value is greater than two standard deviations from its mean; for the houses, blue value is greater than one standard deviation from its mean)
  3. Turn the road pixels into background and building pixels into foreground.
    - [Chibombo 1 Segmentation and Building Mask](https://github.com/vgu888/sibs-d4d/tree/master/images/summer2014/chibombo1-veg-subtract-veg-mask.png)

* `rectDetect.py`: Same as before except it allows for polygons with between 3-5 sides, and changed the minimum area threshold.
  - [Chibombo 1 Detect](https://github.com/vgu888/sibs-d4d/tree/master/images/summer2014/chibombo1-detect.png)
