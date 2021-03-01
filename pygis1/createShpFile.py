# script to copy first 10 points in a shapefile
# import modules, set the working directory, and get the driver

import ogr, os, sys

os.chdir(r'C:\Users\Luis\Downloads\nhn_rhn_05ck000_shp_en')
driver = ogr.GetDriverByName('ESRI Shapefile')

# open the input data source and get the layer
inDS = driver.Open('NHN_05CK000_1_0_HN_NLFLOW_1.shp', 0)
if inDS is None:
    print 'Could not open file'
    sys.exit(1)
inLayer = inDS.GetLayer()

# create a new data source and layer
if os.path.exists('test.shp'):
    driver.DeleteDataSource('test.shp')
outDS = driver.CreateDataSource('test.shp')
if outDS is None:
    print 'Could not create file'
    sys.exit(1)
outLayer = outDS.CreateLayer('test', geom_type=ogr.wkbLineString)

# Getting the fields of the features
layer_defn = inLayer.GetLayerDefn() #get definitions of the layer
field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())] #store the field names as a list of strings


# use the input FieldDefn to add a field to the output

for fieldname in field_names:
	fieldDefn = inLayer.GetFeature(0).GetFieldDefnRef(fieldname)
	outLayer.CreateField(fieldDefn)

# get the FeatureDefn for the output layer
featureDefn = outLayer.GetLayerDefn()

# loop through the input features
cnt = 0
inFeature = inLayer.GetNextFeature()
while inFeature:

	if inFeature.GetField("ISOLATED") == 0:
		#print inFeature.GetField("ISOLATED")
		
		# create a new feature
		outFeature = ogr.Feature(featureDefn)
		outFeature.SetGeometry(inFeature.GetGeometryRef())
		
		for fieldname in field_names:
			#outFeature.SetField('NID', inFeature.GetField('NID'))
			outFeature.SetField(fieldname, inFeature.GetField(fieldname))
		
		# add the feature to the output layer
		outLayer.CreateFeature(outFeature)
		
		# destroy the features
		inFeature.Destroy()
		outFeature.Destroy()
		
		# increment cnt and if we have to do more then keep looping
		cnt = cnt + 1
		#if cnt < 10: inFeature = inLayer.GetNextFeature()
		#else: break
		
	inFeature = inLayer.GetNextFeature()
	
# close the data sources
inDS.Destroy()
outDS.Destroy()
