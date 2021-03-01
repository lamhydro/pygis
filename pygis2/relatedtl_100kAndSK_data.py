# Opening ESRI shapefile. Return the shapefile driver of file and its layer.		
def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
		print 'Could not open file'
		sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)
	
def getLayerFields(layer):
	print layer
	# Getting the fields of the features
	layer_defn = layer.GetLayerDefn() #get definitions of the layer
	field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())] #store the field names as a list of strings
	print 'Field names: ', field_names

	return field_names
	
def readLayerField(layer,fields):
	feature = layer.GetNextFeature()
	fieldsArray = []
	while feature:
		
		row = []
		for field in fields:
			row.append(feature.GetField(field))
		
		fieldsArray.append(row)
		
		feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		feature = layer.GetNextFeature()

	return fieldsArray


# A shapefiles and *dbf file (relational tables) are used to create a new shapefile that relate the original shapefile and the *.dbf table.
	
import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import numpy as np

os.chdir(r"E:\AAFC Soils Data\SK")

# Opening shapefile
file = 'dtl_100k.shp'
print 'Reading: ', file
shpfile, inLayer = openingShpFile(file)
# - Printing the field names
fields = getLayerFields(inLayer)

# Opening DBF file1
print 'Reading: ', 'SK_data.DBF'
dbfFile1, dbfLayer1 = openingShpFile(r"E:\AAFC Soils Data\SK_data.DBF")
# - Printing the field names
fieldNames_dbf1 = getLayerFields(dbfLayer1)
# - Reading the fields
fieldsArray_dbf1 = readLayerField(dbfLayer1,fieldNames_dbf1)
fieldsArray_dbf1 = np.array(fieldsArray_dbf1)

#sys.exit(0)

# Create a new shapefile
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
while inFeature:


	KSAT_IN_HR = fieldsArray_dbf1[i,13] # cm/h to in/h
	print KSAT_IN_HR, 'in in/h'
	
	# create a new feature
	outFeature = ogr.Feature(featureDefn)
	outFeature.SetGeometry(inFeature.GetGeometryRef())
	
	# Set the field content	
	for field in fields:
		outFeature.SetField(field, inFeature.GetField(field))
	outFeature.SetField('KSAT_IN_HR', KSAT_IN_HR)
		
	# add the feature to the output layer
	outLayer.CreateFeature(outFeature)
	
	# destroy the features
	inFeature.Destroy()
	outFeature.Destroy()
	inFeature = inLayer.GetNextFeature()
	i += 1

# close the data sources
shpfile.Destroy()
dbfFile1.Destroy()
ds.Destroy()
