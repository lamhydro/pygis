# Transforming a csv file with lat and long point coordinates into a shapefile.

import os, sys
from fnmatch import fnmatch
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr


dir = r"E:\Red_deer_SPARROW\Fluxmaster\Data\TN"
dir = r"E:\Red_deer_SPARROW\Fluxmaster\Flow\initialData"
dir = r"E:\Red_deer_SPARROW\Fluxmaster\Results"
dir = r"E:\Documents\RegiFreqAnaSRrunoffPaper\maps"
dir = r"E:\WaterQualityData\QuAppelle\RIVER OR STREAM"

os.chdir(dir)
csvfile = 'wqStationAfterScreenTN.csv'
csvfile = 'sfStationAfterScreen.csv'
csvfile = 'predict_flux_all.csv'
csvfiledir = r"E:\Documents\RegiFreqAnaSRrunoffPaper\analysis\ANNUAL_MAX_MIN_MEAN_DLY_FLOWS"
csvfiledir = r"E:\WaterQualityData\QuAppelle\RIVER OR STREAM"
csvfile = 'STATIONS_SUMMARY.csv'
csvfile = 'RIVER OR STREAM.csv'

# Creating the DBF files
dbfname = csvfile[:-4]+'.dbf'
dbffile = os.path.join(dir, dbfname)
if os.path.isfile(dbffile):
		os.remove(dbffile)
cmd = 'ogr2ogr -f "ESRI Shapefile" ' + '"' +dir + '"' +' "' + os.path.join(csvfiledir, csvfile) + '"'
print cmd
print os.system(cmd)

# Create the VRT file (made manually, can be written from here too)
# - Changes:
# - 1. Set the shpfile name (layer name) in line 2
shpfilename = 'wqStationAfterScreenTNshp'
shpfilename = 'sfStationAfterScreenshp'
shpfilename = 'predict_flux_allShp'
shpfilename = 'STATIONS_SUMMARYshp'
shpfilename = 'RIVER OR STREAMshp'
# - 2. Set the shpefile home dir of shapefile in line 3
# - 3. Set the name of the shpfile source file (DBF file) in line 4
# - 4. Set the field names for x and y coord (Lat and Lon) in line 7
vrtfile =  csvfile[:-4]+'.vrt'

# Create the SHP file
# - Removing pre-existing shapefiles
# - Removing DBF
DBF = shpfilename+'.dbf'
if os.path.isfile(os.path.join(dir, DBF)):
	os.remove(os.path.join(dir, DBF))
PRJ = shpfilename+'.prj'
if os.path.isfile(os.path.join(dir, PRJ)):
	os.remove(os.path.join(dir, PRJ))
SHP = shpfilename+'.shp'
if os.path.isfile(os.path.join(dir, SHP)):
	os.remove(os.path.join(dir, SHP))
SHX = shpfilename+'.shx'
if os.path.isfile(os.path.join(dir, SHX)):
	os.remove(os.path.join(dir, SHX))	
	
cmd = 'ogr2ogr -f "ESRI Shapefile" ' + '"' +dir + '"' + ' "' + os.path.join(dir, vrtfile) + '"'
print cmd
print os.system(cmd)
