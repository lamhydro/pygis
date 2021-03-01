# Getting the hydrological units within a specific catchment (WSCSDANAME)

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

# River catchment name for looking out. It is recomended to visualize the *.shp file to know the WSCSDANAME 
WSCSDANAME = 'Upper South Saskatchewan'# 'Bow'

# set directory
os.chdir(r"E:\GeoBase\NHN_INDEX_10_INDEX_WORKUNIT_LIMIT_2")

# Opening the shape file
file = r'E:\GeoBase\NHN_INDEX_10_INDEX_WORKUNIT_LIMIT_2\NHN_INDEX_10_INDEX_WORKUNIT_LIMIT_2.shp'
shfile, layer = openingShpFile(file)

# Reading through features
feature = layer.GetNextFeature()
while feature:

	# Printing fields
	if feature.GetField('WSCSDANAME') == WSCSDANAME:
		print feature.GetField('WSCSDANAME'), feature.GetField('DATASETNAM'), feature.GetField('WSCSSDANAM')
	
	feature.Destroy()
	feature = layer.GetNextFeature()
	
layer = None
shfile = None