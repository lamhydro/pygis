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
locDir = r"W:\Luis\Colin_QuAppelle\effective_areas"
os.chdir(locDir) 

root = r"W:\Luis\Colin_QuAppelle\effective_areas"
#allPattern = ['*ISLAND_2.shp','*MANMADE_0.shp','*MANMADE_1.shp','*MANMADE_2.shp','*OBSTACLE_0.shp','*SLWATER_1.shp','*WATERBODY_2.shp','*BANK_1.shp','*DELIMITER_1.shp','*HYDROJUNCT_0.shp','*NLFLOW_1.shp','*NAMEDFEA_0.shp','*WORKUNIT_LIMIT_2.shp']
#pattern = allPattern[12]
pattern = '*effective_area.shp'
projec = 0

nameMergedFile = pattern[1:]
mergedFile = os.path.join(root, nameMergedFile)
## if file exists, delete it ##
if os.path.isfile(mergedFile):
        os.remove(mergedFile)

i = 0
for path, subdirs, files in os.walk(locDir):
    for name in files:
        if fnmatch(name, pattern):
			file = os.path.join(path, name)
			print name
			print path
			
			# Create the main file
			if i == 0:
				cmd = 'ogr2ogr ' + mergedFile + ' ' + file
				print os.system(cmd)
			# Merge (append) 'file' to the 'main' file
			else:
				cmd = 'ogr2ogr -update -append ' + mergedFile + ' ' + file + ' -nln ' + nameMergedFile[:-4] 
				print os.system(cmd)
			
			i += 1


# If the file does not have coord. sys.
if projec:

	coordSys='EPSG:4269' # for NAD83 coord sys

	mergedFileGeo = os.path.join(root, nameMergedFile[:-4]+'geog.shp')
	## if file exists, delete it ##
	if os.path.isfile(mergedFileGeo):
		os.remove(mergedFileGeo)
		
	# Setting up the coord. sys.
	cmd = 'ogr2ogr -f ' + '"ESRI Shapefile"'+ ' -a_srs ' + coordSys + ' ' + mergedFileGeo + ' ' + mergedFile
	print os.system(cmd)
