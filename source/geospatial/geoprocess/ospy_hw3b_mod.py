# import other modules
import ogr, osr, os, sys

# function to copy fields (not the data) from one layer to another
# parameters:
#   fromLayer: layer object that contains the fields to copy
#   toLayer: layer object to copy the fields into
def copyFields(fromLayer, toLayer):
  featureDefn = fromLayer.GetLayerDefn()
  for i in range(featureDefn.GetFieldCount()):
    toLayer.CreateField(featureDefn.GetFieldDefn(i))

# function to copy attributes from one feature to another
# (this assumes the features have the same attribute fields!)
# parameters:
#   fromFeature: feature object that contains the data to copy
#   toFeature: feature object that the data is to be copied into
def copyAttributes(fromFeature, toFeature):
  for i in range(fromFeature.GetFieldCount()):
    fieldName = fromFeature.GetFieldDefnRef(i).GetName()
    toFeature.SetField(fieldName, fromFeature.GetField(fieldName))

# define the function
def reproject(inFN, inEPSG, outFN, outEPSG):

  # get the shapefile driver
  driver = ogr.GetDriverByName('ESRI Shapefile')

  # create the input SpatialReference
  inSpatialRef = osr.SpatialReference()
  inSpatialRef.ImportFromEPSG(inEPSG)

  # create the output SpatialReference
  outSpatialRef = osr.SpatialReference()
  outSpatialRef.ImportFromEPSG(outEPSG)

  # create the CoordinateTransformation
  coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

  # open the input data source and get the layer
  inDS = driver.Open(inFN, 0)
  if inDS is None:
    print 'Could not open ' + inFN
    sys.exit(1)
  inLayer = inDS.GetLayer()

  # create a new data source and layer
  if os.path.exists(outFN):
    driver.DeleteDataSource(outFN)
  outDS = driver.CreateDataSource(outFN)
  if outDS is None:
    print 'Could not create ' + outFN
    sys.exit(1)
  outLayer = outDS.CreateLayer(os.path.basename(outFN)[:-4],
                               geom_type=inLayer.GetLayerDefn().GetGeomType())

  # copy the fields from the input layer to the output layer
  copyFields(inLayer, outLayer)

  # get the FeatureDefn for the output shapefile
  featureDefn = outLayer.GetLayerDefn()

  # loop through the input features
  inFeature = inLayer.GetNextFeature()
  while inFeature:

    # get the input geometry
    geom = inFeature.GetGeometryRef()

    # reproject the geometry
    geom.Transform(coordTrans)

    # create a new feature
    outFeature = ogr.Feature(featureDefn)

    # set the geometry and attribute
    outFeature.SetGeometry(geom)

    # copy the attributes
    copyAttributes(inFeature, outFeature)

    # add the feature to the shapefile
    outLayer.CreateFeature(outFeature)

    # destroy the features and get the next input feature
    outFeature.Destroy
    inFeature.Destroy
    inFeature = inLayer.GetNextFeature()

  # close the shapefiles
  inDS.Destroy()
  outDS.Destroy()

  # create the *.prj file
  outSpatialRef.MorphToESRI()
  file = open(outFN.replace('.shp', '.prj'), 'w')
  file.write(outSpatialRef.ExportToWkt())
  file.close()
