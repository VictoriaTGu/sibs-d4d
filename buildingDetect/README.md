# Satellite Image-Based Sampling Project
## The goal of this project is to detect buildings from satellite imagery of rural/semi-rural areas in Africa. Our current data source is taking screen shots from Google Maps, so the resolution is poor.

# Outline of workflow:
Basic rectangle detection with OpenCV; tests with SimpleCV (to be discontinued); some preprocessing (bilateral filter) and segmentation (mean shift) tests on images from GMaps


# Progress from 2014 spring semester:

Summary: We set up a simple workflow for image preprocessing (bilateral filter) and segmentation followed by rectangle detection. It is evident that many trees are still being picked up by rectangle detection, so next steps are to work on vegetation/road detection and masking, as well as postprocessing (extracting the building latitude/longitude coordinates)

* `testSimpleCV.py`: Tests with SimpleCV (a simplified version of OpenCV). Moving forward, we decided to work with OpenCV instead because it has more libraries and functionality built in.
* `simpleRectDetect.py`: Simple test to verify that rectangle detection works on a set of colored shapes
* `segmentColor.py`: Pre-processing (bilateral filter) followed by segmentation (mean shift), which aims to separate the houses and trees by taking advantage of color invariants.
* 'rectDetect.py': Uses the same test from `simpleRectDetect.py` on the segmented image. It finds contours, fits polygons to it, and then excludes polygons that are not 4-sided or are smaller than a certain threshold.

----------------------------

# Progress from summer 2014:

* `segmentColor.py`: 
