# homework 6b
# high-pass filter using slice notation
import os, sys, Numeric, gdal, time
from gdalconst import *

start = time.time()

os.chdir('c:/temp/py6')

# register all of the GDAL drivers
gdal.AllRegister()

# open the image
inDs = gdal.Open('aster.img', GA_ReadOnly)
if inDs is None:
  print 'Could not open aster.img'
  sys.exit(1)

# get image size
rows = inDs.RasterYSize
cols = inDs.RasterXSize

# read the input data
inBand = inDs.GetRasterBand(1)
inData = inBand.ReadAsArray(0, 0, cols, rows).astype(Numeric.Int)

# do the calculation
outData = Numeric.zeros((rows, cols), Numeric.Float)
outData[1:rows-1,1:cols-1] = ((-0.7 * inData[0:rows-2,0:cols-2]) +
  (-1.0 * inData[0:rows-2,1:cols-1]) + (-0.7 * inData[0:rows-2,2:cols]) +
  (-1.0 * inData[1:rows-1,0:cols-2]) + (6.8 * inData[1:rows-1,1:cols-1]) +
  (-1.0 * inData[1:rows-1,2:cols]) + (-0.7 * inData[2:rows,0:cols-2]) +
  (-1.0 * inData[2:rows,1:cols-1]) + (-0.7 * inData[2:rows,2:cols]))

# create the output image
driver = inDs.GetDriver()
outDs = driver.Create('highpass3.img', cols, rows, 1, GDT_Float32)
if outDs is None:
  print 'Could not create highpass3.img'
  sys.exit(1)
outBand = outDs.GetRasterBand(1)

# write the output data
outBand.WriteArray(outData, 0, 0)

# flush data to disk, set the NoData value and calculate stats
outBand.FlushCache()
stats = outBand.GetStatistics(0, 1)

# georeference the image and set the projection
outDs.SetGeoTransform(inDs.GetGeoTransform())
outDs.SetProjection(inDs.GetProjection())

inDs = None
outDs = None

print time.time() - start, 'seconds'