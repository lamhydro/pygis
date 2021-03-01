def world2Pixel(geoMatrix, x, y):
  """
  Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
  the pixel location of a geospatial coordinate
  """
  ulX = geoMatrix[0]
  ulY = geoMatrix[3]
  xDist = geoMatrix[1]
  yDist = geoMatrix[5]
  rtnX = geoMatrix[2]
  rtnY = geoMatrix[4]
  pixel = np.round((x - ulX) / xDist).astype(np.int)
  line = np.round((ulY - y) / xDist).astype(np.int)
  return (pixel, line)

# after http://geospatialpython.com/2011/02/clip-raster-using-shapefile.html
# This function will convert the rasterized clipper shapefile
# to a mask for use within GDAL.
def imageToArray(i):
    """
    Converts a Python Imaging Library array to a
    numpy array.
    """
    a=np.fromstring(i.tostring(),'b')
    a.shape=i.im.size[1], i.im.size[0]
    return a
	
#Opening ESRI shapefile. Return the shapefile driver of file and its layer.		
def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
		print 'Could not open file'
		sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)

#import GdalOgrPylib as go
import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from gdalconst import *
import struct
import numpy as np
import matplotlib.pylab as plt
import Image,ImageDraw
import csv
#import math

# set directory
os.chdir("E:\\Documents\\NutrientsLecture2\\Maps") 

# Opening 'CatchmentDef.shp'
#file = 'New_Shapefile.shp'
file = 'NLFLOW_1geog_MiryCreekV2_proj.shp'
shfileCatch, layer = openingShpFile(file)
# - Getting the spatial projection
geoSR = layer.GetSpatialRef()
geoSRop = layer.GetSpatialRef()
#wkt = geoSR.ExportToWkt()
#print 'Spatial projection:', geoSR

# Reading the raster
# - register all of the drivers
gdal.AllRegister()
# open the image
ds = gdal.Open('Fill.tif')
if ds is None:
	print 'Could not open image'
	sys.exit(1)
print '\n \n'
demWKT = ds.GetProjectionRef()
#print 'Spatial projection:', demWKT
geoSRop.ImportFromWkt(demWKT)

# Getting raster dimensions	
cols = ds.RasterXSize
rows = ds.RasterYSize
bands = ds.RasterCount

# Read the whole band (DEMs have only one band)
band = ds.GetRasterBand(1)
blockSize = band.GetBlockSize()
xBlockSize = blockSize[0]
yBlockSize = blockSize[1]
print xBlockSize, yBlockSize

# Reading georeference information
geo_t = ds.GetGeoTransform()
xOrigin = geo_t[0]
yOrigin = geo_t[3]
pixelWidth = geo_t[1]
pixelHeight = geo_t[5]
print xOrigin, yOrigin, geo_t[1], geo_t[5]

# Writing a new raster file
driver = ds.GetDriver()
newRasterfn='StrLnkV2.tif'
#outRaster = driver.Create(newRasterfn, cols, rows, 1, GDT_Float32)
outRaster = driver.Create(newRasterfn, cols, rows, 1, GDT_Int16)
outBand = outRaster.GetRasterBand(1)
outBand.SetNoDataValue(0)

feature = layer.GetNextFeature()
k = 0
while feature:

	# Getting the geometry of the polyline
	pts = feature.GetGeometryRef()
	#pts.AssignSpatialReference(geoSR)
	pts.TransformTo(geoSRop)
	points = []
	for p in range(pts.GetPointCount()):
		points.append((pts.GetX(p), pts.GetY(p)))

	pnts = np.array(points).transpose()
	
	pixel, line = world2Pixel(geo_t,pnts[0],pnts[1])
	j = int(min(pixel))
	i = int(min(line))
	ncols = int(max(pixel) - j)+1
	nrows = int(max(line) - i)+1
	data = band.ReadAsArray(j, i, ncols, nrows)*0 + k+1 # by 0 + 1 to change z into 1 
	dataO = outBand.ReadAsArray(j, i, ncols, nrows)
	
	#print 'OB  ', feature.GetField('OBJECTID')+2
	
	#dataNew = data*0.
	#linepixel = [(line[ii]-i, pixel[ii]-j) for ii in xrange(len(line))]
	
	# Create a new image with the raster dimension
	rasterPoly = Image.new("L", (ncols, nrows),1)
	rasterize = ImageDraw.Draw(rasterPoly)
	listdata = [(pixel[ii]-j,line[ii]-i) for ii in xrange(len(pixel))]
	rasterize.line(listdata,0)
	mask = 1 - imageToArray(rasterPoly)
	mask2 = np.where(mask==0,1,0)
	
	#linepixel = [(line[ii]-i, pixel[ii]-j) for ii in xrange(len(line))]
	#for ij in linepixel:
	#	#print data[ij]
	#	dataO[ij] = 0.
		
	dataInPoly=data*mask+dataO*mask2	
	outBand.WriteArray(dataInPoly, j, i)
	
	
	print k, j, i, ncols, nrows
	
	feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
	feature = layer.GetNextFeature()
	
	#print k
	k += 1
	
	#if k>1:
	#	break
	

# flush data to disk, set the NoData value and calculate stats
outRaster.FlushCache()
#stats = outRaster.GetStatistics(0, 1)

# georeference the image and set the projection
outRaster.SetGeoTransform(ds.GetGeoTransform())
outRaster.SetProjection(ds.GetProjection())	
	
# Cleaning up memory
ds = None
outRaster = None	

# close the shapefile
shfileCatch.Destroy()




