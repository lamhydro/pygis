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

#W:\Luis\QuAppelle\Qu'Appelle River shoreline\merginShapeFil_gdal.py

# set the working directory
locDir = r"W:\Luis\QuAppelle\QuAppelle River shoreline"
os.chdir(locDir)

# Shapefile list
files = ["W:\Luis\QuAppelle\QuAppelle River shoreline\y_quapp_Sshore_elevation.shp",
"W:\Luis\QuAppelle\QuAppelle River shoreline\y_quapp_Nshore_elevation.shp",
"W:\Luis\QuAppelle\QuAppelle River shoreline\Cross_Section\Cross_Section\Waypoints_sonarAppelle_proj.shp"] 

nameMergedFile = 'quapp_section_elevation.shp'
mergedFile = os.path.join(locDir, nameMergedFile)
## if file exists, delete it ##
if os.path.isfile(mergedFile):
        os.remove(mergedFile)
projec = 1

i = 0
for file in files:
    print file
    # Create the main file
    if i == 0:
        cmd = 'ogr2ogr ' + '"' + mergedFile + '"' + ' ' + '"'+ file +'"'
        print cmd
        print os.system(cmd)
    # Merge (append) 'file' to the 'main' file
    else:
        cmd = 'ogr2ogr -update -append ' + '"' + mergedFile + '"' + ' ' +'"'+ file +'"'+ ' -nln ' + nameMergedFile[:-4] 
        print os.system(cmd)
    
    i += 1
	
