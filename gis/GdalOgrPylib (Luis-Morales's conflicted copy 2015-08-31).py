# GDAL/ORG library
#
# By, LAM, GIWS, Oct. 2013
import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from gdalconst import *
import math
import numpy as np 

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
	
def getLayerFieldTypes(layer):
	print layer
	# Getting the fields of the features
	layer_defn = layer.GetLayerDefn() #get definitions of the layer
	field_types = [layer_defn.GetFieldDefn(i).GetTypeName() for i in range(layer_defn.GetFieldCount())] #store the field names as a list of strings
	print 'Field names: ', field_types

	return field_types	

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

def pointWithinPoly(layerPoly, layerPoint,polyID):
	featurePoint = layerPoint.GetNextFeature()
	featurePoly  = layerPoly.GetFeature(polyID)
	geomPoly=featurePoly.GetGeometryRef()
	while featurePoint:

		geomPoint = featurePoint.GetGeometryRef()
		if geomPoint.Within(geomPoly):
			return featurePoint.GetField('HydroID')

		featurePoint.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		featurePoint = layerPoint.GetNextFeature()
		
# Return the row of a point with (xi,yi) coordinates withing the xlist and ylist lists of coordinates.	
def indexOfXYpointInXYlist(xi,yi,xlist,ylist):
	
	index = 0
	for x,y in zip(xlist,ylist):
		dist = math.sqrt((xi-x)**2 + (yi-y)**2)
		if dist == 0.0:
			return(index)				
		index += 1
		
# Return the row of a point with (xi,yi) coordinates withing the xlist and ylist lists of coordinates.	Same ouput of 'indexOfXYpointInXYlist' but with the procedure use arrays instead.
def indexOfXYpointInXYlist2(xi,yi,xlist,ylist):
	
	dist = np.sqrt((xi-np.array(xlist))**2 + (yi-np.array(ylist))**2)
	index = dist.argmin()
	return(index)

# Transform a shapefile atribute table into a csv file		
def shpFileTableIntoCSV(shpFile, csvFile):

	cmd = 'ogr2ogr -f CSV ' + '"'+csvFile+'"' +' '+ '"'+shpFile+'"'
	print cmd
	print os.system(cmd) # if is 0 is normal execution
	

# Look through the RN to correct(invert FROM_JUNCT and TO_JUNCT) the segment direction.
# Where:
# 	i: FID (first column). Usually an element with a right FROM_JUNCT and TO_JUNCT.
#	it is usually the outlet element of the cathcment. 
#	FROM_JUNCTs: FROM_JUNCT's list of all river network elements.
#	TO_JUNCTs: TO_JUNCT's list of all river network elements.
# The function return a new FROM_JUNCTs and a new TO_JUNCTs lists.
def lookThroughRN(i, FROM_JUNCTs, TO_JUNCTs, listOfele):
	FROM_JUNCT = FROM_JUNCTs[i]
	TO_JUNCT = TO_JUNCTs[i]	
	rowsFJal = [j for j, x in enumerate(TO_JUNCTs) if x == FROM_JUNCT]
	rowsFJ = [j for j, x in enumerate(FROM_JUNCTs) if x == FROM_JUNCT]
	rowsFJ.remove(i)
	
	# Invert direction of elements
	if len(rowsFJ) >= 1:
		for ele in rowsFJ:
			newFROM_JUNCT = TO_JUNCTs[ele] 
			newTO_JUNCT = FROM_JUNCTs[ele] 
			FROM_JUNCTs[ele] = newFROM_JUNCT
			TO_JUNCTs[ele] = newTO_JUNCT 

	allrows = rowsFJal + rowsFJ
	for ele in allrows:
		print ele
		listOfele.append(ele)
		lookThroughRN(ele, FROM_JUNCTs, TO_JUNCTs, listOfele)
	
	return FROM_JUNCTs, TO_JUNCTs, listOfele

# Get (X,Y) coordinated of a points layer.
# 
def getXYcoordPointLayer(layer):
	feature = layer.GetNextFeature()
	xJunct = []
	yJunct = []
	while feature:

		geometry = feature.GetGeometryRef()
		xJunct.append(geometry.GetX())
		yJunct.append(geometry.GetY())
		
		feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		feature = layer.GetNextFeature()
	
	return xJunct, yJunct
	

# Copy a shapefile geometry and modify user's specifics fields
# Where:
# - dir: directory path
# - filename: shape file name 
# - layer: Original layer
# - layerFieldNames: Field names of original layer
# - fielnamesToChange: field names to change
# - fieldvaluesToChange: List of lists of values of those field names to change. 
def copyShpFileModifyUserSpecFields(dir,filename, layer, layerFieldNames, fieldnamesToChange, fieldvaluesToChange):

	## Create a new data source and layer
	driver = ogr.GetDriverByName('ESRI Shapefile')
	print 'herere',driver
	shfileNew = os.path.join(dir,filename)
	if os.path.exists(shfileNew):
		driver.DeleteDataSource(shfileNew)
	ds = driver.CreateDataSource(shfileNew)
	if ds is None:
		print 'Could not create file'
		sys.exit(1)
	outLayer = ds.CreateLayer(filename[:-4], srs = layer.GetSpatialRef(),geom_type=layer.GetLayerDefn().GetGeomType())

	# use the input FieldDefn to add a field to the output
	for layerFieldName in layerFieldNames:
		fieldDefn = layer.GetFeature(0).GetFieldDefnRef(layerFieldName)
		outLayer.CreateField(fieldDefn)

	layer.ResetReading()
	feature = layer.GetNextFeature()
	featureDefn =  outLayer.GetLayerDefn()
	i = 0
	while feature:

		print 'Creating feature No.: ', i

		# create a new feature
		outFeature = ogr.Feature(featureDefn)
		outFeature.SetGeometry(feature.GetGeometryRef())

		# Set the field content
		for layerFieldName in layerFieldNames:	
			if (layerFieldName in fieldnamesToChange):
				idx = fieldnamesToChange.index(layerFieldName)
				outFeature.SetField(layerFieldName, fieldvaluesToChange[idx][i])
			else:
				outFeature.SetField(layerFieldName, feature.GetField(layerFieldName))
			
		# add the feature to the output layer
		outLayer.CreateFeature(outFeature)
		
		# destroy the features
		outFeature.Destroy()
		feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		
		feature = layer.GetNextFeature()
		
		i += 1
		#if i>71:
		#	break
				
	# close the shapefiles
	ds.Destroy()


# Copy a shapefile geometry and add user's specifics fields
# Where:
# - dir: directory path
# - filename: shape file name 
# - layer: Original layer
# - layerFieldNames: List with field names of original layer
# - fieldnamesToAdd: List of lists with field names to change
# - fieldvaluesToAdd: List of lists of values of those field names to change. 
def copyShpFileAddingUserSpecFields(dir,filename, layer, layerFieldNames, fieldnamesToAdd, fieldvaluesToAdd, fieldtypesToAdd):

	## Create a new data source and layer
	driver = ogr.GetDriverByName('ESRI Shapefile')
	print 'herere',driver
	shfileNew = os.path.join(dir,filename)
	if os.path.exists(shfileNew):
		driver.DeleteDataSource(shfileNew)
	ds = driver.CreateDataSource(shfileNew)
	if ds is None:
		print 'Could not create file'
		sys.exit(1)
	outLayer = ds.CreateLayer(filename[:-4], srs = layer.GetSpatialRef(),geom_type=layer.GetLayerDefn().GetGeomType())

	# Add a field to the output
	for layerFieldName in layerFieldNames:
		fieldDefn = layer.GetFeature(0).GetFieldDefnRef(layerFieldName)
		outLayer.CreateField(fieldDefn)
		
	# Add a new fields to the output
	
	for fieldnameToAdd, fieldtypeToAdd in zip(fieldnamesToAdd,fieldtypesToAdd):
		if fieldtypeToAdd == 'real':
			fieldDefn = ogr.FieldDefn(fieldnameToAdd, ogr.OFTReal)
		elif fieldtypeToAdd == 'int':
			fieldDefn = ogr.FieldDefn(fieldnameToAdd, ogr.OFTInteger)
		else:
			fieldDefn = ogr.FieldDefn(fieldnameToAdd, ogr.OFTString)
	
		outLayer.CreateField(fieldDefn)	

		
	layer.ResetReading()
	feature = layer.GetNextFeature()
	featureDefn =  outLayer.GetLayerDefn()
	i = 0
	while feature:

		print 'Creating feature No.: ', i

		# create a new feature
		outFeature = ogr.Feature(featureDefn)
		outFeature.SetGeometry(feature.GetGeometryRef())

		# Set the old field content
		for layerFieldName in layerFieldNames:	
				outFeature.SetField(layerFieldName, feature.GetField(layerFieldName))
				
		# Set new field content
		j = 0	
		for fieldnameToAdd in fieldnamesToAdd:
			outFeature.SetField(fieldnameToAdd, fieldvaluesToAdd[j][i])		
			j += 1	
			
		# add the feature to the output layer
		outLayer.CreateFeature(outFeature)
		
		# destroy the features
		outFeature.Destroy()
		feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		
		feature = layer.GetNextFeature()
		
		i += 1
		#if i>71:
		#	break
				
	# close the shapefiles
	ds.Destroy()	

# Set the NextDownID field. The NextDownID tell to which reach the actual reach go. So if 
# we are in reach i and the NextDownID is j, it means that i goes to j. It is assume that 
# reaches are connected correctly, so the FROM_JUNCTs and TO_JUNCTs are correctly assembled.
# Where:
# - FROM_JUNCTs: list of junctions where the reaches go from
# - TO_JUNCTs: list of junctions where the reaches go to
# - NIDs: list of reach identifiers.
def setNexDownIDinRivNet(FROM_JUNCTs, TO_JUNCTs, NIDs):
	
	i = 1
	NextDownID = []
	for TO_JUNCT in TO_JUNCTs:
		rowsTJal = [j for j, x in enumerate(FROM_JUNCTs) if x == TO_JUNCT]
		print 'hertrt', rowsTJal 
		if len(rowsTJal)>1:
			print 'Bifurcation in: ', i, len(rowsTJal)
			return
		elif len(rowsTJal) == 0:
			NextDownID.append(None)
		else:
			NextDownID.append(NIDs[rowsTJal[0]])
		i+=1
	
	return NextDownID


# Return the unique elements in a list.
# Where:
# - original_list: original list.
# Return the unique list
def make_unique(original_list):
    unique_list = []
    [unique_list.append(obj) for obj in original_list if obj not in unique_list]
    return unique_list

# Asign the Sthraler number equal to 1 to the headwater elements in a river nerwork.
# Where:
# - allrowsFJal: List of lists. Each list contains those elements connected upstream of a element.
# Return the RiverOrder. RiverOrder is equal to 1 if the element is in the headwaters, and None otherwise.	
def headWriverOrderFun(allrowsFJal):
	RiverOrder = []
	for rowsFJal in allrowsFJal:
		if len(rowsFJal)== 0 :
			RiverOrder.append(1)
		else:
			RiverOrder.append(None)
	
	return RiverOrder
	
# Asign the Sthraler number to the streams in a river nerwork.
# Where:
# - RiverOrder: It is equal to 1 if the element is in the headwaters, and None otherwise. This input variable must be the output of "headWriverOrderFun(allrowsFJal)"
# - allrowsFJal: List of lists. Each list contains those elements connected upstream of a element.
# - kk: Counter of the recursion.
# Return the RiverOrder
def riverOrderFun2(allrowsFJal, RiverOrder,kk):

	i = 0
	for ro in RiverOrder:
		if ro == None:
			rowsFJal = allrowsFJal[i]
			rivOr = []
			for k in rowsFJal:
				rivOr.append(RiverOrder[k])
			
			#if sum(rivOr) != None:
			if all(rivOr):
				print i, rivOr
				if len(rivOr) == 1:
					RiverOrder[i] = rivOr[0]
				else:
					rivOr = make_unique(rivOr)
					#print i, rivOr
					if len(rivOr) == 1:
						RiverOrder[i] = rivOr[0] + 1
					else:
						RiverOrder[i] = max(rivOr)
				print '--> ',kk, RiverOrder[i]
				kk += 1
				if kk == 1000: # The number here must be changed to get: all(RiverOrder)=TRUE
					break
				riverOrderFun2(allrowsFJal, RiverOrder, kk)
		i += 1 
			
	return RiverOrder, kk		
	
def riverOrderFun(fus,FROM_JUNCTs, TO_JUNCTs, RiverOrder):
	if fus:
		i = 0
		#RiverOrder = []
		#headwaterIds = []
		for FROM_JUNCT in FROM_JUNCTs:
			rowsFJal = [j for j, x in enumerate(TO_JUNCTs) if x == FROM_JUNCT]
			if len(rowsFJal)== 0 :
				RiverOrder.append(1)
				#headwaterIds.append(i) 
			else:
				RiverOrder.append(None)
			i += 1
	
	fus = 0

	i = 0
	for ro in RiverOrder:
		if ro == None:
			FROM_JUNCT = FROM_JUNCTs[i]
			rowsFJal = [j for j, x in enumerate(TO_JUNCTs) if x == FROM_JUNCT]
			rivOr = []
			print i #,'herer',rowsFJal, ro
			#if i > 1000: return
			for k in rowsFJal:
				rivOr.append(RiverOrder[k])
			#print 'herere', rivOr
			
			#if sum(rivOr) != None:
			if all(rivOr):
				if len(rivOr) == 1:
					RiverOrder[i] = rivOr[0]
				else:
					rivOr = make_unique(rivOr)
					if len(rivOr) == 1:
						RiverOrder[i] = rivOr[0] + 1
					else:
						RiverOrder[i] = max(rivOr)

				riverOrderFun(fus,FROM_JUNCTs, TO_JUNCTs, RiverOrder)
		i += 1 
			
	return RiverOrder

# Merge features in a vector file by common attribute. A new shapefile
# is produces where all features are merged.
# Arguments:
# - infile: Input shapefile. It includes path and filename.
# - outfile: Output shapefile. It includes path and filename.
# - common_attribute: Attribute name. If the aim is to merge 
# all features the same attribute value must be common in all
# features. Empty values are accepted.
def mergeFeatuVectorFile(infile,outfile, common_attribute):
	
	
	# Expliting 'infile'
	inDir, infilename = os.path.split(infile)
	
	# Setting the layer name
	layerName = infilename[:-4]
	
	# Setting the sql expression
	sqlexp = '"'+ 'select ST_union(Geometry),' +  common_attribute + ' from ' + layerName + ' GROUP BY ' + common_attribute + '"'
	
	# Getting information of the original (infile) shape file
	cmd = 'ogrinfo ' + infile + ' -dialect sqlite -sql ' + sqlexp
	print cmd
	print os.system(cmd) # if is 0 is normal execution
	
	# Merging features of the original (infile) shape file. A new 'outfile' is created.
	## Deleting 'outfile' created previously.
	driver = ogr.GetDriverByName('ESRI Shapefile')
	if os.path.exists(outfile):
		driver.DeleteDataSource(outfile)
	cmd ='ogr2ogr -f "ESRI Shapefile" ' + outfile + ' ' + infile + ' -dialect sqlite -sql ' + sqlexp
	print cmd
	print os.system(cmd) # if is 0 is normal execution

def mergeListOfShpfiles(listOfShpfiles, mergedFile, projec):
	
	# listOfShpfiles=[
	# r'E:\Red_deer_SPARROW\GIS2\redDeerRiverCatch.shp',
	# r'E:\GeoBase\NHNBowRiver\nhn_merged\WORKUNIT_LIMIT_2geogAllFea.shp',
	# r'E:\GeoBase\NHNOldmanRiver\nhn_merged\WORKUNIT_LIMIT_2geogAllFea.shp',
	# r'E:\GeoBase\NHNSouthSaskRiver\nhn_merged\WORKUNIT_LIMIT_2geogAllFea.shp'
	# ]
	# mergedFile = r'E:\SaskRiv_SPARROW\GenMaps\SouthSaskRivBasin.shp'
	# projec = 1

	# Expliting 'mergedFile'
	dir, nameMergedFile = os.path.split(mergedFile)
	
	## if file exists, delete it ##
	if os.path.isfile(mergedFile):
			os.remove(mergedFile)

			
	i = 0
	for file in listOfShpfiles:
		print file
		
		# Create the main file
		if i == 0:
			cmd = 'ogr2ogr ' + mergedFile + ' ' + file
			print os.system(cmd)
		# Merge (append) 'file' to the 'main' file
		else:
			cmd = 'ogr2ogr -update -append ' + mergedFile + ' ' + file + ' -nln ' + nameMergedFile[:-4] 
			print os.system(cmd)
		
		i += 1

	# If the file does not have coord. sys.
	if projec:

		coordSys='EPSG:4269' # for NAD83 coord sys

		mergedFileGeo = os.path.join(dir, nameMergedFile[:-4]+'_proj.shp')
		## if file exists, delete it ##
		if os.path.isfile(mergedFileGeo):
			os.remove(mergedFileGeo)
			
		# Setting up the coord. sys.
		cmd = 'ogr2ogr -f ' + '"ESRI Shapefile"'+ ' -a_srs ' + coordSys + ' ' + mergedFileGeo + ' ' + mergedFile
		print os.system(cmd)

# Clip a raster file with the bounding box of a shape file.	
# - rasterIn: raster file to be clipped. Dir + filename.
# - shpfile: Shapefile to clipp the raster file.
# - rasterOut: clipped raster by the shpfile bounding box.
def clippingRasterFilewithShapefile(rasterIn,shpfile,rasterOut):
	# Opening the projected shapefile
	#shpfile = r'E:\GeoBase\CDED\redDeerRiverDEM\redDeerRiverCatchPrXY\redDeerRiverCatch.shp'
	shfile, layer = openingShpFile(shpfile)

	# Get the extension
	extent = layer.GetExtent()
	print extent

	# Reading the raster
	# register all of the drivers
	gdal.AllRegister()
	# open the image
	#rasterIn = r'E:\Runoff\runoff_14_r30_PrXY.tif'
	#rasterOut = r'E:\Runoff\runoff_14_r30_PrXY_redDeer.tif'
	ds = gdal.Open(rasterIn)
	if ds is None:
		print 'Could not open image'
		sys.exit(1)
	print '\n \n'
	demWKT = ds.GetProjectionRef()
	print 'Spatial projection:', demWKT

	geotransform = ds.GetGeoTransform()
	print geotransform

	# Cliping the raster
	cmd = 'gdal_translate' + ' -projwin ' + str(extent[0]) + ' ' + str(extent[3]) + ' ' + str(extent[1]) + ' ' + str(extent[2]) + ' -of GTiff ' + rasterIn + ' ' + rasterOut
	print cmd
	print os.system(cmd) # if is 0 is normal execution
	
# Clipping a raster file with the contour of a polygon.
# - rasterIn: raster file to be clipped. Dir + filename.
# - shpfile: Shapefile to clip the raster file. Dir + filename.
# - rasterOut: clipped raster by the shpfile bounding box. Dir + filename.
def clippingRasterFilewithShapefile2(rasterIn,shpfile,rasterOut):
	## if file exists, delete it ##
	if os.path.isfile(rasterOut):
			os.remove(rasterOut)

	# Cliping raster with other polygon
	print 'Clipping raster file with a polygon'
	print ''
	#cmd = 'gdalwarp -dstnodata 0 '+' -cutline ' +  shpfile + ' -crop_to_cutline -dstalpha ' + rasterIn + ' ' + rasterOut
	cmd = 'gdalwarp -dstnodata -99999 '+' -cutline ' +  shpfile + ' ' + rasterIn + ' ' + rasterOut
	print cmd
	print os.system(cmd) # if is 0 is normal execution


	

# Create a copy of shapefile deleting specific features listed in 'FIDofFeatToDelete'
# - dir: directory path
# - filename: shape file name 
# - layer: Original layer
# - FIDofFeatToDelete: List of FID of features to delete.
def deletingFeatureOfShpFile(dir,filename, layer, layerFieldNames, FIDofFeatToDelete):

	## Create a new data source and layer
	driver = ogr.GetDriverByName('ESRI Shapefile')
	print 'herere',driver
	shfileNew = os.path.join(dir,filename)
	if os.path.exists(shfileNew):
		driver.DeleteDataSource(shfileNew)
	ds = driver.CreateDataSource(shfileNew)
	if ds is None:
		print 'Could not create file'
		sys.exit(1)
	outLayer = ds.CreateLayer(filename[:-4], srs = layer.GetSpatialRef(),geom_type=layer.GetLayerDefn().GetGeomType())

	# Add a field to the output
	for layerFieldName in layerFieldNames:
		fieldDefn = layer.GetFeature(0).GetFieldDefnRef(layerFieldName)
		outLayer.CreateField(fieldDefn)
		
		
	layer.ResetReading()
	feature = layer.GetNextFeature()
	featureDefn =  outLayer.GetLayerDefn()
	i = 0
	while feature:
	
		if i not in FIDofFeatToDelete:

			print 'Creating feature No.: ', i

			# create a new feature
			outFeature = ogr.Feature(featureDefn)
			outFeature.SetGeometry(feature.GetGeometryRef())

			# Set the old field content
			for layerFieldName in layerFieldNames:	
					outFeature.SetField(layerFieldName, feature.GetField(layerFieldName))
					
				
			# add the feature to the output layer
			outLayer.CreateFeature(outFeature)
			
			# destroy the features
			outFeature.Destroy()
		
		feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
			
		feature = layer.GetNextFeature()
			
		i += 1
			#if i>71:
			#	break
				
	# close the shapefiles
	ds.Destroy()

# Project a shapefile into geographical coordinates (X and y). It will produce a new shapefile 'fn' projected into XY coord.
# - workDir: working directory path
# - file0: Shapefile with the XY projection system(shpefile already projected!). It must include directory, usually: file0 = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.shp"
# - inDirFilename: directory and name of the input shapefile.
# - fn: Output shapefile name. It is saved into 'workDir'.
# - typeOfGeom: Type of geometry in the shapefile: 'point', 'line', 'polygon'
def projectShpfileIntoXY(workDir, file0, inDirFilename, fn, typeOfGeom):
	# set the working directory
	#workDir = "E:\\Documents\\NutrientsLecture2\\Maps"
	os.chdir(workDir)
	 
	# get the shapefile driver
	driver = ogr.GetDriverByName('ESRI Shapefile')

	# create the input SpatialReference
	inSpatialRef = osr.SpatialReference()
	inSpatialRef.ImportFromEPSG(4269)

	# Opening 
	#file0 = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.shp"
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
	coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

	# open the input data source and get the layer
	#inDirFilename = r'E:\Documents\NutrientsLecture2\Maps\Catchment.shp'
	inDS = driver.Open(inDirFilename, 0)
	if inDS is None:
	  print 'Could not open file'
	  sys.exit(1)
	inLayer = inDS.GetLayer()

	# create a new data source and layer
	#fn = 'NLFLOW_1geog_MiryCreekV2_proj.shp'
	#fn = 'Catchment_proj.shp'
	if os.path.exists(fn):
	  driver.DeleteDataSource(fn)
	outDS = driver.CreateDataSource(fn)
	if outDS is None:
	  print 'Could not create file'
	  sys.exit(1)
	#outLayer = outDS.CreateLayer('NLFLOW_1geog_MiryCreekV2_proj', outSpatialRef, geom_type=ogr.wkbLineString)
	if typeOfGeom == 'point':
		outLayer = outDS.CreateLayer(fn[:-4], outSpatialRef, geom_type=ogr.wkbPoint)
	elif typeOfGeom == 'line':
		outLayer = outDS.CreateLayer(fn[:-4], outSpatialRef, geom_type=ogr.wkbLineString)
	elif typeOfGeom == 'polygon':
		outLayer = outDS.CreateLayer(fn[:-4], outSpatialRef, geom_type=ogr.wkbPolygon)
	else:
		print 'Could not project file'
		sys.exit(1)
	#outLayer = outDS.CreateLayer(fn[:-4], outSpatialRef, geom_type=ogr.wkbPolygon)


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
	k = 0
	while inFeature:
	
	  print 'Projection into XY coord feature No.: ', k

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
	  
	  k += 1

	# Close the shapefiles
	inDS.Destroy()
	outDS.Destroy()

	# create the *.prj file
	outSpatialRef.MorphToESRI()
	#open('redDeerRiverNHN_proj.prj', 'w')
	file = open(fn[:-4]+'.prj','w')#open('redDeerRiverNHN_proj.prj', 'w')
	file.write(outSpatialRef.ExportToWkt())
	file.close()

# Estimate the length of features in a Line-type shapefile.
# - dir: directory path
# - filename: shape file name 
def getLengthOfLineFeatures(dir,filename):

	# Opening the shape file
	shpfile = os.path.join(dir,filename)
	shfile, layer = openingShpFile(shpfile)
	
	# Estimating the lenght
	feature = layer.GetNextFeature()
	i = 0
	length = []
	while feature:
	
		print 'Getting the lenght of: ', i
		
		geometry = feature.GetGeometryRef()
		
		length.append(geometry.Length()) # Length
		
		feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
			
		feature = layer.GetNextFeature()
			
		i += 1
		
	# close the shapefile
	shfile.Destroy()
	
	return length
	
# Clipp a shape file with another shapefile. The clipper is usually a polygon shape file with only one feature.
# - clipshape: Shpfile with the feature to clip.
# - inshape: Shpfile to be clipped.
# - outshape: Resultiog shapefile.
def clippShpfileWithAnother(clipshape, inshape, outshape): # DOES NOT WORK!!!!!!!
	#clipshape = r'E:\Red_deer_SPARROW\GIS\redDeerRiverCatch.shp'
	#inshape   = r'E:\InterpolatedCensusofAgriculture\aafc_interpolated_coaSHPfiles\CEN_CA_AG_SLC_PRD_2001_aux_proj.shp'
	#outshape  = r'E:\InterpolatedCensusofAgriculture\aafc_interpolated_coaSHPfiles\CEN_CA_AG_SLC_PRD_2001_aux_proj_RedDeer.shp'
	cmd = 'ogr2ogr -clipsrc ' + '"'+clipshape + '" '+'"' + outshape + '" ' +'"'+ inshape+'"'
	print cmd
	print os.system(cmd) # if is 0 is normal execution