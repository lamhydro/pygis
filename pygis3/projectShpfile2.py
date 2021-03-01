#Opening ESRI shapefile. Return the shapefile driver of file and its layer.		
def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
		print 'Could not open file'
		sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)

# import modules
import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal
from osgeo import ogr
from osgeo import osr

# set the working directory
workDir = r"W:\Luis\Colin_QuAppelle\effective_areas"
os.chdir(workDir)
 
# get the shapefile driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# open the input data source and get the layer
#inDS = driver.Open(r'E:\Documents\NutrientsLecture2\Maps\NLFLOW_1geog_MiryCreekV2.shp', 0)
inDS = driver.Open('effective_area.shp', 0)
if inDS is None:
  print 'Could not open file'
  sys.exit(1)
inLayer = inDS.GetLayer()

# create the input SpatialReference
inSpatialRef = osr.SpatialReference()
#inSpatialRef = inLayer.GetSpatialRef()
print inSpatialRef.ExportToWkt()
#inSpatialRef.SetWellKnownGeogCS("NAD83")
inSpatialRef.SetWellKnownGeogCS("WGS84")
#inSpatialRef.ImportFromEPSG(4269)

# Opening 
file0 = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.shp"
shfileCatch0, layer0 = openingShpFile(file0)
# - Getting the spatial projection
#geoSRlayer0 = layer0.GetSpatialRef()
geoSR = layer0.GetSpatialRef()
wkt = geoSR.ExportToWkt()
print wkt# create the output SpatialReference
outSpatialRef = osr.SpatialReference()
outSpatialRef.ImportFromWkt(wkt)
#geoSRop.ImportFromWkt(demWKT)

# create the CoordinateTransformation
coordTrans = osr.CoordinateTransformation(inSpatialRef, geoSR)



# create a new data source and layer
#fn = 'NLFLOW_1geog_MiryCreekV2_proj.shp'
fn = 'effective_area_proj.shp'
if os.path.exists(fn):
  driver.DeleteDataSource(fn)
outDS = driver.CreateDataSource(fn)
if outDS is None:
  print 'Could not create file'
  sys.exit(1)
#outLayer = outDS.CreateLayer('NLFLOW_1geog_MiryCreekV2_proj', outSpatialRef, geom_type=ogr.wkbLineString)
outLayer = outDS.CreateLayer('effective_area_proj', outSpatialRef, geom_type=ogr.wkbPolygon)


# Getting the fields of the features
layer_defn = inLayer.GetLayerDefn() #get definitions of the layer
field_names = [layer_defn.GetFieldDefn(i).GetName() for i in range(layer_defn.GetFieldCount())] #store the field names as a list of strings


# use the input FieldDefn to add a field to the output
for fieldname in field_names:
	fieldDefn = inLayer.GetFeature(0).GetFieldDefnRef(fieldname)
	outLayer.CreateField(fieldDefn)

# # get the FieldDefn for the county name field
# feature = inLayer.GetFeature(0)
# fieldDefn = feature.GetFieldDefnRef('NID')

# # add the field to the output shapefile
# outLayer.CreateField(fieldDefn)

# get the FeatureDefn for the output shapefile
featureDefn = outLayer.GetLayerDefn()

# loop through the input features
inFeature = inLayer.GetNextFeature()
while inFeature:

  # get the input geometry
  geom = inFeature.GetGeometryRef()
  #print geom.GetGeometryName() # Getting the type of geometry

  # reproject the geometry
  geom.Transform(coordTrans)

  # create a new feature
  outFeature = ogr.Feature(featureDefn)
 
  # set the geometry and attribute
  outFeature.SetGeometry(geom)
 
  # Set attribute 
  for fieldname in field_names:
	outFeature.SetField(fieldname, inFeature.GetField(fieldname))

  #outFeature.SetField('NID', inFeature.GetField('NID'))

  # add the feature to the shapefile
  outLayer.CreateFeature(outFeature)

  # destroy the features and get the next input feature
  outFeature.Destroy
  inFeature.Destroy
  inFeature = inLayer.GetNextFeature()

# Close the shapefiles
inDS.Destroy()
outDS.Destroy()

# create the *.prj file
#outSpatialRef.MorphToESRI()
#file = open('NLFLOW_1geog_MiryCreekV2_proj.prj','w')#open('redDeerRiverNHN_proj.prj', 'w')
#file = open('effective_area_proj.prj','w')#open('redDeerRiverNHN_proj.prj', 'w')
#file.write(outSpatialRef.ExportToWkt())
#file.close()