# homework 6a
# high-pass filter using pixel notation
import os, sys, Numeric, gdal, time
from gdalconst import *

start = time.time()

os.chdir('c:/temp/py6')

# register all of the GDAL drivers
gdal.AllRegister()

# open the image
inDs = gdal.Open('smallaster.img', GA_ReadOnly)
if inDs is None:
  print 'Could not open smallaster.img'
  sys.exit(1)

# get image size
rows = inDs.RasterYSize
cols = inDs.RasterXSize

# read the input data
inBand = inDs.GetRasterBand(1)
inData = inBand.ReadAsArray(0, 0, cols, rows).astype(Numeric.Float)

# do the calculation
outData = Numeric.zeros((rows, cols), Numeric.Float)
for i in range(1, rows-1):
  for j in range(1, cols-1):
    outData[i,j] = ((-0.7 * inData[i-1,j-1]) + (-1.0 * inData[i-1,j]) + (-0.7 * inData[i-1,j+1]) +
      (-1.0 * inData[i,j-1]) + (6.8 * inData[i,j]) + (-1.0 * inData[i,j+1]) +
      (-0.7 * inData[i+1,j-1]) + (-1.0 * inData[i+1,j]) + (-0.7 * inData[i+1,j+1]))

# create the output image
driver = inDs.GetDriver()
outDs = driver.Create('highpass1.img', cols, rows, 1, GDT_Float32)
if outDs is None:
  print 'Could not create highpass1.img'
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