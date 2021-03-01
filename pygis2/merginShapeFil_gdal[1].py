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
locDir = "Z:\\Luis\\STATSGO\\merge_ussoils_10and17shp"
os.chdir(locDir) 

projec = 0


# Create the merged file			
nameMergedFile = 'ussoils_10and17.shp'
mergedFile = os.path.join(locDir, nameMergedFile)
file = r'Z:\Luis\STATSGO\ussoils_10.e00\ussoils_100_polygon.shp'	
cmd = 'ogr2ogr ' + mergedFile + ' ' + file
print os.system(cmd)	

# Merge the files
file = r'Z:\Luis\STATSGO\ussoils_17.e00\ussoils_170_polygon.shp'		
cmd = 'ogr2ogr -update -append ' + mergedFile + ' ' + file + ' -nln ' + nameMergedFile[:-4] 
print os.system(cmd)

# If the file does not have coord. sys.
if projec:

	coordSys='EPSG:4269' # for NAD83 coord sys

	mergedFileGeo = os.path.join(locDir, nameMergedFile[:-4]+'geog.shp')
	## if file exists, delete it ##
	if os.path.isfile(mergedFileGeo):
		os.remove(mergedFileGeo)
		
	# Setting up the coord. sys.
	cmd = 'ogr2ogr -f ' + '"ESRI Shapefile"'+ ' -a_srs ' + coordSys + ' ' + mergedFileGeo + ' ' + mergedFile
	print os.system(cmd)
