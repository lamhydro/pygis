# Opening ESRI shapefile. Return the shapefile driver of file and its layer.		
def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
		print 'Could not open file'
		sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)


# Create a shp file from a *.txt file where the characteristics and the spatial locations of the point features are included.
import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import csv

os.chdir(r'E:\Red_deer_SPARROW\Fluxmaster\Results')

# Opening 'NHNWaterbody.shp' (Read ONLY to get the SPATIAL REFERENCE)
filename = 'E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef'
shfileCatch, CatchLay = openingShpFile(filename+'.shp')
# - Getting the spatial projection
geoSRcatch = CatchLay.GetSpatialRef()
print geoSRcatch

# Opening the csv file with the point feature information
filepath = r'E:\Red_deer_SPARROW\Fluxmaster\Results'
filename = 'predict_flux_all' # 
latCol = 6
lonCol = 7

f = open(filepath + '/' + filename + '.csv', 'rb')
reader = csv.reader(f)

# Create a new data source and layer
driver = ogr.GetDriverByName('ESRI Shapefile')
newfile = filename + '.shp'
if os.path.exists(newfile):
	driver.DeleteDataSource(newfile)
outDS = driver.CreateDataSource(newfile)
if outDS is None:
	print 'Could not create file'
	sys.exit(1)
outLayer = outDS.CreateLayer(filename, geoSRcatch,geom_type=ogr.wkbPoint)

# get the FeatureDefn for the output layer
featureDefn = outLayer.GetLayerDefn()

# Defining a conversion spatial re
point_ref=osr.SpatialReference()
point_ref.ImportFromEPSG(4236) #WG84#
ctran=ogr.osr.CoordinateTransformation(point_ref,geoSRcatch)

rownum = 0
for fields in reader:

	if rownum == 0:
		header = fields
		# use the input FieldDefn to add a field to the out
		i = 0
		for col in header:
			# Warning!: field name has a 12-character limit
			if len(col) > 11: 
				col = col[0:8]+str(i) # add str(i) to differentiate field names
				header[i] = col
			if i==0 or i==1 or i==2 or i==3 or i==4: 
				fldDef = ogr.FieldDefn(col, ogr.OFTString)
				fldDef.SetWidth(30)
			elif i==12 or i==13 or i==16 or i==17 or i==18 or i==19 or i==20 or i==21 or i==22 or i==23 or i==29 or i==30 or i==31 or i==32 or i==33 or i==35 or i==38 or i==44 or i==45 or i==46 or i==47 or i==48 or i==50 or i==53:
				fldDef = ogr.FieldDefn(col, ogr.OFTInteger)
			else:
				fldDef = ogr.FieldDefn(col, ogr.OFTReal)
			outLayer.CreateField(fldDef)
			i += 1
	else:
		[lon,lat,z]=ctran.TransformPoint(float(fields[lonCol]),float(fields[latCol]))
		point = ogr.Geometry(ogr.wkbPoint)
		#point.AddPoint(float(fields[4]),float(fields[3]))
		point.SetPoint_2D(0,lon,lat)
		print fields[lonCol], fields[latCol]
		# create a new feature
		outFeature = ogr.Feature(featureDefn)
		outFeature.SetGeometry(point)
		i = 0
		for field in fields:
			if field != 'NA' and field != '':
				if i==0 or i==1 or i==2 or i==3 or i==4:
					newfield = field
				elif i==12 or i==13 or i==16 or i==17 or i==18 or i==19 or i==20 or i==21 or i==22 or i==23 or i==29 or i==30 or i==31 or i==32 or i==33 or i==35 or i==38 or i==44 or i==45 or i==46 or i==47 or i==48 or i==50 or i==53:
					newfield = int(field)
				else:
					newfield = float(field)
			else:
				newfield = None
			print header[i], "  ",newfield
			outFeature.SetField(header[i], newfield)
			i += 1
		
		# add the feature to the output layer
		outLayer.CreateFeature(outFeature)
		# destroy the features
		#inFeature.Destroy()
		outFeature.Destroy()
		
	#print row
	rownum += 1 
	
# close the data sources
shfileCatch.Destroy()
outDS.Destroy()

		
