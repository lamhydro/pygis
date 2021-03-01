# Opening ESRI shapefile. Return the shapefile driver of file and its layer.		
def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
		print 'Could not open file'
		sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)


# Here is created a copy of a shape file including only one of the original fields.
# Two more fields are included to the copycat shapefile. Sometimes need ArcMap close to run properly.	
	
import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import csv

os.chdir("E:\\Red_deer_SPARROW\\RiverNet2")

# Opening 'CatchmentDef.shp'
src, inLayer = openingShpFile('CatchmentDef.shp')

# create a new data source and layer
driver = ogr.GetDriverByName('ESRI Shapefile')
if os.path.exists('CatchmentDefCopy.shp'):
	driver.DeleteDataSource('CatchmentDefCopy.shp')
ds = driver.CreateDataSource('CatchmentDefCopy.shp')
if ds is None:
	print 'Could not create file'
	sys.exit(1)
outLayer = ds.CreateLayer('CatchmentDefCopy', srs = inLayer.GetSpatialRef(),geom_type=inLayer.GetLayerDefn().GetGeomType())

# use the input FieldDefn to add a field to the output
fieldDefn = inLayer.GetFeature(0).GetFieldDefnRef('HydroID')
outLayer.CreateField(fieldDefn)
fieldDefn = inLayer.GetFeature(0).GetFieldDefnRef('NextDownID')
outLayer.CreateField(fieldDefn)

# New field definitions
fldDef = ogr.FieldDefn('strflowm3s', ogr.OFTReal)
outLayer.CreateField(fldDef)
fldDef = ogr.FieldDefn('acStrflowm3s', ogr.OFTReal)
outLayer.CreateField(fldDef)


cr = csv.reader(open("annualRunoff.csv","rb"))
i =0
streamflow = []
for row in cr:    
	if  i!=0:
		streamflow.append(row[10])
	i += 1

# get the FeatureDefn for the output layer
featureDefn = outLayer.GetLayerDefn()
# loop through the input features
i = 0
inFeature = inLayer.GetNextFeature()
while inFeature:

	# create a new feature
	outFeature = ogr.Feature(featureDefn)
	outFeature.SetGeometry(inFeature.GetGeometryRef())
	
	# Set the field content
	outFeature.SetField('HydroID', inFeature.GetField('HydroID'))
	outFeature.SetField('NextDownID', inFeature.GetField('NextDownID'))
	outFeature.SetField('strflowm3s', float(streamflow[i]))
	# add the feature to the output layer
	outLayer.CreateFeature(outFeature)
	# destroy the features
	inFeature.Destroy()
	outFeature.Destroy()
	inFeature = inLayer.GetNextFeature()
	i += 1

# close the data sources
src.Destroy()
ds.Destroy()
sys.exit()

