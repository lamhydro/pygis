#Calculate the great circle distance between two points on the earth (specified in decimal degrees)
def haversine(lon1, lat1, lon2, lat2):
   
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km 

# Getting some attributes from the shapefile layer	
def shapefileAtt(layer):

	# Get Features
	print layer.GetName(), ' contains ', layer.GetFeatureCount(), ' features'
	feature = layer.GetFeature(0)

	# Get Geometry
	geometry = feature.GetGeometryRef()
	print ' Feature contains the Geometry', geometry.GetGeometryName()
	print ' It contains', geometry.GetGeometryCount(), geometry.GetGeometryName()

	# Getting the fields of the features
	layer_defn = layer.GetLayerDefn() #get definitions of the layer
	field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())] #store the field names as a list of strings
	print 'Field names: ', field_names

	# Get the extent as a tuple
	extent = layer.GetExtent()
	print 'Extent:', extent
	print 'UL:', extent[0], extent[3]
	print 'LR:', extent[1], extent[2]

	# Getting the spatial projection
	geoSR = layer.GetSpatialRef()
	print 'Spatial projection:', geoSR

	return geoSR
	
# Read a shape file a get its attributes

import sys, os
#if "C:\\gdalwin32-1.6\\bin" not in sys.path:
#    sys.path.append("C:\\gdalwin32-1.6\\bin")
if "C:\\Python27\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\Lib\\site-packages")
# if "C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\arcpy\\arcpy" not in sys.path:
    # sys.path.append("C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\arcpy\\arcpy")	
from osgeo import ogr
from osgeo import osr
from math import radians, cos, sin, asin, sqrt


os.chdir(r'C:\Users\Luis\Downloads\nhn_rhn_05ck000_shp_en')
file = 'NHN_05CK000_1_0_HN_NLFLOW_1.shp'
driver = ogr.GetDriverByName('ESRI Shapefile')
shapefile = driver.Open(file, 0)
if shapefile is None:
    print 'Could not open file'
    sys.exit(1)

#shapefile = ogr.Open(shapefile)
# Opening a layer
layer = shapefile.GetLayer(0)

# Getting some attributes from the shapefile layer	
geoSR = shapefileAtt(layer)

# Creating spatial reference where points are projected
utmSR = osr.SpatialReference()
utmSR.ImportFromEPSG(32612) # UTM 12N WGS84

# Transforming coordinates
coordTrans = osr.CoordinateTransformation(geoSR, utmSR)


# Reading a second shapefile
file2 = 'NHN_05CK000_1_0_HD_WATERBODY_2.shp'
driver2 = ogr.GetDriverByName('ESRI Shapefile')
shapefile2 = driver2.Open(file2, 0)
if shapefile2 is None:
    print 'Could not open file'
    sys.exit(1)

#shapefile = ogr.Open(shapefile)
# Opening a layer
layer2 = shapefile2.GetLayer(0)

# Getting some attributes from the shapefile layer	
geoSR2 = shapefileAtt(layer2)

feature = layer.GetNextFeature()
feature2 = layer2.GetFeature(2104)

#Calculating the actual area
geom2=feature2.GetGeometryRef()  
geometryArea = geom2.Clone()  
geometryArea.Transform(coordTrans)  
polygonArea = geometryArea.GetArea()/(1000000.0)
print 'AREA POL 2104: ', polygonArea, 'km2' 
#sys.exit()
cnt = 0
i = 0
while feature:
		
		geom2=feature2.GetGeometryRef()
		geom = feature.GetGeometryRef()
		if geom.Within(geom2):
			cnt = cnt + 1
			print i

		
		feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		feature = layer.GetNextFeature()
		
		i = i + 1

print cnt
sys.exit()



# Loop through all of the features
cnt = 0
feature = layer.GetNextFeature()
while feature:
		cnt = cnt + 1
		
		# get the x,y coordinates for the point
		geom = feature.GetGeometryRef()
		#geom.Transform(coordTrans)
		xS = geom.GetX(0)
		yS = geom.GetY(0)
		xE = geom.GetX(geom.GetPointCount()-1)
		yE = geom.GetY(geom.GetPointCount()-1)
		
		
		print str(cnt) + ' ' + str(xS) + ' ' + str(yS)
		print str(cnt) + ' ' + str(xE) + ' ' + str(yE)
		print haversine(xS, yS, xE, yE)*1000 # * 1000 to meters
		#print sqrt((xS-xE)**2 + (yS-yE)**2)
		#print geom.GetGeometryType()
		# write info out to the text file
		#print 'X:' +  str(x) + '-- Y:' +  str(y) 
	  
		feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		feature = layer.GetNextFeature()
	
print 'There are ' + str(cnt) + ' features'   
#layer.ResetReading() #need if looping again

# Also need to close DataSource objects 
# when done with them
shapefile.Destroy()

#layer_defn = layer.GetLayerDefn() #get definitions of the layer

#field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())] #store the field names as a list of strings

#n = 0
#for i in range(layer.GetFeatureCount()):
#    feature = layer.GetFeature(i)
#    name = feature.GetField("NID")
#    geometry = feature.GetGeometryRef()
#    if feature.GetField("ISOLATED"):
#        print i, name, geometry.GetGeometryName()
#        n = n + 1


