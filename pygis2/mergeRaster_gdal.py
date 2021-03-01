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

# List of raster to be merged
inRasterList=[
'E:\\SaskRiv_SPARROW\\dem\\can3d_dem', 
'E:\\SouthSaskRiv_SPARROW\\dem\\USGS_NEDdatabase\\n49w114\\floatn49w114_1.flt',
'E:\\SouthSaskRiv_SPARROW\\dem\\USGS_NEDdatabase\\n49w115\\floatn49w115_1.flt'
]

outdir = 'E:\\SaskRiv_SPARROW\\dem\\'
conInRasterList = ""
for i in inRasterList:

	# Masking the 'black' (no data) sectors in the rasters
	#get path and filename seperately   
	(filepath, name) = os.path.split(i)                
	#get file name without extension   
	(shortname, extension) = os.path.splitext(name) 
	outfile = outdir + shortname +'_NoBlackCol'+ extension
	cmd = 'gdal_translate ' + i + ' ' + outfile + ' -mask 1'
	print cmd
	print os.system(cmd) # if is 0 is normal execution
	
	# Concatenate strings and white spaces
	conInRasterList += outfile + " "

conInRasterList = conInRasterList[:-1]
print conInRasterList

# Merging rasters
outRaster = outdir + 'canadaDEM_montana.tif'
if os.path.exists(outRaster):
    os.remove(outRaster)
cmd = 'gdalwarp ' + conInRasterList + ' ' + outRaster + ' -dstnodata None'
print cmd
print os.system(cmd) # if is 0 is normal execution

# Reprojecting resulting merged raster
# - Getting the spatial projection from shapefile
# Opening the shape file
file = r'E:\Red_deer_SPARROW\RiverNet2\CatchmentDef.shp'
shfile, layer = openingShpFile(file)
geoSR = layer.GetSpatialRef()
wkt = geoSR.ExportToWkt()
outRaster1 = outdir + 'canadaDEM_montana_PrXY.tif' 
cmd = 'gdalwarp -overwrite' + ' -t_srs ' + '"'+wkt +'"'+ ' ' + outRaster + ' ' + outRaster1
print cmd
print os.system(cmd) # if is 0 is normal execution
