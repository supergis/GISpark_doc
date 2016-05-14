# import modules
import ogr, os, sys

# set the working directory
os.chdir('f:/data/classes/python/data')

# open the output text file for writing
file = open('hw1a.txt', 'w')

# get the shapefile driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# open the data source
datasource = driver.Open('sites.shp', 0)
if datasource is None:
  print 'Could not open file'
  sys.exit(1)

# get the data layer
layer = datasource.GetLayer()

# loop through the features in the layer
feature = layer.GetNextFeature()
while feature:

  # get the attributes
  id = feature.GetFieldAsString('id')
  cover = feature.GetFieldAsString('cover')

  # get the x,y coordinates for the point
  geom = feature.GetGeometryRef()
  x = str(geom.GetX())
  y = str(geom.GetY())

  # write info out to the text file
  file.write(id + ' ' + x + ' ' + y + ' ' + cover + '\n')

  # destroy the feature and get a new one
  feature.Destroy()
  feature = layer.GetNextFeature()

# close the data source and text file
datasource.Destroy()
file.close()
