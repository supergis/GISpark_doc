# import modules
import ogr, os, sys

# set the working directory
os.chdir('f:/data/classes/python/data')

# get the shapefile driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# open the input data source and get the layer
inDS = driver.Open('sites.shp', 0)
if inDS is None:
  print 'Could not open file'
  sys.exit(1)
inLayer = inDS.GetLayer()

# create a new data source and layer
fn = 'hw1b.shp'
if os.path.exists(fn):
  driver.DeleteDataSource(fn)
outDS = driver.CreateDataSource(fn)
if outDS is None:
  print 'Could not create file'
  sys.exit(1)
outLayer = outDS.CreateLayer('hw1b', geom_type=ogr.wkbPoint)

# get the FieldDefn's for the id and cover fields in the input shapefile
feature = inLayer.GetFeature(0)
idFieldDefn = feature.GetFieldDefnRef('id')
coverFieldDefn = feature.GetFieldDefnRef('cover')

# create new id and cover fields in the output shapefile
outLayer.CreateField(idFieldDefn)
outLayer.CreateField(coverFieldDefn)

# get the FeatureDefn for the output layer
featureDefn = outLayer.GetLayerDefn()

# loop through the input features
inFeature = inLayer.GetNextFeature()
while inFeature:

  # get the cover attribute for the input feature
  cover = inFeature.GetField('cover')

  # check to see if cover == grass
  if cover == 'trees':

    # create a new feature
    outFeature = ogr.Feature(featureDefn)

    # set the geometry
    geom = inFeature.GetGeometryRef()
    outFeature.SetGeometry(geom)

    # set the attributes
    id = inFeature.GetField('id')
    outFeature.SetField('id', id)
    outFeature.SetField('cover', cover)

    # add the feature to the output layer
    outLayer.CreateFeature(outFeature)

    # destroy the output feature
    outFeature.Destroy()

  # destroy the input feature and get a new one
  inFeature.Destroy()
  inFeature = inLayer.GetNextFeature()

# close the data sources
inDS.Destroy()
outDS.Destroy()
