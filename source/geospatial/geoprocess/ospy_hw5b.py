# homework 5b
# mosaic two images together
import os, sys, gdal
from gdalconst import *

os.chdir('c:/temp/py5')

# register all of the GDAL drivers
gdal.AllRegister()

# read in doq1 and get info about it
ds1 = gdal.Open('doq1.img')
band1 = ds1.GetRasterBand(1)
rows1 = ds1.RasterYSize
cols1 = ds1.RasterXSize

# get the corner coordinates for doq1
transform1 = ds1.GetGeoTransform()
minX1 = transform1[0]
maxY1 = transform1[3]
pixelWidth1 = transform1[1]
pixelHeight1 = transform1[5]
maxX1 = minX1 + (cols1 * pixelWidth1)
minY1 = maxY1 + (rows1 * pixelHeight1)

# read in doq2 and get info about it
ds2 = gdal.Open('doq2.img')
band2 = ds2.GetRasterBand(1)
rows2 = ds2.RasterYSize
cols2 = ds2.RasterXSize

# get the corner coordinates for doq2
transform2 = ds2.GetGeoTransform()
minX2 = transform2[0]
maxY2 = transform2[3]
pixelWidth2 = transform2[1]
pixelHeight2 = transform2[5]
maxX2 = minX2 + (cols2 * pixelWidth2)
minY2 = maxY2 + (rows2 * pixelHeight2)

# get the corner coordinates for the output
minX = min(minX1, minX2)
maxX = max(maxX1, maxX2)
minY = min(minY1, minY2)
maxY = max(maxY1, maxY2)

# get the number of rows and columns for the output
cols = int((maxX - minX) / pixelWidth1)
rows = int((maxY - minY) / abs(pixelHeight1))

# compute the origin (upper left) offset for doq1
xOffset1 = int((minX1 - minX) / pixelWidth1)
yOffset1 = int((maxY1 - maxY) / pixelHeight1)

# compute the origin (upper left) offset for doq2
xOffset2 = int((minX2 - minX) / pixelWidth1)
yOffset2 = int((maxY2 - maxY) / pixelHeight1)

# create the output image
driver = ds1.GetDriver()
dsOut = driver.Create('mosiac.img', cols, rows, 1, band1.DataType)
bandOut = dsOut.GetRasterBand(1)

# read in doq1 and write it to the output
data1 = band1.ReadAsArray(0, 0, cols1, rows1)
bandOut.WriteArray(data1, xOffset1, yOffset1)

# read in doq2 and write it to the output
data2 = band2.ReadAsArray(0, 0, cols2, rows2)
bandOut.WriteArray(data2, xOffset2, yOffset2)

# compute statistics for the output
bandOut.FlushCache()
stats = bandOut.GetStatistics(0, 1)

# set the geotransform and projection on the output
geotransform = [minX, pixelWidth1, 0, maxY, 0, pixelHeight1]
dsOut.SetGeoTransform(geotransform)
dsOut.SetProjection(ds1.GetProjection())

# build pyramids for the output
gdal.SetConfigOption('HFA_USE_RRD', 'YES')
dsOut.BuildOverviews(overviewlist=[2,4,8,16])
