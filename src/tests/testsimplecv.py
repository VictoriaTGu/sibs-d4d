from SimpleCV import *

img = Image('../images/shapes.png')
# threshold for findBlobs can be adjusted
blobs = img.findBlobsFromWatershed()

drawLayer = DrawingLayer((img.width, img.height))
for b in blobs:
  b.drawMinRect(layer=drawLayer, color=Color.RED, width=3)

img.addDrawingLayer(drawLayer)
img.applyLayers()

img.show()


