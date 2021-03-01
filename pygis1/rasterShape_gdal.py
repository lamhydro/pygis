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
	
# Opening ESRI shapefile. Return the shapefile driver of file and its layer.		
def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
		print 'Could not open file'
		sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)

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

# set directory
#os.chdir(r'C:\Users\Luis\Downloads\072e')
os.chdir("E:\\Red_deer_SPARROW\\RiverNet2")

# Opening 'CatchmentDef.shp'
#file = 'New_Shapefile.shp'
file = 'CatchmentDef.shp'
shfileCatch, layer = openingShpFile(file)

# Getting the spatial projection
geoSR = layer.GetSpatialRef()
geoSRop = layer.GetSpatialRef()
wkt = geoSR.ExportToWkt()
print 'Spatial projection:', geoSR

# Reading the raster
# register all of the drivers
gdal.AllRegister()
# open the image
ds = gdal.Open('filall')
if ds is None:
	print 'Could not open image'
	sys.exit(1)
print '\n \n'
demWKT = ds.GetProjectionRef()
print 'Spatial projection:', demWKT

geoSRop.ImportFromWkt(demWKT)
# wkt from above, is the wicket from the shapefile
geoSR.ImportFromWkt(wkt)
# now make sure we have the shapefile geom

# Getting image dimensions	
cols = ds.RasterXSize
rows = ds.RasterYSize
bands = ds.RasterCount
# Read the whole band (DEMs have only one band)
band = ds.GetRasterBand(1) 
data = band.ReadAsArray(0, 0, cols, rows).astype(np.float)
#mask = np.greater(data,0)
data = np.where(data>np.min(data),data,0)
#sys.exit(0)
# feature = layer.GetFeature(5)
# geom = feature.GetGeometryRef()
# bbox = geom.GetEnvelope()
# tpe = geom.GetGeometryType()
# print '5 ', geom.GetGeometryCount(), bbox, tpe
# outring = geom.GetGeometryRef(0)
# inring = geom.GetGeometryRef(1)
# print outring.GetPointCount(), ' ', inring.GetPointCount()

#sys.exit(0)

geo_t = ds.GetGeoTransform()

feature = layer.GetNextFeature()
j = 0
maxPi=[]
f = open('catchMinMax.txt', 'w')
while feature:
	# Geting the geometry of the polygons
	geom = feature.GetGeometryRef()
	points = []
	print j, ' ', geom.GetGeometryType(),'  ', geom.GetGeometryCount()
	if geom.GetGeometryType() == 6: # For multipolygons
		for idpol in range(geom.GetGeometryCount()):
			pts = geom.GetGeometryRef(idpol).Boundary()
			pts.AssignSpatialReference(geoSR)
			pts.TransformTo(geoSRop)
			for p in range(pts.GetPointCount()):
				points.append((pts.GetX(p), pts.GetY(p)))
	else:							# For polygons
		pts = geom.GetGeometryRef(0) #0 for the outer polygon
		pts.AssignSpatialReference(geoSR)
		pts.TransformTo(geoSRop)
		for p in range(pts.GetPointCount()):
			points.append((pts.GetX(p), pts.GetY(p)))

	pnts = np.array(points).transpose()

	#transforming between pixel/line (P,L) raster space, and projection coordinates (Xp,Yp) space.
	pixel, line = world2Pixel(geo_t,pnts[0],pnts[1])

	#import pylab
	#plt.figure()
	#plt.plot(pnts[0],pnts[1])
	#plt.imshow(data)
	#plt.plot(pixel, line)
	#plt.show()
	#cbar = fig.colorbar(cax)
	#sys.exit()

	# Create a new image with the raster dimension
	rasterPoly = Image.new("L", (cols, rows),1)
	rasterize = ImageDraw.Draw(rasterPoly)
	listdata = [(pixel[i],line[i]) for i in xrange(len(pixel))]
	rasterize.polygon(listdata,0)
	mask = 1 - imageToArray(rasterPoly)
	
	#plt.imshow(mask)
	#plt.show()
	
	dataInPoly=data*mask
	#dataInPoly[np.where(dataInPoly == 0)] = -99999
	
	#minPi = []
	#for k  in range(len(dataInPoly)):
	#	print min(np.nonzero(dataInPoly[k]))
	#	minPi.append(min(np.nonzero(dataInPoly[k])))

	maxZ = np.max(dataInPoly[np.nonzero(dataInPoly)])
	minZ = np.min(dataInPoly[np.nonzero(dataInPoly)])

	f.write(str(minZ)+'\t'+str(maxZ)+'\n')
	#maxPi.append(np.max(dataInPoly))
	
	
	#fig = plt.figure()
	#ax = fig.add_subplot(111)
	#cax = ax.imshow(dataInPoly, interpolation='nearest')	

	feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them

	feature = layer.GetNextFeature()
	
	#if j == 12:
	#	break
		
	j += 1
	#plt.imshow(mask)
	#plt.show()
	
f.close()

# Cleaning up memory
band = None
data = None	

#cbar = fig.colorbar(cax)
#plt.show()
