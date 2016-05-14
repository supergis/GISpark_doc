import Numeric, os
os.chdir('c:/temp')
data2 = Numeric.array([ [0,54,100], [87,230,5], [161,120,24] ])
data3 = Numeric.array([ [0,100,23], [78,29,1], [134,245,0] ])
print data2
print data3
ndvi = (data3 - data2) / (data3 + data2)
mask = Numeric.greater(data3 + data2, 0)
print mask
ndvi = Numeric.choose(mask, (-99, (data3 - data2) / (data3 + data2)))
data3 = data3.astype(Numeric.Float16)
data2 = data2.astype(Numeric.Float16)
ndvi = Numeric.choose(mask, (-99, (data3 - data2) / (data3 + data2)))
print ndvi
import gdal
from gdalconst import *
driver = gdal.GetDriverByName('HFA')
ds = driver.Create('sample1.img', 3, 3, 1, GDT_Float32)
band = ds.GetRasterBand(1)
band.WriteArray(ndvi, 0, 0)
ds = None
ds = driver.Create('sample2.img', 3, 3, 1, GDT_Float32)
band = ds.GetRasterBand(1)
band.WriteArray(ndvi, 0, 0)
ds = None
ds = driver.Create('sample3.img', 3, 3, 1, GDT_Float32)
band = ds.GetRasterBand(1)
band.WriteArray(ndvi, 0, 0)
band.FlushCache()
band.SetNoDataValue(-99)
band.GetStatistics(0,1)
ds = None
ds = driver.Create('sample4.img', 3, 3, 1, GDT_Float32)
band = ds.GetRasterBand(1)
band.WriteArray(ndvi, 1, 1)
