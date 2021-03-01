# Merging shapefiles using GDAL/ORG

# Opening ESRI shapefile. Return the shapefile driver of file and its layer.		
def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
		print 'Could not open file'
		sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)

import os, sys
from fnmatch import fnmatch
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr

# set the working directory
locDir = "Z:\\Luis\\STATSGO\\merge_ussoilsAndcasoils"
os.chdir(locDir) 


# Merge two files with different attributes		
nameMergedFile = 'ussoils_casoils.shp'
mergedFile = os.path.join(locDir, nameMergedFile)
# - This file 'merge.vrt' is created with the names of the two shapefiles that are going to be merged.
merge_vrt = 'Z:\Luis\STATSGO\merge_ussoilsAndcasoils\merge.vrt'	 
cmd = 'ogr2ogr ' +' "' + mergedFile + '" ' + merge_vrt # merge.shp merge.vrt
print cmd
print os.system(cmd)	
