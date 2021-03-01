

# Opening ESRI shapefile. Return the shapefile driver of file and its layer.		
def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
		print 'Could not open file'
		sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)

# Clipping raster file using gdal
import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from gdalconst import *

# set directory
#os.chdir(r"E:\Runoff")

# - Getting the spatial projection from a shapefile
# Opening the shape file
file = r'E:\Red_deer_SPARROW\RiverNet2\CatchmentDef.shp'
shfile, layer = openingShpFile(file)
geoSR = layer.GetSpatialRef()
wkt = geoSR.ExportToWkt()
print 'Spatial projection:', wkt

# Projecting the target shapefile
inputfile = r'E:\GeoBase\CDED\redDeerRiverDEM\redDeerRiverCatch.shp'
outputdir = r'E:\GeoBase\CDED\redDeerRiverDEM\redDeerRiverCatchPrXY'
cmd = 'ogr2ogr' + ' -overwrite' + ' -f "ESRI Shapefile" ' + ' -t_srs ' + '"'+wkt +'"'+ ' ' + outputdir + ' ' + inputfile
print cmd
print os.system(cmd) # if is 0 is normal execution

# Opening the projected shapefile
file = r'E:\GeoBase\CDED\redDeerRiverDEM\redDeerRiverCatchPrXY\redDeerRiverCatch.shp'
#file = r'E:\GeoBase\CDED\redDeerRiverDEM\redDeerRiverCatch.shp'
shfile, layer = openingShpFile(file)

# Get the extension
extent = layer.GetExtent()
print extent

# RASTER

# Reprojecting raster
inputfile = r'E:\Runoff\runoff_14_r30'
outputdir = r'E:\Runoff\runoff_14_r30_PrXY.tif'
cmd = 'gdalwarp -overwrite' + ' -t_srs ' + '"'+wkt +'"'+ ' ' + inputfile + ' ' + outputdir
print cmd
print os.system(cmd) # if is 0 is normal execution
#sys.exit(0)
#gdalwarp -t_srs '+proj=merc +datum=WGS84' geoworld.tif mercator.tif

# Reading the raster
# register all of the drivers
gdal.AllRegister()
# open the image
rasterIn = r'E:\Runoff\runoff_14_r30_PrXY.tif'
rasterOut = r'E:\Runoff\runoff_14_r30_PrXY_redDeer.tif'
ds = gdal.Open(rasterIn)
if ds is None:
	print 'Could not open image'
	sys.exit(1)
print '\n \n'
demWKT = ds.GetProjectionRef()
print 'Spatial projection:', demWKT

geotransform = ds.GetGeoTransform()
print geotransform

# Cliping the raster
cmd = 'gdal_translate' + ' -projwin ' + str(extent[0]-5000.) + ' ' + str(extent[3]+5000.) + ' ' + str(extent[1]+5000.) + ' ' + str(extent[2]-5000.) + ' -of GTiff ' + rasterIn + ' ' + rasterOut
print cmd
print os.system(cmd) # if is 0 is normal execution

sys.exit(0)


# Getting the spatial projection
geoSR = layer.GetSpatialRef()
#print 'Spatial projection:', geoSR

#geoSR = osr.SpatialReference()
#geoSR.ImportFromEPSG(4326) # unprojected WGS84



utmSR = osr.SpatialReference()
utmSR.ImportFromEPSG(32612) # UTM 12N WGS84

coordTrans = osr.CoordinateTransformation(geoSR, utmSR)
feature = layer.GetNextFeature()
geom = feature.GetGeometryRef()
geom.Transform(coordTrans)
print geom.GetX(10), geom.GetY(10)

sys.exit(0)


import os, sys
#if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
#    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
osgeopath = "C:/Program Files (x86)/GDAL"
#osgeopath ="C:\OSGeo4W\bin"
path = "E:/Red_deer_SPARROW/RiverNet2/riverNet2.gdb"  # path to .shp files
newpath = "E:/Red_deer_SPARROW/RiverNet2"
newfilename = "AdjointCatchment.shp"
filename="AdjointCatchment"

# Getting the extend of the shape file
path=r'C:\Users\Luis\Downloads\nhn_rhn_05ck000_shp_en'
shfile='NHN_05CK000_1_0_HD_WATERBODY_2.sh'
cmd = '"' + osgeopath + '/' + 'ogrinfo" ' + path + '/' + shfile + ' ' + '-so' + ' ' + '-al' 

#ogrinfo clipping_mask.shp -so -al
#coordinates 

#cmd = '"' +  osgeopath + '/' + 'gdal_translate -projwin"'  + path + ' ' + filename
print cmd
print os.system(cmd)



