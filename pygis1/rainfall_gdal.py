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

# set directory
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
ds = gdal.Open(r'E:\CaPAdata\preciAv2002_2013_PrXY_RedDeer_r30.tif')
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
blockSize = band.GetBlockSize()
xBSize = blockSize[0]
xBSize = blockSize[1]
print xBSize, xBSize


#data = band.ReadAsArray(0, 0, cols, rows).astype(np.float)

#data = np.where(data>np.min(data),data,0)

geo_t = ds.GetGeoTransform()
xOrigin = geo_t[0]
yOrigin = geo_t[3]
pixelWidth = geo_t[1]
pixelHeight = geo_t[5]
print xOrigin, yOrigin, geo_t[1], geo_t[5]
cellArea = abs(pixelWidth*pixelHeight)
#sys.exit(0)

feature = layer.GetNextFeature()
j = 0
maxPi=[]
geoMatrix=range(0,6)
#f = open('runoffm3s.txt', 'w')
#f.write('SPARROWID,COUNT,CellAreaSQM,CatchmentAreaSQM,SUM(mm/year),	SUM(m/year),R1(m3/year),R2(m3/year),Error,R1(m3/s),R2_Chosen(m3/s)'+'\n')
ofile  = open('annualCaPA_Rainfall.csv', "wb")
writer = csv.writer(ofile)
header = ['SPARROWID','CaPA_Rainfall_mmYear']
writer.writerow(header)
sumError = 0
while feature:
	# Geting the geometry of the polygons
	geom = feature.GetGeometryRef()
	points = []
	#print j, ' ', geom.GetGeometryType(),'  ', geom.GetGeometryCount()
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
	
	# Getting the portion of raster limited by the polygon
	minXgeom = min(pnts[0])
	maxXgeom = max(pnts[0])
	minYgeom = min(pnts[1])
	maxYgeom = max(pnts[1])
	xOffset = int((minXgeom - xOrigin) / pixelWidth)
	yOffset = int((maxYgeom - yOrigin) / pixelHeight)
	ncols = int((maxXgeom - minXgeom) / pixelWidth)
	nrows = int((maxYgeom - minYgeom) / abs(pixelHeight))
	data = band.ReadAsArray(xOffset, yOffset, ncols, nrows)
	geoMatrix[0] = minXgeom
	geoMatrix[3] = maxYgeom
	geoMatrix[1] = pixelWidth
	geoMatrix[5] = pixelHeight
	geoMatrix[2] = 0.0
	geoMatrix[4] = 0.0

	#transforming between pixel/line (P,L) raster space, and projection coordinates (Xp,Yp) space.
	pixel, line = world2Pixel(geoMatrix,pnts[0],pnts[1])
	#pixel, line = world2Pixel(geo_t,pnts[0],pnts[1])

	# Create a new image with the raster dimension
	#rasterPoly = Image.new("L", (cols, rows),1)
	rasterPoly = Image.new("L", (ncols, nrows),1)
	rasterize = ImageDraw.Draw(rasterPoly)
	listdata = [(pixel[i],line[i]) for i in xrange(len(pixel))]
	rasterize.polygon(listdata,0)
	mask = 1 - imageToArray(rasterPoly)
	ncell = np.sum(mask)

	dataInPoly=data*mask
	#dataInPoly[np.where(dataInPoly == 0)] = -99999

	#maxZ = np.max(dataInPoly[np.nonzero(dataInPoly)])
	#minZ = np.min(dataInPoly[np.nonzero(dataInPoly)])
	
	rainAveM = np.sum(dataInPoly)/(ncell)
	#rainAveCell = ncell*cellArea*rainAveM
	#rainAveArea = feature.GetField('Shape_Area') * rainAveM
	
	print 'Ave. rainfall mm/y : ' ,j, rainAveM
	
	#plt.imshow(mask)
	#plt.show()	
	#print ncell*cellArea, ' ', feature.GetField('Shape_Area')
	#print 100*abs(ncell*cellArea - feature.GetField('Shape_Area'))/feature.GetField('Shape_Area')

	# Writing to a file
	writer.writerow([int(j),\
					float(rainAveM)])
					
	#sumError = sumError + abs(100*(rainAveCell-rainAveArea)/rainAveCell)

	#maxPi.append(np.max(dataInPoly))
	
	feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them

	feature = layer.GetNextFeature()
	
	#if j == 12:
	#	break
		
	j += 1
	
ofile.close()

#print 'Ave error of rainfall estimation: ', sumError/j, ' %'
# Cleaning up memory
band = None
data = None	