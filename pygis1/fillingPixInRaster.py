# Filling up sink pixels in a raster file. The script will create a  new raster file with the
# sink pixes filled up.

import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal
from gdalconst import *
import numpy as np

# set directory
os.chdir("W:\\Luis") 

# Register all of the drivers
gdal.AllRegister()

# Reading the DEM raster
# open the image
#ds = gdal.Open('E:\\GeoBase\\CDED\\082n16\\082n16_0201_deme1.tif')
ds = gdal.Open('W:\\Luis\\filled_dem_melkamu1.tif')
if ds is None:
	print 'Could not open image'
	sys.exit(1)
print '\n \n'

# Getting raster dimensions	
cols = ds.RasterXSize
rows = ds.RasterYSize
bands = ds.RasterCount
print cols, rows, bands

# Get the band
band = ds.GetRasterBand(1)

# Writing a new raster file
driver = ds.GetDriver()
newRasterfn='filled_dem_melkamu1_FillPix.tif'
outRaster = driver.Create(newRasterfn, cols, rows, 1, GDT_Float32)
outBand = outRaster.GetRasterBand(1)
outBand.SetNoDataValue(0.0)

# Setting a sink pixel to a mininum value
for i in range(rows):
	for j in range(cols):
		data = band.ReadAsArray(j, i, 1,1)
		value = data[0,0]
		outBand.WriteArray(data, j, i)
		if i == 0 and j == 0:
			dataE = band.ReadAsArray(j+1, i, 1, 1)
			dataS = band.ReadAsArray(j, i+1, 1, 1)
			dataSE = band.ReadAsArray(j+1, i+1, 1, 1)
			v = (dataE[0,0], dataS[0,0], dataSE[0,0])
			if value < min(v):
				print j,i, " Sink!!!"
				a=np.zeros((1,1))
				a[0,0] = min(v)
				outBand.WriteArray(a, j, i)
		elif i == 0 and j == cols-1:
			dataW = band.ReadAsArray(j-1, i, 1, 1)
			dataSW = band.ReadAsArray(j-1, i+1, 1, 1)
			dataS = band.ReadAsArray(j, i+1, 1, 1)
			v = (dataW[0,0], dataSW[0,0], dataS[0,0])
			if value < min(v):
				print j,i, " Sink!!!"
				a=np.zeros((1,1))
				a[0,0] = min(v)
				outBand.WriteArray(a, j, i)
		elif i == rows-1 and j == 0:
			dataE = band.ReadAsArray(j+1, i, 1, 1)
			dataNE = band.ReadAsArray(j+1, i-1, 1, 1)
			dataN = band.ReadAsArray(j, i-1, 1, 1)
			v = (dataE[0,0], dataNE[0,0], dataN[0,0])
			if value < min(v):
				print j,i, " Sink!!!"
				a=np.zeros((1,1))
				a[0,0] = min(v)
				outBand.WriteArray(a, j, i)
		elif i == rows-1 and j == cols-1:
			dataN = band.ReadAsArray(j, i-1, 1, 1)
			dataNW = band.ReadAsArray(j-1, i-1, 1, 1)
			dataW = band.ReadAsArray(j-1, i, 1, 1)
			v = (dataN[0,0], dataNW[0,0], dataW[0,0])
			if value < min(v):
				print j,i, " Sink!!!"
				a=np.zeros((1,1))
				a[0,0] = min(v)
				outBand.WriteArray(a, j, i)
		elif i==0 and (j>0 and j<cols-1):
			dataE = band.ReadAsArray(j+1, i, 1, 1)
			dataW = band.ReadAsArray(j-1, i, 1, 1)
			dataSW = band.ReadAsArray(j-1, i+1, 1, 1)
			dataS = band.ReadAsArray(j, i+1, 1, 1)
			dataSE = band.ReadAsArray(j+1, i+1, 1, 1)
			v = (dataE[0,0], dataW[0,0], dataSW[0,0], dataS[0,0], dataSE[0,0])
			if value < min(v):
				print j,i, " Sink!!!"
				a=np.zeros((1,1))
				a[0,0] = min(v)
				outBand.WriteArray(a, j, i)
		elif i==rows-1 and (j>0 and j<cols-1):
			dataE = band.ReadAsArray(j+1, i, 1, 1)
			dataNE = band.ReadAsArray(j+1, i-1, 1, 1)
			dataN = band.ReadAsArray(j, i-1, 1, 1)
			dataNW = band.ReadAsArray(j-1, i-1, 1, 1)
			dataW = band.ReadAsArray(j-1, i, 1, 1)
			v = (dataE[0,0], dataNE[0,0], dataN[0,0], dataNW[0,0], dataW[0,0])
			if value < min(v):
				print j,i, " Sink!!!"
				a=np.zeros((1,1))
				a[0,0] = min(v)
				outBand.WriteArray(a, j, i)
		elif (i>0 and i<rows-1) and j==0:
			dataE = band.ReadAsArray(j+1, i, 1, 1)
			dataNE = band.ReadAsArray(j+1, i-1, 1, 1)
			dataN = band.ReadAsArray(j, i-1, 1, 1)
			dataS = band.ReadAsArray(j, i+1, 1, 1)
			dataSE = band.ReadAsArray(j+1, i+1, 1, 1)
			v = (dataE[0,0], dataNE[0,0], dataN[0,0], dataS[0,0], dataSE[0,0])
			if value < min(v):
				print j,i, " Sink!!!"
				a=np.zeros((1,1))
				a[0,0] = min(v)
				outBand.WriteArray(a, j, i)
		elif (i>0 and i<rows-1) and j==cols-1:
			dataN = band.ReadAsArray(j, i-1, 1, 1)
			dataNW = band.ReadAsArray(j-1, i-1, 1, 1)
			dataW = band.ReadAsArray(j-1, i, 1, 1)
			dataSW = band.ReadAsArray(j-1, i+1, 1, 1)
			dataS = band.ReadAsArray(j, i+1, 1, 1)
			v = (dataN[0,0], dataNW[0,0], dataW[0,0], dataSW[0,0], dataS[0,0])
			if value < min(v):
				print j,i, " Sink!!!"
				a=np.zeros((1,1))
				a[0,0] = min(v)
				outBand.WriteArray(a, j, i)
		else:
			dataE = band.ReadAsArray(j+1, i, 1, 1)
			dataNE = band.ReadAsArray(j+1, i-1, 1, 1)
			dataN = band.ReadAsArray(j, i-1, 1, 1)
			dataNW = band.ReadAsArray(j-1, i-1, 1, 1)
			dataW = band.ReadAsArray(j-1, i, 1, 1)
			dataSW = band.ReadAsArray(j-1, i+1, 1, 1)
			dataS = band.ReadAsArray(j, i+1, 1, 1)
			dataSE = band.ReadAsArray(j+1, i+1, 1, 1)
			v = (dataE[0,0], dataNE[0,0], dataN[0,0], dataNW[0,0], dataW[0,0] , dataSW[0,0], dataS[0,0], dataSE[0,0])
			if value < min(v):
				print j,i, " Sink!!!"
				a=np.zeros((1,1))
				a[0,0] = min(v)
				outBand.WriteArray(a, j, i)

# flush data to disk, set the NoData value and calculate stats
outBand.FlushCache()
outBand.GetStatistics(0, 1)
#outRaster.SetNoDataValue(ds.GetNoDataValue())
#stats = outRaster.GetStatistics(0, 1)

# georeference the image and set the projection
geoTransform = ds.GetGeoTransform()
outRaster.SetGeoTransform(geoTransform)
proj = ds.GetProjection()
outRaster.SetProjection(ds.GetProjection())	
			
			
# Cleaning up memory
ds = None
outRaster = None
			
