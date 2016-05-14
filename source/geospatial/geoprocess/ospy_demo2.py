import ogr

pt = ogr.Geometry(ogr.wkbPoint) #create a point
print pt
pt.AddPoint(5,10)
print pt
pt.AddPoint(15,10,2) #change the point coords
print pt

>>> line = ogr.Geometry(ogr.wkbLineString) #create a line
print line
line.AddPoint(5,10)
line.AddPoint(15,20)
line.AddPoint(20,30)
print line
line.SetPoint(2,25,30) #change coords for the third vertex
print line
line.GetPointCount() #get number of vertices in the line
line.GetX(1) #get x for second vertex
line.GetY(2) #get y for third vertex

ring = ogr.Geometry(ogr.wkbLinearRing) #create a ring
print ring
ring.AddPoint(0,0)
ring.AddPoint(100,0)
ring.AddPoint(100,100)
ring.AddPoint(0,100)
ring.AddPoint(0,0) #close the ring
print ring
poly = ogr.Geometry(ogr.wkbPolygon) #create a polygon
poly.AddGeometry(ring)
print poly
poly.GetGeometryCount()

ring2 = ogr.Geometry(ogr.wkbLinearRing) #create another ring
ring2.AddPoint(25,25)
ring2.AddPoint(75,25)
ring2.AddPoint(75,75)
ring2.AddPoint(25,75)
ring2.CloseRings() #close the ring
print ring2
poly.AddGeometry(ring2) #add a second ring to the polygon
print poly
poly.GetGeometryCount() #now it should say there are 2

ring3 = poly.GetGeometryRef(1) #get the second ring in the polygon
print ring3
ring3.GetPointCount() #"extra" vertex because first and last are the same
ring3.GetX(0) #get x for the first vertex
ring3.GetY(3) #get y for the fourth vertex

line = 'test:1 2,5 6,3 3,1 2' #homework example
tmp = line.split(':')
tmp
name = tmp[0]
name
coords = tmp[1]
coords
coordlist = coords.split(',')
coordlist
coord = coordlist[0]
coord
xy = coord.split()
xy
xy[0]
xy[1]
float(xy[1])

################################################################################

driver = ogr.GetDriverByName('ESRI Shapefile')
ds = driver.Open(r'F:\Data\Classes\Python\data\sites.shp')
layer = ds.GetLayer()
sr = layer.GetSpatialRef() #UTM 12N WGS84
sr
print sr #prints as Pretty WKT
sr.ExportToWkt()
sr.ExportToPrettyWkt() #notice the newline characters
print sr.ExportToPrettyWkt()
sr.ExportToProj4()
sr.ExportToPCI()
sr.ExportToUSGS()
sr.ExportToXML() #more newline chars
print sr.ExportToXML()

sr2 = osr.SpatialReference() #osr isn't imported yet
import osr
sr2 = osr.SpatialReference()
print sr2 #empty
sr2.ImportFromEPSG(4326) #unprojected WGS84
print sr2
ct = osr.CoordinateTransformation(sr, sr2) #create coordinate transform to go from UTM to geo
ct
feature = layer.GetFeature(0)
geom = feature.GetGeometryRef()
print geom #point coords in UTM
geom.Transform(ct)
print geom #unprojected point coords

#ESRI stuff is only different sometimes
print sr.ExportToPrettyWkt()
sr.MorphToESRI()
print sr.ExportToPrettyWkt() #should look about the same

print sr2.ExportToPrettyWkt()
sr2.MorphToESRI()
print sr2.ExportToPrettyWkt() #should look different
