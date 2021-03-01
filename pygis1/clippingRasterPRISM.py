

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


# Opening the projected shapefile
file = r'E:\GeoBase\CDED\redDeerRiverDEM\redDeerRiverCatchPrXY\redDeerRiverCatch.shp'
#file = r'E:\GeoBase\CDED\redDeerRiverDEM\redDeerRiverCatch.shp'
shfile, layer = openingShpFile(file)

# Get the extension
extent = layer.GetExtent()
print extent

# RASTER

# Reprojecting raster
inputfile = r'E:\PRISM\MeanTempGrids\tmean_14'
outputdir = r'E:\PRISM\MeanTempGrids\tmean_14_PrXY.tif'
cmd = 'gdalwarp -overwrite' + ' -t_srs ' + '"'+wkt +'"'+ ' ' + inputfile + ' ' + outputdir
print cmd
print os.system(cmd) # if is 0 is normal execution
#sys.exit(0)
#gdalwarp -t_srs '+proj=merc +datum=WGS84' geoworld.tif mercator.tif

# Reading the raster
# register all of the drivers
gdal.AllRegister()
# open the image
rasterIn = r'E:\PRISM\MeanTempGrids\tmean_14_PrXY.tif'
rasterOut = r'E:\PRISM\MeanTempGrids\tmean_14_PrXY_redDeer.tif'
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
cmd = 'gdal_translate' + ' -projwin ' + str(extent[0]-1000) + ' ' + str(extent[3]+1000) + ' ' + str(extent[1]+10000) + ' ' + str(extent[2]-10000) + ' -of GTiff ' + rasterIn + ' ' + rasterOut
print cmd
print os.system(cmd) # if is 0 is normal execution


