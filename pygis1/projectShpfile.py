#Opening ESRI shapefile. Return the shapefile driver of file and its layer.		
def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
		print 'Could not open file'
		sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)


# Projecting a shapefile that only have geog. coordinate system but 
# not proj. coordinate system. The proj. cood. sys. is taken from a 
# known or existing projected shapefile.

import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr

# Opening 
file0 = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.shp"
shfileCatch0, layer0 = openingShpFile(file0)
# - Getting the spatial projection
#geoSRlayer0 = layer0.GetSpatialRef()
geoSR = layer0.GetSpatialRef()
wkt = geoSR.ExportToWkt()
print wkt



prjfile = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.prj"
prjfile = "EPSG:4269"
#prjfile = wkt
shpfileBeforeProj = r'E:\Red_deer_SPARROW\RiverNet3\NHNFlowlineCleanUp.shp'
shpfileAfterProj = r'E:\Red_deer_SPARROW\RiverNet3\NHNFlowlineCleanUp_proj.shp'

if os.path.isfile(shpfileAfterProj):
		os.remove(shpfileAfterProj)

# Getting general information of GML file
cmd = 'ogr2ogr -f "ESRI Shapefile" -a_srs ' +  prjfile +' '+ shpfileAfterProj +' '+ shpfileBeforeProj
print cmd
print os.system(cmd) # if is 0 is normal execution