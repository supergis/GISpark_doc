# import modules
import glob, os, ospy_hw3b_mod

# set the working directory
os.chdir(r'Z:\Data\Classes\Python\ospy3\ospy3_data')

# loop through the shapefiles in the working directory
for inFN in glob.glob('*.shp'):

  # make the output filename
  outFN = inFN.replace('.shp', '_proj.shp')

  # reproject the shapefile
  hw3b_mod.reproject(inFN, 26912, outFN, 4269)
