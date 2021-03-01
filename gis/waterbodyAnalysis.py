def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
			print 'Could not open file'
			sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)
	
def createProjecFromPrjFile(prj_file):
	prj_text = open(prj_file, 'r').read()
	srs = osr.SpatialReference() # Create a spatial referencia
	srs.ImportFromWkt(prj_text)
    #srs.ImportFromWkt(prj_text):
    #    raise ValueError("Error importing PRJ information from: %s" % prj_file)
	return srs	
    #print srs.ExportToProj4()	
	
def getLayerFields(layer):

	# Getting the fields of the features
	layer_defn = layer.GetLayerDefn() #get definitions of the layer
	field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())] #store the field names as a list of strings
	print 'Field names: ', field_names

	return field_names	

import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import csv
import numpy as np

#os.chdir(r'C:\Users\Luis\Downloads\nhn_rhn_05ck000_shp_en')
os.chdir("E:\\Red_deer_SPARROW\\RiverNet2")

# Opening 'NHNWaterbody.shp'
#filename = 'NHN_05CK000_1_0_HD_WATERBODY_2'
filename = 'NHNWaterbody'
shfileWaBo, WaBoLay = openingShpFile(filename+'.shp')
# - Get the fields' names
field_names = getLayerFields(WaBoLay)
# - Getting the spatial projection
geoSRwabo = WaBoLay.GetSpatialRef()
print geoSRwabo

# Creating projection
#prjProjec = createProjecFromPrjFile('NHN_05CK000_1_0_HD_WATERBODY_2.prj')
#print prjProjec
prjProjec = osr.SpatialReference()
prjProjec.ImportFromEPSG(32612) # UTM 12N WGS84
print prjProjec
# - Transforming coordinates
coordTrans = osr.CoordinateTransformation(geoSRwabo, prjProjec)

feature = WaBoLay.GetNextFeature()
cnt = 0
row=[]
i = 0
lakeTotalArea = 0.
lakeArea = [] 
while feature:
	#if feature.GetField('TYPE_TEXT')=='Lake': This exeption does not work since there are big waterbodies classified as non-lakes (maybe reservoirs.)
	if feature.GetField('NID')!='606e18a12b084291b6ce267584b2fbc0' and feature.GetField('NID')!='2667ac95548846b9a888eee93e709eaa' and feature.GetField('NID')!='e6819732f6714b7398024ad332894b0d' and feature.GetField('NID')!='af55fc1aadec4a5c8abe058b51d5b009' and feature.GetField('NID')!='ed9e71cbd06d4e189cba5f9f3928bb4b' and feature.GetField('NID')!='e477c3a1d6324de8afa47057206a9798' and feature.GetField('NID')!='e16c8b22ea55421dac53c3002eafc765' and feature.GetField('NID')!='376d470ee86d43d89357104d7ed381b6' and feature.GetField('NID')!='e819c035fc4d44929cec515ff4db33d3' and feature.GetField('NID')!='c72cd09fb25b4bd0a2fe4dff4546bf85' and feature.GetField('NID')!='52464f91d25f4602bc155284c4af2b66' and feature.GetField('NID')!='b499dcbfe99941a091c516e0bf2681ba' and feature.GetField('NID')!='d448e94290e24ea1b9d77c9ab1a5a877' and feature.GetField('NID')!='b15060a1ba2b4db0962e28e9a711fdfc' and feature.GetField('NID')!='201b1b5ca669476198905ac4636a2d0c' and feature.GetField('NID')!='e068cd2971f149d1b5d7a8fcdcbce38e' and feature.GetField('NID')!='b5720a10f445406b9d2328dae2f132a9' and feature.GetField('NID')!='762ebf4d683f49158c09a9b8358372d7': # All except the rivers.
		poly=feature.GetGeometryRef()  
		poly = poly.Clone()  
		poly.Transform(coordTrans)
		polygonArea = poly.GetArea()/(1000000.0)
		lakeTotalArea = lakeTotalArea + polygonArea
		#print 'AREA POL 2431: ', polygonArea, 'km2'

		if polygonArea > 0.1:
			lakeArea.append(polygonArea)
			row.append(i)
					
	feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
	feature = WaBoLay.GetNextFeature()

	i += 1

print 'TOTAL AREA OF LAKES: ', lakeTotalArea, 'km2'

# create a new data source and layer
driver = ogr.GetDriverByName('ESRI Shapefile')
newfile = filename+'_BIG_LAKES'+'.shp'
if os.path.exists(newfile):
	driver.DeleteDataSource(newfile)
outDS = driver.CreateDataSource(newfile)
if outDS is None:
	print 'Could not create file'
	sys.exit(1)
outLayer = outDS.CreateLayer(filename+'_BIG_LAKES', geoSRwabo,geom_type=ogr.wkbPolygon)
# use the input FieldDefn to add a field to the out
for field in field_names:
	fieldDefn = WaBoLay.GetFeature(0).GetFieldDefnRef(field)
	outLayer.CreateField(fieldDefn)
fldDef = ogr.FieldDefn('AreaKm2', ogr.OFTReal)
outLayer.CreateField(fldDef)
	
# get the FeatureDefn for the output layer
WaBoLay.ResetReading() #need if looping again
featureDefn = outLayer.GetLayerDefn()
# loop through the input features
#cnt = 0
#inFeature = WaBoLay.GetNextFeature()
i = 0
#while inFeature:
for ro in row:
	inFeature  = WaBoLay.GetFeature(ro)
	# create a new feature
	outFeature = ogr.Feature(featureDefn)
	outFeature.SetGeometry(inFeature.GetGeometryRef())
	for field in field_names: 
		outFeature.SetField(field, inFeature.GetField(field))
	outFeature.SetField('AreaKm2', lakeArea[i])
		
	# add the feature to the output layer
	outLayer.CreateFeature(outFeature)
	# destroy the features
	#inFeature.Destroy()
	outFeature.Destroy()
	#inFeature = WaBoLay.GetNextFeature()
	
	i += 1 
	
	
# close the data sources
shfileWaBo.Destroy()
outDS.Destroy()