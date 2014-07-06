import urllib
import math
from TorCtl import TorCtl
import urllib2
import os
 
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
user_agent = 'Mozilla/5.5 (Windows; U; Windows NT 6.2; it; rv:1.9.1.11) Gecko/20071127 Firefox/2.0.1'
user_agent = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.15 Safari/535.1'
headers={'User-Agent':user_agent}
 
def request(url):
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
    _set_urlproxy()
    try:
      request=urllib2.Request(url, None, headers)
      response = urllib2.urlopen(request)
      data = response.read()
      response.close()
      return data
    except urllib2.HTTPError, e:
      print e
      return
 
def renew_connection():
    conn = TorCtl.connect(controlAddr="127.0.0.1", controlPort=9051, passphrase="your_password")
    conn.send_signal("NEWNYM")
    conn.close()

class Point():
  """Stores a simple (x,y) point.  It is used for storing x/y pixels.

  Attributes:
    x: An int for a x value.
    y: An int for a y value.
  """
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def ToString(self):
    return '(%s, %s)' % (self.x, self.y)
    
  def Equals(self, other):
    if other is None :
      return false
    else:
      return (other.x == self.x and other.y == self.y)

def Bound(value, opt_min, opt_max):
  """Returns value if in min/max, otherwise returns the min/max.

  Args:
    value: The value in question.
    opt_min: The minimum the value can be.
    opt_max: The maximum the value can be.

  Returns:
    An int that is either the value passed in or the min or the max.
  """
  if opt_min is not None:
    value = max(value, opt_min)
  if opt_max is not None:
    value = min(value, opt_max)
  return value

    
def DegreesToRadians(deg):
  return deg * (math.pi / 180)


def CalcCenterFromBounds(bounds):
  """
  Calculates the center point given southwest/northeast lat/lng pairs.

  Given southwest and northeast bounds, this method will return the center

  point.  We use this method when we have done a search for points on the map,

  and we get multiple results.  In the results we don't get anything to

  calculate the center point of the map so this method calculates it for us.


  Args:

    bounds: A list of length 2, each holding a list of length 2. It holds

      the southwest and northeast lat/lng bounds of a map.  It should look

      like this: [[southwestLat, southwestLng], [northeastLat, northeastLng]]


  Returns:

    An dict containing keys lat and lng for the center point.

  """
  north = bounds[1][0]
  south = bounds[0][0]
  east = bounds[1][1]
  west = bounds[0][1]
  center = {}
  center['lat'] = north - float((north - south) / 2)
  center['lng'] = east - float((east - west) / 2)
  return center

def CalcBoundsFromPoints(lst):
  """Calculates the max/min lat/lng in the lists.

  This method takes in a list of lats,lng pairs, and outputs the 
  southwest and northeast bounds for these points 

  Args:
    list of [lat,lng] pairs

  Returns:
    A list of length 2, each holding a list of length 2.  It holds 
    the southwest and northeast lat/lng bounds of a map.  It should look 
    like this: [[southwestLat, southwestLat], [northeastLat, northeastLng]]
  """
  lats = [float(lat) for [lat,lng] in lst]
  lngs = [float(lng) for [lat,lng] in lst]
  flats = map(float,lats)
  flngs = map(float,lngs)
  west = min(flngs)
  east = max(flngs)
  north = max(flats)
  south = min(flats)
  return [[south, west], [north, east]]

# Given the bounds of a rectangle, divide it into a grid
def sample_grid_boundaries(bounds, lat_dimension, lng_dimension):
  [[south, west], [north, east]] = bounds
  # north and west stay the same
  new_south = north - ((north - south) / float(lat_dimension))
  new_east = west + ((east - west) / float(lng_dimension))
  return [[new_south, west], [north, new_east]] 

# helper function for getZoomLevel
def latRad(lat):
  sin = math.sin(lat * math.pi / 180)
  radX2 = math.log((1+sin) / (1-sin)) / 2
  return max([min([radX2, math.pi]), -math.pi]) / 2

