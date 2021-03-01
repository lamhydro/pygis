import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import csv
import numpy as np

#files = ['CatchmentDef.shp','HydroEdgeDef.shp','HydroJunctionDef.shp']
#names = ['CatchmentDef','HydroEdgeDef','HydroJunctionDef']

os.chdir("E:\\Red_deer_SPARROW\\RiverNet2")

driver = ogr.GetDriverByName('ESRI Shapefile')

# Opening 'CatchmentDef.shp'
shfileCatch= driver.Open('CatchmentDef.shp', 0)
if shfileCatch is None:
	print 'Could not open file'
	sys.exit(1)
# - Opening a layer. 0 indicate the layer 0. Some shpfiles have more than 1	
CatchLay = shfileCatch.GetLayer(0)

# Opening 'HydroEdgeDef.shp'
shfileEdge = driver.Open('HydroEdgeDef.shp', 0)
if shfileEdge is None:
	print 'Could not open file'
	sys.exit(1)
# - Opening a layer. 0 indicate the layer 0. Some shpfiles have more than 1	
EdgeLay = shfileEdge.GetLayer(0)

# Opening 'HydroJunctionDef.shp'
shfileJunc = driver.Open('HydroJunctionDef.shp', 0)
if shfileJunc is None:
	print 'Could not open file'
	sys.exit(1)
# - Opening a layer. 0 indicate the layer 0. Some shpfiles have more than 1	
JuncLay = shfileJunc.GetLayer(0)



#i = 0
#cnt = 0
#featurePoly  = CatchLay.GetFeature(2104)
CatchLay.ResetReading() #need if looping again
featurePoly  = CatchLay.GetNextFeature()
fnode = []
i=0
while featurePoly:
	JuncLay.ResetReading() #need if looping again
	geomPoly=featurePoly.GetGeometryRef()
	featurePoint = JuncLay.GetNextFeature()
	while featurePoint:
		geomPoint = featurePoint.GetGeometryRef()
		if geomPoint.Within(geomPoly):
		#if geomPoly.Contains(geomPoint):
			#cnt = cnt + 1
			#fnode.append(featurePoint.GetField('HydroID'))
			print featurePoint.GetField('HydroID')
			break

		featurePoint.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		featurePoint = JuncLay.GetNextFeature()
	
	featurePoly.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
	featurePoly = CatchLay.GetNextFeature()

	i += 1

#print cnt

#print JuncLay.GetSpatialRef()
#print '\n'
#print CatchLay.GetSpatialRef()



# Also need to close DataSource objects 
# when done with them
shfileCatch.Destroy()
shfileEdge.Destroy()
shfileJunc.Destroy()