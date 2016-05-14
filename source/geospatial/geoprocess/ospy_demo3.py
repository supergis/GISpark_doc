import ogr, os
os.chdir(r'Z:\Data\Classes\Python\ospy3\ospy3_data')
driver = ogr.GetDriverByName('ESRI Shapefile')
ptDS = driver.Open('sites.shp', 0)
ptLayer = ptDS.GetLayer()
import tools
tools.printAtts(ptLayer)
ptLayer.SetAttributeFilter("cover = 'trees'") #11 rows, ascending order
tools.printAtts(ptLayer)
ptLayer.SetAttributeFilter("cover = 'shrubs'")
tools.printAtts(ptLayer)
ptLayer.SetAttributeFilter("cover = ''")
tools.printAtts(ptLayer) #nothing
ptLayer.SetAttributeFilter(None)
tools.printAtts(ptLayer) #everything is back

ptLayer.SetSpatialFilterRect(455000, 4610000, 478000, 4640000)
tools.printAtts(ptLayer)
ptLayer.SetAttributeFilter("cover = 'trees'") #apply spatial & att filters at same time
tools.printAtts(ptLayer)
ptLayer.SetSpatialFilter(None) #att filter still in effect
tools.printAtts(ptLayer)
ptLayer.SetAttributeFilter(None)
tools.printAtts(ptLayer) #everything is back

polyDS = driver.Open('cache_towns.shp')
polyLayer = polyDS.GetLayer()
polyFeature = polyLayer.GetFeature(18)
polyFeature.GetField('name')
poly = polyFeature.GetGeometryRef()
ptLayer.SetSpatialFilter(poly)
tools.printAtts(ptLayer) #should just be one
ptLayer.SetSpatialFilter(None)
tools.printAtts(ptLayer) #everything is back

ptLayer.GetName() #make sure we know the name of the layer
result = ptDS.ExecuteSQL("select * from sites where cover = 'trees' order by id desc")
tools.printAtts(result) #11 rows, descending order
ptDS.ReleaseResultSet(result)
result = ptDS.ExecuteSQL("select count(*) from sites where cover = 'trees'")
tools.printAtts(result)
ptDS.ReleaseResultSet(result)
result = ptDS.ExecuteSQL("select distinct cover from sites")
tools.printAtts(result)
ptDS.ReleaseResultSet(result)

ptFeature = ptLayer.GetFeature(0)
pt = ptFeature.GetGeometryRef()
print pt
ptBuffer = pt.Buffer(100)
print ptBuffer #polygon
pt.Equal(poly)
pt.Distance(poly)
poly.Distance(pt) #better be the same as the previous one
poly.GetEnvelope() #extent of the poly