# helper function for getZoomLevel
def zoom(mapPx, worldPx, fraction):
  return math.floor(math.log(mapPx / worldPx / fraction) / math.log(2))

""" 
Returns the highest zoom level that can display the bounds
within a certain size map
Input:
  bounds: [[south, west], [north, east]]
  map_dimensions: {height: y, width: x}
Output:
  zoom_level: int
"""
def getZoomLevel(bounds, map_dimensions):
  [[south, west], [north, east]] = bounds
  WORLD_DIM = { 'height': 256, 'width': 256 }
  ZOOM_MAX = 20
  latFraction = (latRad(north) - latRad(south)) / math.pi
  lngDiff = east - west
  lngFraction = 1
  if lngDiff < 0:
    lngFraction = (lngDiff + 360) / 360
  else:
    lngFraction = lngDiff / 360
  latZoom = zoom(map_dimensions['height'], WORLD_DIM['height'], latFraction)
  lngZoom = zoom(map_dimensions['width'], WORLD_DIM['width'], lngFraction)
  return int(min([latZoom, lngZoom, ZOOM_MAX]))
  

def build_image_request(lat, lng, zoom, size): 
  url = "http://maps.googleapis.com/maps/api/staticmap?center="
  url += str(lat) + "," + str(lng)
  url += "&zoom=" + str(zoom)
  url += "&size=" + size
  url += "&sensor=false&maptype=satellite"
  return url


def download_image(image_url, destination_file):
  renew_connection()
  data = request(image_url)
  output = open(destination_file, "wb")
  output.write(data)
  output.close()
  # urllib.urlretrieve(image_url, destination_file)

