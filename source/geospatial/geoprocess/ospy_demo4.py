gdalinfo --formats

python
import os
os.chdir(r'Z:\Data\Classes\Python\data')
import gdal

import gdalconst
print gdalconst.GA_ReadOnly
print GA_ReadOnly #not defined
from gdalconst import *
print GA_ReadOnly #now it works

ds = gdal.Open('aster', GA_ReadOnly) #need file extension
ds = gdal.Open('aster.img', GA_ReadOnly)
ds
cols = ds.RasterXSize() #don't need parentheses
cols = ds.RasterXSize
rows = ds.RasterYSize
bands = ds.RasterCount
print cols, rows, bands

gt = ds.GetGeoTransform()
print gt
#top left x, pixel width, rotation, top left y, rotation, pixel height
#notice pixel height is negative because it's measured from top!
x0 = gt[0]
y0 = gt[3]
pwidth = gt[1]
pheight = gt[5]

#get offsets
xoff = int((447520 - x0) / pwidth)
xoff
yoff = int((4631976 - y0) / pheight)
yoff

band = ds.GetRasterBand(0) #index too small
band = ds.GetRasterBand(4) #index too big
band = ds.GetRasterBand(1) #gets first band
data = band.ReadAsArray(xoff, yoff, 1, 1)
data
print data
data[0]
data[0,0]
data = band.ReadAsArray(xoff, yoff, 5, 5)
print data
data[0] #get first row
data[:2] #get first two rows
data[:,2] #get third column
data[3,2] #get fourth row, third column
data[2,3] #get third row, fourth column
print rows, cols
data = band.ReadAsArray(6000, yoff, 1, 1) #there aren't 6000 columns

data = band.ReadAsArray(0, 0, cols, rows) #read entire image
data[yoff, xoff] #correct (same value as before - 55)
data[xoff, yoff] #wrong
data[6000, 300] #there aren't 6000 rows

#######################################################################

import Numeric
a = Numeric.array([0, 4, 3, 0, 9, 2])
print a
b = a.astype(Numeric.Float16)
print b
mask = Numeric.greater(a, 5)
print mask
mask = Numeric.greater(a, 0)
print mask
Numeric.sum(mask)
Numeric.sum(a)
Numeric.sum(b)
18/4 #this is not what we want
18.0/4 #this is

c = Numeric.array([a, [3, 2, 0, 1, 7, 0]]) #2d array
print c
print Numeric.sum(c)
print Numeric.sum(Numeric.sum(c))
