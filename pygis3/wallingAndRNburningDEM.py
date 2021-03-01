import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal
from gdalconst import *
import numpy as np

# set directory
os.chdir("E:\\Documents\\NutrientsLecture2\\Maps") 

# Register all of the drivers
gdal.AllRegister()


# Reading the DEM raster
# open the image
ds = gdal.Open('Fill.tif')
if ds is None:
	print 'Could not open image'
	sys.exit(1)
print '\n \n'

# Getting raster dimensions	
cols = ds.RasterXSize
rows = ds.RasterYSize
bands = ds.RasterCount

# Read the whole band (DEMs have only one band)
band = ds.GetRasterBand(1)
blockSize = band.GetBlockSize()
xBlockSize = blockSize[0]
yBlockSize = blockSize[1]

# Reading the river network mask file 
# open the image
dsRN = gdal.Open('StrV2.tif')
if dsRN is None:
	print 'Could not open image'
	sys.exit(1)
print '\n \n'
bandRN = dsRN.GetRasterBand(1)

# Reading the river network mask file 
# open the image
# dsNHN = gdal.Open('WallOpen.tif')
# if dsNHN is None:
	# print 'Could not open image'
	# sys.exit(1)
# print '\n \n'
# bandNHN = dsNHN.GetRasterBand(1)


# Writing a new raster file
driver = ds.GetDriver()
newRasterfn='MiryCreek_PrXY_RNBurnV2.tif'
outRaster = driver.Create(newRasterfn, cols, rows, 1, GDT_Float32)
outBand = outRaster.GetRasterBand(1)
outBand.SetNoDataValue(-32768.000000)
outBand.SetNoDataValue(0.0)

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
		data = band.ReadAsArray(j, i, numCols, numRows)
		#dataNHN = bandNHN.ReadAsArray(j, i, numCols, numRows)
		dataRN = bandRN.ReadAsArray(j, i, numCols, numRows)
		#data += dataNHN*1000.
		#data = np.where(dataNHN==1,100000.,data) # Comment to burn RN only
		#data -= dataRN*50.
		data = np.where(dataRN==1,data*0.8,data)
		outBand.WriteArray(data, j, i)

# flush data to disk, set the NoData value and calculate stats
outRaster.FlushCache()
#outRaster.SetNoDataValue(ds.GetNoDataValue())
#stats = outRaster.GetStatistics(0, 1)

# georeference the image and set the projection
outRaster.SetGeoTransform(ds.GetGeoTransform())
outRaster.SetProjection(ds.GetProjection())	
	
# Cleaning up memory
ds = None
dsNHN = None
dsRN = None
outRaster = None