def main():
  DEFAULT_ZOOM = 19
  DEFAULT_OUTPUT = "/Users/vgu/Dropbox/github/sibs-d4d/images/mturk_input/users/vgu888/chibombo"
  DEFAULT_SIZE = "640x640"
  DEFAULT_MAP_DIMENSIONS = {'height': 640, 'width': 640}
  DEFAULT_NAME = "chib"
  boundaries = [ [ 28.489461899000105, -15.505137443999899 ], [ 28.484674454000015, -15.499405860999957 ], [ 28.452842712000233, -15.497296332999952 ], [ 28.43986511200012, -15.492409705999933 ], [ 28.435997009000062, -15.480487822999919 ], [ 28.433513641000104, -15.466823577999889 ], [ 28.417819977000136, -15.467472075999922 ], [ 28.400384903000145, -15.46986579899982 ], [ 28.395030975000168, -15.469969748999802 ], [ 28.386543274000189, -15.473217963999957 ], [ 28.37479209900016, -15.474472045999903 ], [ 28.363737106000201, -15.475026130999936 ], [ 28.350931168000045, -15.476984023999933 ], [ 28.349323273000152, -15.484215735999896 ], [ 28.348554611000168, -15.496574401999908 ], [ 28.334278107000216, -15.496845244999918 ], [ 28.330713272000196, -15.482509612999877 ], [ 28.327136993000124, -15.482234000999881 ], [ 28.316064835000077, -15.482098578999796 ], [ 28.298177719000194, -15.480717658999822 ], [ 28.300203323000062, -15.490626334999888 ], [ 28.301557541000022, -15.502261161999854 ], [ 28.302520752000078, -15.512532233999877 ], [ 28.297748566000109, -15.521882056999914 ], [ 28.29154777500014, -15.531258582999897 ], [ 28.284946442000091, -15.538927077999858 ], [ 28.276762008999981, -15.540109633999919 ], [ 28.268159866000076, -15.538897513999927 ], [ 28.260637283000221, -15.53800773599994 ], [ 28.251239777000137, -15.533379554999897 ], [ 28.241228104000186, -15.532877921999955 ], [ 28.232269287000122, -15.531669616999864 ], [ 28.230003357000214, -15.526565551999909 ], [ 28.232322693000128, -15.518976211999814 ], [ 28.234266281000146, -15.51070785499985 ], [ 28.233778000000143, -15.505228042999931 ], [ 28.231180191000249, -15.501158713999871 ], [ 28.226627350000058, -15.489921569999922 ], [ 28.218811034999987, -15.476684569999918 ], [ 28.215612411000052, -15.462333678999926 ], [ 28.219026566000139, -15.455755233999923 ], [ 28.226877213000193, -15.455613135999954 ], [ 28.232887268000184, -15.453104018999909 ], [ 28.233890533000135, -15.450341224999931 ], [ 28.233005524000191, -15.443154334999917 ], [ 28.230707169000198, -15.436677932999885 ], [ 28.228103638000164, -15.432265281999946 ], [ 28.223899841000048, -15.420678138999904 ], [ 28.223863602000165, -15.404213904999949 ], [ 28.223154068000099, -15.389475821999952 ], [ 28.221771240000066, -15.376465796999923 ], [ 28.227947235000102, -15.36606597899987 ], [ 28.239568710000015, -15.342790603999902 ], [ 28.249876022000194, -15.343037604999836 ], [ 28.251935959000207, -15.324822425999855 ], [ 28.260007858000108, -15.319190978999927 ], [ 28.288148880000051, -15.317314147999809 ], [ 28.313667297000165, -15.310336112999948 ], [ 28.310504913000159, -15.297704696999915 ], [ 28.309583664000058, -15.296677588999955 ], [ 28.324911118000102, -15.303272246999882 ], [ 28.343538284000147, -15.306360244999951 ], [ 28.346521378000034, -15.326192855999921 ], [ 28.353801727000189, -15.346631049999871 ], [ 28.363693237000064, -15.357075690999864 ], [ 28.374691010000049, -15.354470252999931 ], [ 28.39023971600011, -15.348349570999858 ], [ 28.404312134000065, -15.354597091999949 ], [ 28.406978606999985, -15.361403464999853 ], [ 28.406671524000103, -15.392263411999863 ], [ 28.414426804000129, -15.402743339999859 ], [ 28.426013947000058, -15.409377097999936 ], [ 28.442977905000191, -15.416933059999906 ], [ 28.459213257000215, -15.423814773999823 ], [ 28.466701508000142, -15.437722205999876 ], [ 28.480686188000107, -15.440188407999926 ], [ 28.492902756000149, -15.443373679999866 ], [ 28.513345718000153, -15.44707870499974 ], [ 28.505971909000152, -15.466076850999912 ], [ 28.489461899000105, -15.505137443999899 ] ]
  boundaries_rev = [[lat,lng] for [lng,lat] in boundaries]
  original_bounds = CalcBoundsFromPoints(boundaries_rev) 

  dimension = 2
  zoom_level = 1
  
  while zoom_level < 19:
    new_bounds = sample_grid_boundaries(original_bounds, dimension, dimension)
    zoom_level = getZoomLevel(new_bounds, DEFAULT_MAP_DIMENSIONS)
    dimension += 1
  
  [[new_south, west], [north, new_east]] = new_bounds
  lat_change = north - new_south
  lng_change = new_east - west
  print lat_change, lng_change
  print dimension

  # get all the satellite image tiles, first vertically then horizontally
  for x in range(dimension):
    for y in range(dimension):
      center = CalcCenterFromBounds(new_bounds)
      image_url = build_image_request(center['lat'], center['lng'], zoom_level, DEFAULT_SIZE)
      fname = DEFAULT_OUTPUT + "/" + DEFAULT_NAME + "_" + str(x) + "_" + str(y) + ".jpg"
      print fname, image_url
      if not os.path.isfile(fname):
        print "downloading..."
        download_image(image_url, fname)
      # shift the north coordinate downward latitudinally
      new_bounds[1][0] -= 1.5*lat_change
      print "north " + str(new_bounds[1][0])
    # shift the west coordinate to the right (east) longitudinally
    new_bounds[0][1] += lng_change
    # reset the north bounding latitude
    new_bounds[1][0] = north
    print "east " + str(new_bounds[0][1])

if __name__ == "__main__":
  main()
