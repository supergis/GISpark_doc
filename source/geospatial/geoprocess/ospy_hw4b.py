import os, sys, utils

use_numeric = True

try:
  from osgeo import ogr, gdal
  from osgeo.gdalconst import *
  import numpy
  os.chdir('/Volumes/MacA/Data/Classes/Python/data/')
  use_numeric = False
except ImportError:
  import ogr, gdal
  from gdalconst import *
  import Numeric
  os.chdir(r'Z:\Data\Classes\Python\data')

# register all of the GDAL drivers
gdal.AllRegister()

# open the image
ds = gdal.Open('aster.img', GA_ReadOnly)
if ds is None:
  print 'Could not open aster.img'
  sys.exit(1)

# get image size
rows = ds.RasterYSize
cols = ds.RasterXSize
bands = ds.RasterCount

# get the band and block sizes
band = ds.GetRasterBand(1)
blockSizes = utils.GetBlockSize(band)
xBlockSize = blockSizes[0]
yBlockSize = blockSizes[1]

# initialize variables
count = 0
total = 0

# loop through the rows
for i in range(0, rows, yBlockSize):
  if i + yBlockSize < rows:
    numRows = yBlockSize
  else:
    numRows = rows - i

  # loop through the columns
  for j in range(0, cols, xBlockSize):
    if j + xBlockSize < cols:
      numCols = xBlockSize
    else:
      numCols = cols - j

    # read the data and do the calculations
    if use_numeric:
      data = band.ReadAsArray(j, i, numCols, numRows).astype(Numeric.Float)
      mask = Numeric.greater(data, 0)
      count = count + Numeric.sum(Numeric.sum(mask))
      total = total + Numeric.sum(Numeric.sum(data))
    else:
      data = band.ReadAsArray(j, i, numCols, numRows).astype(numpy.float)
      mask = numpy.greater(data, 0)
      count = count + numpy.sum(numpy.sum(mask))
      total = total + numpy.sum(numpy.sum(data))

# print results
print 'Ignoring 0:', total / count
print 'Including 0:', total / (rows * cols)
