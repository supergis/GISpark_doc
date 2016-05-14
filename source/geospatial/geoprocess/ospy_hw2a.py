# import modules
import ogr, os, sys

# set the working directory
os.chdir('f:/data/classes/python/data')

# get the shapefile driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# create a new data source and layer
fn = 'hw2a.shp'
if os.path.exists(fn):
  driver.DeleteDataSource(fn)
ds = driver.CreateDataSource(fn)
if ds is None:
  print 'Could not create file'
  sys.exit(1)
layer = ds.CreateLayer('hw2a', geom_type=ogr.wkbPolygon)

# create a field for the county name
fieldDefn = ogr.FieldDefn('name', ogr.OFTString)
fieldDefn.SetWidth(30)

# add the field to the shapefile
layer.CreateField(fieldDefn)

# get the FeatureDefn for the shapefile
featureDefn = layer.GetLayerDefn()

# open the input text file for reading
file = open('ut_counties.txt', 'r')

# loop through the lines in the text file
for line in file:

  # create an empty ring geometry
  ring = ogr.Geometry(ogr.wkbLinearRing)

  # split the line on colons to get county name and a string with coordinates
  tmp = line.split(':')
  name = tmp[0]
  coords = tmp[1]

  # split the coords on commas to get a list of x,y pairs
  coordlist = coords.split(',')

  # loop through the list of coordinates
  for coord in coordlist:

    # split the x,y pair on spaces to get the individual x and y values
    xy = coord.split()
    x = float(xy[0])
    y = float(xy[1])

    # add the vertex to the ring
    ring.AddPoint(x, y)

  # now that we've looped through all of the coordinates, create a polygon
  poly = ogr.Geometry(ogr.wkbPolygon)
  poly.AddGeometry(ring)

  # create a new feature and set its geometry and attribute
  feature = ogr.Feature(featureDefn)
  feature.SetGeometry(poly)
  feature.SetField('name', name)

  # add the feature to the shapefile
  layer.CreateFeature(feature)

  # destroy the geometries and feature
  ring.Destroy()
  poly.Destroy()
  feature.Destroy()

# now that we've looped through the entire text file, close the files
file.close()
ds.Destroy()