# import modules
import ogr, os, sys

# set the working directory
os.chdir('z:/data/classes/python/data')

# get the shapefile driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# open sites.shp and get the layer
sitesDS = driver.Open('sites.shp', 0)
if sitesDS is None:
  print 'Could not open sites.shp'
  sys.exit(1)
sitesLayer = sitesDS.GetLayer()

# open cache_towns.shp and get the layer
townsDS = driver.Open('cache_towns.shp', 0)
if townsDS is None:
  print 'Could not open cache_towns.shp'
  sys.exit(1)
townsLayer = townsDS.GetLayer()

# use an attribute filter to restrict cache_towns.shp to "Nibley"
townsLayer.SetAttributeFilter("NAME = 'Nibley'")

# get the Nibley geometry and buffer it by 1500
nibleyFeature = townsLayer.GetFeature(0)
nibleyGeom = nibleyFeature.GetGeometryRef()
bufferGeom = nibleyGeom.Buffer(1500)

# use bufferGeom as a spatial filter on sites.shp to get all sites
# within 1500 meters of Nibley
sitesLayer.SetSpatialFilter(bufferGeom)

# loop through the remaining features in sites.shp and print their
# id values
siteFeature = sitesLayer.GetNextFeature()
while siteFeature:
  print siteFeature.GetField('ID')
  siteFeature.Destroy()
  siteFeature = sitesLayer.GetNextFeature()

# close the shapefiles
sitesDS.Destroy()
townsDS.Destroy()
