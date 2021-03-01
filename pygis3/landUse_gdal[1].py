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
    a=np.fromstring(i.tobytes(),'b')
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
import csv
from collections import Counter
try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image, ImageDraw  


# set directory
os.chdir(r"W:\Luis\Colin_QuAppelle\effective_areas")

# Opening 'CatchmentDef.shp'
file = 'effective_area.shp'
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
ds = gdal.Open(r'G:\QuAppelle_SPARROW\sourceVariables\LandUse\QuAppelleLandUse_BB_repro.tif')
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
jj = 0
maxPi=[]
geoMatrix=range(0,6)
GridIDs = []
AAFCcode_20=[]
AAFCcode_30=[]
AAFCcode_31=[]
AAFCcode_32=[]
AAFCcode_33=[]
AAFCcode_34=[]
AAFCcode_40=[]
AAFCcode_50=[]
AAFCcode_51=[]
AAFCcode_52=[]
AAFCcode_80=[]
AAFCcode_81=[]
AAFCcode_82=[]
AAFCcode_83=[]
AAFCcode_110=[]
AAFCcode_120=[]
AAFCcode_121=[]
AAFCcode_122=[]
AAFCcode_200=[]
AAFCcode_210=[]
AAFCcode_220=[]
AAFCcode_230=[]
sumError = 0
areas = ['05JG004', '05JG005','05JG007','05JG010','05JG011','05JG013','05JG014']
with open('effective_landUse_perce.csv','w') as f1, open('effective_landUse_areaM2.csv','w') as f2:
	writer=csv.writer(f1, delimiter=',',lineterminator='\n')
	writer2=csv.writer(f2, delimiter=',',lineterminator='\n')
	# Note: see file 'AAFC_LULC_Classes.csv' in the current dir for codes.
	writer.writerow(['FID','SubCatchment','Area(M^2)','AAFCcode_20','AAFCcode_30','AAFCcode_31','AAFCcode_32','AAFCcode_33','AAFCcode_34','AAFCcode_40','AAFCcode_50','AAFCcode_51','AAFCcode_52','AAFCcode_80','AAFCcode_81','AAFCcode_82','AAFCcode_83','AAFCcode_110','AAFCcode_120','AAFCcode_121','AAFCcode_122','AAFCcode_200', 'AAFCcode_210','AAFCcode_220','AAFCcode_230'])
	writer2.writerow(['FID','SubCatchment','Area(M^2)','AAFCcode_20','AAFCcode_30','AAFCcode_31','AAFCcode_32','AAFCcode_33','AAFCcode_34','AAFCcode_40','AAFCcode_50','AAFCcode_51','AAFCcode_52','AAFCcode_80','AAFCcode_81','AAFCcode_82','AAFCcode_83','AAFCcode_110','AAFCcode_120','AAFCcode_121','AAFCcode_122','AAFCcode_200', 'AAFCcode_210','AAFCcode_220','AAFCcode_230'])

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

		#transforming between pixel/line (P,L) raster space, and projection coordinates (Xp,Yp) space.
		pixel, line = world2Pixel(geo_t,pnts[0],pnts[1])
		
		# Reading the rectangle of the raster occupy by the polygon
		j = int(min(pixel))
		i = int(min(line))
		ncols = int(max(pixel) - j)+1
		nrows = int(max(line) - i)+1
		data = band.ReadAsArray(j, i, ncols, nrows)

		# Create a new image with the raster dimension
		rasterPoly = Image.new("L", (ncols, nrows),1)
		rasterize = ImageDraw.Draw(rasterPoly)
		listdata = [(pixel[ii]-j,line[ii]-i) for ii in xrange(len(pixel))]
		#listdata = [(pixel[i],line[i]) for i in xrange(len(pixel))]
		rasterize.polygon(listdata,0)
		mask = 1 - imageToArray(rasterPoly)
		ncell = np.sum(mask)

		dataInPoly=data*mask
		dime = dataInPoly.shape
		dataInPolyFreq = Counter( np.reshape(dataInPoly, dime[0]*dime[1]) )
		dataInPolyFreq_perce = dataInPolyFreq.copy()
		dataInPolyFreq_area = dataInPolyFreq.copy()
		for k in dataInPolyFreq.keys():
			dataInPolyFreq_perce[k] = 100.*dataInPolyFreq[k]/ncell
			dataInPolyFreq_area[k] = dataInPolyFreq[k]*cellArea
	 
		#dataInPoly[np.where(dataInPoly == 0)] = -99999

		#maxZ = np.max(dataInPoly[np.nonzero(dataInPoly)])
		#minZ = np.min(dataInPoly[np.nonzero(dataInPoly)])
		
		#avAtmosDepo = np.sum(dataInPoly)/(ncell)
		#rainAveCell = ncell*cellArea*rainAveM
		#rainAveArea = feature.GetField('Shape_Area') * rainAveM
		
		print jj
		
		#GridIDs.append(feature.GetField('GridID'))
		# AAFCcode_20.append(dataInPolyFreq[20])
		# AAFCcode_30.append(dataInPolyFreq[30])
		# AAFCcode_31.append(dataInPolyFreq[31])
		# AAFCcode_32.append(dataInPolyFreq[32])
		# AAFCcode_33.append(dataInPolyFreq[33])
		# AAFCcode_34.append(dataInPolyFreq[34])
		# AAFCcode_40.append(dataInPolyFreq[40])
		# AAFCcode_50.append(dataInPolyFreq[50])
		# AAFCcode_51.append(dataInPolyFreq[51])
		# AAFCcode_52.append(dataInPolyFreq[52])
		# AAFCcode_80.append(dataInPolyFreq[80])
		# AAFCcode_81.append(dataInPolyFreq[81])
		# AAFCcode_82.append(dataInPolyFreq[82])
		# AAFCcode_83.append(dataInPolyFreq[83])
		# AAFCcode_110.append(dataInPolyFreq[110])
		# AAFCcode_120.append(dataInPolyFreq[120])
		# AAFCcode_121.append(dataInPolyFreq[121])
		# AAFCcode_122.append(dataInPolyFreq[122])
		# AAFCcode_200.append(dataInPolyFreq[200])
		# AAFCcode_210.append(dataInPolyFreq[210])
		# AAFCcode_220.append(dataInPolyFreq[220])
		# AAFCcode_230.append(dataInPolyFreq[230])
		totArea = ncell*cellArea
		
		row = [jj,areas[jj],totArea, dataInPolyFreq_perce[20],dataInPolyFreq_perce[30],dataInPolyFreq_perce[31],dataInPolyFreq_perce[32],dataInPolyFreq_perce[33],dataInPolyFreq_perce[34],dataInPolyFreq_perce[40],dataInPolyFreq_perce[50],dataInPolyFreq_perce[51],dataInPolyFreq_perce[52],dataInPolyFreq_perce[80],dataInPolyFreq_perce[81],dataInPolyFreq_perce[82],dataInPolyFreq_perce[83],dataInPolyFreq_perce[110],dataInPolyFreq_perce[120],dataInPolyFreq_perce[121],dataInPolyFreq_perce[122],dataInPolyFreq_perce[200], dataInPolyFreq_perce[210],dataInPolyFreq_perce[220],dataInPolyFreq_perce[230]]
		writer.writerow(row)
		
		row = [jj,areas[jj],totArea, dataInPolyFreq_area[20],dataInPolyFreq_area[30],dataInPolyFreq_area[31],dataInPolyFreq_area[32],dataInPolyFreq_area[33],dataInPolyFreq_area[34],dataInPolyFreq_area[40],dataInPolyFreq_area[50],dataInPolyFreq_area[51],dataInPolyFreq_area[52],dataInPolyFreq_area[80],dataInPolyFreq_area[81],dataInPolyFreq_area[82],dataInPolyFreq_area[83],dataInPolyFreq_area[110],dataInPolyFreq_area[120],dataInPolyFreq_area[121],dataInPolyFreq_area[122],dataInPolyFreq_area[200], dataInPolyFreq_area[210],dataInPolyFreq_area[220],dataInPolyFreq_area[230]]
		writer2.writerow(row)
		
		feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them

		feature = layer.GetNextFeature()
		
		#if jj == 1:
		#	break
			
		jj += 1
		

