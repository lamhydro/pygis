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
os.chdir(r"E:\GeoBase\CDED\redDeerRiverDEM_50k")

# - Getting the spatial projection from a shapefile
# Opening the shape file
file = 'redDeerRiverCatch.shp'
shfile, layer = openingShpFile(file)
geoSR = layer.GetSpatialRef()
wkt = geoSR.ExportToWkt()
print 'Spatial projection:', wkt

#sys.exit(0)

# Opening the projected shapefile
#file = r'E:\GeoBase\CDED\redDeerRiverDEM\redDeerRiverCatchPrXY\redDeerRiverCatch.shp'
#file = r'E:\GeoBase\CDED\redDeerRiverDEM\redDeerRiverCatch.shp'
#shfile, layer = openingShpFile(file)

# Get the extension
#extent = layer.GetExtent()
#print extent

# RASTER

# Reprojecting raster
inputfile = 'reddeerrivdem'
outputdir = 'reddeerdempr.tif'
cmd = 'gdalwarp -overwrite' + ' -t_srs ' + '"'+wkt +'"'+ ' ' + inputfile + ' ' + outputdir
print cmd
#print os.system(cmd) # if is 0 is normal execution
#gdalwarp -t_srs '+proj=merc +datum=WGS84' geoworld.tif mercator.tif

# Cliping raster with other polygon
input_polygon_shp = file
input_tif = outputdir
clipped_output_tif = 'demprcli.tif'
cmd = 'gdalwarp -dstnodata 0 '+' -cutline ' +  input_polygon_shp + ' -crop_to_cutline -dstalpha ' + input_tif + ' ' + clipped_output_tif
print cmd
print os.system(cmd) # if is 0 is normal execution
#gdalwarp -dstnodata <nodata_value> -cutline input_polygon.shp input.tif clipped_output.tif
sys.exit(0)
# Reading the raster
# register all of the drivers
gdal.AllRegister()
# open the image
rasterIn = 'reddeerdempr.tif'
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
cmd = 'gdal_translate' + ' -projwin ' + str(extent[0]) + ' ' + str(extent[3]) + ' ' + str(extent[1]) + ' ' + str(extent[2]) + ' -of GTiff ' + rasterIn + ' ' + rasterOut
print cmd
print os.system(cmd) # if is 0 is normal execution




