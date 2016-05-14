from osgeo import ogr #won't work in the lab
import ogr

driver = GetDriverByName('Shapefile') #missing module name
driver = ogr.GetDriverByName('Shapefile') #wrong driver name
driver = ogr.GetDriverByName('ESRI Shapefile')
driver

os.chdir('f:/data/classes/python/data') #forgot to import os
import os
os.chdir('f:/data/classes/python/data')

ds = driver.Open('sites', 0) #missing file extension
ds #should be empty
print ds #should be none
ds = driver.Open('sites.shp', 0)
ds

layer = ds.GetLayer(1) #no layer at index 1
layer = ds.GetLayer(0)
layer
layer = ds.GetLayer() #equivalent to passing 0
layer

n = layer.GetFeatureCount()
print 'feature count: ' + n #won't work because n is a number
print 'feature count: ' + str(n)
print 'feature count:', n

extent = layer.GetExtent()
print 'extent:', extent
print 'ul:', extent[0], extent[3]
print 'lr:', extent[1], extent[2]

feat = layer.GetFeature(45) #out of range
feat = layer.GetFeature(42) #out of range
feat = layer.GetFeature(41)
feat.GetField('id')
feat = layer.GetFeature(0)
feat.GetField('id') #should be a different id

feat = layer.GetNextFeature()
feat.GetField('id') #what will it print?
while feat:
...   print feat.GetField('id')
...   feat.Destroy()
...   feat = layer.GetNextFeature() #what happens if I forget this?
...

print feat
feat = layer.GetNextFeature() #will this work?
print feat
layer.ResetReading()
feat = layer.GetNextFeature()
print feat
feat.GetField('id') #what id will this be?

geom = feat.GetGeometryRef()
geom.GetX()
geom.GetY()
print geom

###############################################################################

ds2 = driver.CreateDataSource('test.shp') #won't work because it exists (SHOW)
driver.DeleteDataSource('test.shp') #show that file is gone
ds2 = driver.CreateDataSource('test.shp') #show that file isn't there even though it worked

layer2 = ds2.CreateLayer('test', geom_type=wkbPoint) #doesn't work
layer2 = ds2.CreateLayer('test', geom_type=ogr.wkbPoint) #file exists on disk now, can't open in ESRI

fieldDefn = feat.GetFieldDefnRef('id')
fieldDefn.GetName()
fieldDefn.GetType() #show that it matches what is in OGR summary

layer2.CreateField(fieldDefn)
ds2.Destroy() #show that it loads in ESRI but is empty

ds2 = driver.Open('test.shp', 1) #point out the 1
layer2 = ds2.GetLayer()
featDefn = layer2.GetLayerDefn() #why do we have to be sure to use layer2? different number of fields
feat2 = ogr.Feature(featDefn)

feat2.SetGeometry(geom)
feat2.SetField('id', feat.GetField('id'))
layer2.CreateFeature(feat)
ds2.Destroy() #does it show up in ESRI?

