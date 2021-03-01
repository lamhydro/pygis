# A shapefiles and *dbf files (relational tables) are used to create a new shapefile that relate the original shapefile and the *.dbf tables.
	
import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import numpy as np

os.chdir(r"E:\AAFC Soils Data\Detailed_Soil_Survey_DSS_Compilations\dss_v3_sk_20130506")

# Opening shapefile
file = 'dss_v3_sk.shp'
print 'Reading: ', file
shpfile, inLayer = openingShpFile(file)
# - Printing the field names
fields = getLayerFields(inLayer)

# Opening DBF file1
print 'Reading: ', 'dss_v3_sk_cmp.dbf'
dbfFile1, dbfLayer1 = openingShpFile("dss_v3_sk_cmp.dbf")
# - Printing the field names
fieldNames_dbf1 = getLayerFields(dbfLayer1)
# - Reading the fields
fieldsArray_dbf1 = readLayerField(dbfLayer1,fieldNames_dbf1)
fieldsArray_dbf1 = np.array(fieldsArray_dbf1)

# Opening DBF file2
print 'Reading: ', 'soil_layer_sk_v2.dbf'
dbfFile2, dbfLayer2 = openingShpFile("soil_layer_sk_v2.dbf")
# - Printing the field names
fieldNames_dbf2 = getLayerFields(dbfLayer2)
# - Reading the fields
fieldsArray_dbf2 = readLayerField(dbfLayer2,fieldNames_dbf2)
fieldsArray_dbf2 = np.array(fieldsArray_dbf2)

# Create a new shapefiel
newfile = file[:-4]+'_dbf.shp'
driver = ogr.GetDriverByName('ESRI Shapefile')
if os.path.exists(newfile):
	driver.DeleteDataSource(newfile)
ds = driver.CreateDataSource(newfile)
if ds is None:
	print 'Could not create file'
	sys.exit(1)
outLayer = ds.CreateLayer(newfile[:-4], srs = inLayer.GetSpatialRef(),geom_type=inLayer.GetLayerDefn().GetGeomType())

# Defining the fields in the newfile outLayer
for field in fields:
	fieldDefn = inLayer.GetFeature(0).GetFieldDefnRef(field)
	outLayer.CreateField(fieldDefn)

# - New field definitions
fieldDefn = ogr.FieldDefn('KSAT_IN_HR', ogr.OFTReal)
outLayer.CreateField(fieldDefn)

# Get the FeatureDefn for the output layer
featureDefn = outLayer.GetLayerDefn()
# loop through the input features
i = 0
inFeature = inLayer.GetNextFeature()
#POLYNUMB1=list(fieldsArray_dbf1[:,1])
#NEW_SYMBOL2=list(fieldsArray_dbf2[:,0])
POLY_ID_List = list(fieldsArray_dbf1[:,0])
PERCENT_List = list(fieldsArray_dbf1[:,2])
SOIL_ID_List = list(fieldsArray_dbf1[:,10])
SOIL_ID_List2 = list(fieldsArray_dbf2[:,0])
LAYER_NO_List = list(fieldsArray_dbf2[:,5])
KSAT_List = list(fieldsArray_dbf2[:,23])

while inFeature:

	POLY_ID = inFeature.GetField('POLY_ID')
	if POLY_ID in POLY_ID_List:
		indices1 = [j for j, x in enumerate(POLY_ID_List) if x == POLY_ID]
		[ float(PERCENT_List[j]) for j in indices1]
		PERCENT = [float(PERCENT_List[j]) for j in indices1]
		SOIL_ID = [SOIL_ID_List[j] for j in indices1]
		KSATav = 0
		for s,p in zip(SOIL_ID,PERCENT):
			idx = [j for j, x in enumerate(SOIL_ID_List2) if (x == s and LAYER_NO_List[j] == '1')]
			#idx = [j for j, x in enumerate(SOIL_ID_List2) if x == s]
			#for id in idx:
			#	LAYER_NO_List[j]
			if idx == []:
				KSATav +=  0*p
			else:
				KSATav +=  float(KSAT_List[idx[0]])*p
		
		if sum(PERCENT) == 0.:
			KSATav = 0.
		else:
			KSATav = KSATav/(sum(PERCENT)*2.54) # cm/h to in/h	
	if KSATav < 0.:
		KSATav = 0.0
	print KSATav, 'in in/h'

	# create a new feature
	outFeature = ogr.Feature(featureDefn)
	outFeature.SetGeometry(inFeature.GetGeometryRef())
	
	# Set the field content	
	for field in fields:
		outFeature.SetField(field, inFeature.GetField(field))
	outFeature.SetField('KSAT_IN_HR', KSATav)
		
	# add the feature to the output layer
	outLayer.CreateFeature(outFeature)
	
	# destroy the features
	inFeature.Destroy()
	outFeature.Destroy()
	inFeature = inLayer.GetNextFeature()
	i += 1
	
	#if i == 10:
	#	break
	

# close the data sources
shpfile.Destroy()
dbfFile1.Destroy()
dbfFile2.Destroy()
ds.Destroy()

