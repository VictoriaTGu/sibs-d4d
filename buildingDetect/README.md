# Satellite Image-Based Sampling Project
The goal of this project is to detect buildings from satellite imagery of rural/semi-rural areas in Africa. Our current data source is taking screen shots from Google Maps, so the resolution is poor. However, we are looking into getting satellite imagery grants for research purposes.

# Outline of workflow:
1. Download a single satellite image (currently by taking screen shots from Google Maps)
2. Image Preprocessing: Bilateral Filter (blurs the image while keeping the edges sharp)
3. 

# Progress from 2014 spring semester:

Summary: We set up a simple workflow for image preprocessing (bilateral filter) and segmentation followed by rectangle detection. It is evident that many trees are still being picked up by rectangle detection, so next steps are to work on vegetation/road detection and masking, as well as postprocessing (extracting the building latitude/longitude coordinates)

* `testSimpleCV.py`: Tests with SimpleCV (a simplified version of OpenCV). Moving forward, we decided to work with OpenCV instead because it has more libraries and functionality built in.
* `simpleRectDetect.py`: Simple test to verify that rectangle detection works on a set of colored shapes
* `segmentColor.py`: Pre-processing (bilateral filter) followed by segmentation (mean shift), which aims to separate the houses and trees by taking advantage of color invariants.
* 'rectDetect.py': Uses the same test from `simpleRectDetect.py` on the segmented image. It finds contours, fits polygons to it, and then excludes polygons that are not 4-sided or are smaller than a certain threshold.

----------------------------

# Progress from summer 2014:

* `replaceVegetation.py`: Turning vegetation pixels into background pixels
1. Convert the image to grayscale.
2. Threshold the image to produce a black and white image, where the black is vegetation (in our test images, vegetation is a much darker color than the buildings so will be picked up as foreground).
3. Remove noise using erosion (so we're confident that what's left is indeed foreground).
4. Go through the original image and replace the vegetation pixels with the mode pixel of the image (essentially turning vegetation into background).

* `segmentColor.py`: Use color invariants to turn roads into background and turn the buildings black so they appear in the foreground.
1. Plot a histogram of the RGB channels (after turning the vegetation into background, you see very distinct peaks in the histogram, making it easier to isolate the different elements)
2. Threshold the pixels to segment into road and buildings (for the road, red value is greater than two standard deviations from its mean; for the houses, blue value is greater than one standard deviation from its mean)
3. Turn the road pixels into background and building pixels into foreground.

* `rectDetect.py`: Same as before except it allows for polygons with between 3-5 sides, and changed the minimum area threshold.