#print 'Ave error of rainfall estimation: ', sumError/j, ' %'
# Cleaning up memory
band = None
data = None	
shfileCatch.Destroy()

# Reading matching relationship of streams and subcatchments
#NIDriv = []
#GridIDcat = []
#with open('E:\\SouthSaskRiv_SPARROW\\RivNet3\\NIDrivAndGridIDcatDef.txt', 'r') as f:
#    # do things with your file
#	header = f.readline()
#	for line in f:
#		columns = line.split()
#		NIDriv.append(columns[0])
#		GridIDcat.append(int(columns[1]))	

		
# # Reordering sub. catch. values to streams. Writing into a file.

	# i = 0
    # for area in areas:
		# row = [i,area,AAFCcode_20[i],AAFCcode_30[i],AAFCcode_31[i],AAFCcode_32[i],AAFCcode_33[i],AAFCcode_34[i],AAFCcode_40[i],AAFCcode_50[i],AAFCcode_51[i],AAFCcode_52[i],AAFCcode_80[i],AAFCcode_81[i],AAFCcode_82[i],AAFCcode_83[i],AAFCcode_110[i],AAFCcode_120[i],AAFCcode_121[i],AAFCcode_122[i],AAFCcode_200[i], AAFCcode_210[i],AAFCcode_220[i],AAFCcode_230[i]]
		# writer.writerow(row)
		# i += 1 