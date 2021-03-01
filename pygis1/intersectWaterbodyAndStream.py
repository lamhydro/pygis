# def lineIntersPoly(layerPoly, layerLine,polyID):
	# featureLine = layerPoint.GetNextFeature()
	# featurePoly  = layerPoly.GetFeature(polyID)
	# geomPoly=featurePoly.GetGeometryRef()
	# #i = 0
	# while featureLine:
	
		
		# geomLine = featureLine.GetGeometryRef()
		# if geomLine.Within(geomPoly):
			# return featureLine.GetField('HydroID')
		# featurePoint.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		# featurePoint = layerPoint.GetNextFeature()

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
from osgeo import ogr
from osgeo import osr
import csv
import numpy as np
import collections

os.chdir("E:\\Red_deer_SPARROW\\RiverNet2")
#os.chdir(r'C:\Users\Luis\Downloads\nhn_rhn_05ck000_shp_en')

# Opening 'HydroEdgeDef.shp'
shfileEdge, EdgeLay = openingShpFile('HydroEdgeDef.shp')
#shfileEdge, EdgeLay = openingShpFile('NHN_05CK000_1_0_HN_NLFLOW_1.shp')
# - Getting the spatial projection
geoSRedge = EdgeLay.GetSpatialRef()
print geoSRedge
print '\n'

# Opening 'NHNWaterbody.shp'
shfileWaBo, WaBoLay = openingShpFile('NHNWaterbody_BIG_LAKES.shp')
#shfileWaBo, WaBoLay = openingShpFile('NHN_05CK000_1_0_HD_WATERBODY_2_BIG_LAKES.shp')
# - Getting the spatial projection
geoSRwabo = WaBoLay.GetSpatialRef()
print geoSRwabo

# Projecting 'NHNWaterbody.shp' into the Spatial Proje. of 'HydroEdgeDef.shp'
# - Creating CoordinateTransformation
coordTrans = osr.CoordinateTransformation(geoSRwabo, geoSRedge)
#prjProjec = osr.SpatialReference()
#prjProjec.ImportFromEPSG(32612) # UTM 12N WGS84
#coordTrans = osr.CoordinateTransformation(geoSRwabo, prjProjec)

lineFea = EdgeLay.GetNextFeature()
#cnt = 0
i = 0
lakesIntersVec = []
laIn = []
lineId = []
while lineFea:
	
	line = lineFea.GetGeometryRef()
	WaBoLay.ResetReading() #need if looping again
	polyFea = WaBoLay.GetNextFeature()
	cnt = 0
	j = 0
	lakesInters = []
	#areaInters = []
	while polyFea:
		poly = polyFea.GetGeometryRef()  
		poly = poly.Clone()  
		poly.Transform(coordTrans)
		#polygonArea = polyCl.GetArea()/(1000000.0)
		#polygonArea = polyFea.GetField('AreaKm2')
		#print 'AREA POL 2431: ', polygonArea, 'km2'
	
		#if line.Crosses(poly):
		if line.Intersect(poly):
			laIn.append(j)
			lakesInters.append(j)
			cnt = cnt + 1
			
		j += 1
					
		polyFea.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		polyFea = WaBoLay.GetNextFeature()

	if len(lakesInters) > 0:
		lakesIntersVec.append(lakesInters)		
		#f.write(str(i)+'\t')
		#for lakeInter in lakesInters:
		#	f.write(str(lakeInter)+'\t')
		#f.write(str(areaTotal)+'\t')
		#f.write('\n')
		lineId.append(i)

	lineFea.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
	lineFea = EdgeLay.GetNextFeature()
	
	print i, cnt
	#if i > 1000:
	#	break
	i += 1
		

counter = collections.Counter(laIn)
freq = counter.values()
keys = counter.keys()
WaBoLay.ResetReading() #need if looping again
i = 0
are = []
for key in keys :
	polyFea = WaBoLay.GetFeature(key)
	are.append(polyFea.GetField('AreaKm2')/freq[i])
	polyFea.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
	#polyFea = WaBoLay.GetNextFeature()
	i += 1

i = 0
areaIntersVec = []
f = open('streamLakeArea.txt', 'w')
f.write('EdgeRow \t' + 'TotalLakeAreakm2 \n')
for liId in lineId:
	areaTotal = 0
	for areaId in lakesIntersVec[i]:
		posi = keys.index(areaId)
		areaTotal +=are[posi]
	f.write(str(liId)+'\t')
	f.write(str(areaTotal)+'\t')
	f.write('\n')
	areaIntersVec.append(areaTotal)	
	i += 1
	
f.close()		

# close the data sources
shfileEdge.Destroy()
shfileWaBo.Destroy()

sys.exit(0)




# Old!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
polyFea= WaBoLay.GetFeature(2431)
poly=polyFea.GetGeometryRef()  
poly = poly.Clone()  
poly.Transform(coordTrans)
polygonArea = poly.GetArea()/(1000000.0)
print 'AREA POL 2431: ', polygonArea, 'km2' 
print poly.GetSpatialReference()

lineFea = EdgeLay.GetFeature(10486)
line = lineFea.GetGeometryRef()
ii=line.Crosses(poly) # HEREEEEEEEEEEEEEEEEEEEEEEE 23 Oct
print int(ii)
sys.exit(0)

# Area of a polygon
# - Creating spatial reference where points are projected
utmSR = osr.SpatialReference()
utmSR.ImportFromEPSG(32612) # UTM 12N WGS84
# - Transforming coordinates
coordTrans = osr.CoordinateTransformation(geoSR, utmSR)
# - Calculating the actual area
polyFea= WaBoLay.GetFeature(2431)
print polyFea.GetField('NID')
poly=polyFea.GetGeometryRef()  
geometryArea = poly.Clone()  
geometryArea.Transform(coordTrans)  
polygonArea = geometryArea.GetArea()/(1000000.0)
print 'AREA POL 977: ', polygonArea, 'km2' 

lineFea = EdgeLay.GetFeature(10486)
print lineFea.GetField('HydroID')
line = lineFea.GetGeometryRef()
ii=poly.Crosses(line) # HEREEEEEEEEEEEEEEEEEEEEEEE 23 Oct
print int(ii)
sys.exit(0)

feature = EdgeLay.GetNextFeature()
cnt = 0
i = 0


while feature:
		geom = feature.GetGeometryRef()
		if geom2.Crosses(geom):
			cnt = cnt + 1
			print i
			
		feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		feature = EdgeLay.GetNextFeature()
		
		i = i + 1

print cnt
sys.exit()

