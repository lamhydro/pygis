# GDAL/ORG library
#
# By, LAM, GIWS, Oct. 2013
import sys, os
#if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
#    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from gdalconst import *
import math
import numpy as np 
import csv
from scipy import interpolate

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


# Export attribute table from shapefile. 
# Input: shapefile name
# Output: *.csv file with attribute table.	
def exportAttTableShp(file):
    # Opening the river shapefile
    #file = 'HydatStLocQA_proj.shp'
    shfile, layer = openingShpFile(file)
    
    # Reading field names
    fieldnames = getLayerFields(layer)
    
    # Reading field
    fields = readLayerField(layer,fieldnames)
    
    with open(file[:-4]+'_attTable.csv', "wb") as ofile:
        writer = csv.writer(ofile)
        writer.writerow(fieldnames)
        for l in fields:
            writer.writerow(l)	
 
# Get the extent (Bounding box) of a shape file and return the [xmin,ymin,xmax,ymax]
# - shapefile: filename including path.
# - if adjust is true, a 2% is added to the BBox
def BBoxOfShapeFile(shapefile,adjust):
    shfile, layer = openingShpFile(shapefile)
    extent = layer.GetExtent()
    shfile.Destroy()
    if adjust:
        return ([1.01*extent[0],0.99*extent[2],0.99*extent[1],1.01*extent[3]])
    else:
        return ([extent[0],extent[2],extent[1],extent[3]]) 

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
	
# Get the streams conected sequentially donwstream an stream i. The recursive
# function usually stop at the cathcment outlet stream.
# Where:
# 	i: FID of the stream.
#	FROM_JUNCTs: FROM_JUNCT's list of all river network elements.
#	TO_JUNCTs: TO_JUNCT's list of all river network elements.
#   listOfStreams: List of the streams FID conected downstream. Returned by the function
def getConnectedStreams(i,FROM_JUNCTs, TO_JUNCTs, listOfStreams):
	TO_JUNCT = TO_JUNCTs[i]
	if TO_JUNCT in FROM_JUNCTs:
		index = FROM_JUNCTs.index(TO_JUNCT)
		listOfStreams.append(index)
		getConnectedStreams(index,FROM_JUNCTs, TO_JUNCTs, listOfStreams)
	
	return listOfStreams
	
# Get the streams conected sequentially between a upstreamd and a downstream
# Where:
# 	upstream: FID of upstream.
# 	upstream: FID of downstream.
#	FROM_JUNCTs: FROM_JUNCT's list of all river network elements.
#	TO_JUNCTs: TO_JUNCT's list of all river network elements.
#   listOfStreams: List of the streams FID conected downstream. Returned by the function
def getConnectedStreamsBetweenUpstreamAndDownstream(upstream, downstream, FROM_JUNCTs, TO_JUNCTs,  listOfStreams):
	TO_JUNCT = TO_JUNCTs[upstream]
	if TO_JUNCT in FROM_JUNCTs:
		index = FROM_JUNCTs.index(TO_JUNCT)
		#print index
		listOfStreams.append(index)
		if index == downstream:
			return listOfStreams
		else:
			getConnectedStreamsBetweenUpstreamAndDownstream(index, downstream, FROM_JUNCTs, TO_JUNCTs,  listOfStreams)
	
	return listOfStreams
		
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
			#print fieldnameToAdd, fieldvaluesToAdd[j][i]
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
    if common_attribute == ' ':
        sqlexp = '"'+ 'SELECT ST_Union(Geometry) AS geometry FROM ' + layerName + '"'
    else:
        sqlexp = '"'+ 'select ST_union(Geometry),' +  common_attribute + ' from ' + layerName + ' GROUP BY ' + common_attribute + '"'
        
    # Getting information of the original (infile) shape file
    #cmd = 'ogrinfo ' + infile + ' -dialect sqlite -sql ' + sqlexp
    #print cmd
    #print os.system(cmd) # if is 0 is normal execution
    
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
			cmd = 'ogr2ogr ' + ' "' + mergedFile + '" '  + ' "'+  file + '" '
			print cmd
			print os.system(cmd)
		# Merge (append) 'file' to the 'main' file
		else:
			cmd = 'ogr2ogr -update -append ' + ' "' + mergedFile + '" '  + ' "'+  file + '" ' + ' -nln ' + nameMergedFile[:-4]
			print cmd
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
		print cmd
		print os.system(cmd)

# Clip a raster file with the bounding box of a shape file.	
# - rasterIn: raster file to be clipped. Dir + filename.
# - shpfile: Shapefile to clipp the raster file.
# - rasterOut: clipped raster by the shpfile bounding box.
def clippingRasterFilewithShapefile(rasterIn,shpfile,rasterOut,offset):
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
	cmd = 'gdal_translate' + ' -projwin ' + str(extent[0]-offset) + ' ' + str(extent[3]+offset) + ' ' + str(extent[1]+offset) + ' ' + str(extent[2]-offset) + ' -of GTiff ' + rasterIn + ' ' + rasterOut
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
	#cmd = 'gdalwarp --config GDALWARP_IGNORE_BAD_CUTLINE YES -dstnodata -99999 '+' -cutline ' +  shpfile + ' ' + rasterIn + ' ' + rasterOut 
	cmd = 'gdalwarp -dstnodata -99999 '+' -cutline ' +  shpfile + ' ' + rasterIn + ' ' + rasterOut # This one works fine for MS WIN
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
	print 'here', coordTrans

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
	  #print coordTrans

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
	
# Project a shapefile into geographical coordinates (X and y). It will produce a new shapefile 'fn' projected into XY coord.
# - workDir: working directory path
# - file0: Shapefile with the XY projection system(shpefile already projected!). It must include directory, usually: file0 = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.shp"
# - inDirFilename: directory and name of the input shapefile.
# - fn: Output shapefile name. It is saved into 'workDir'.
# - typeOfGeom: Type of geometry in the shapefile: 'point', 'line', 'polygon'
# NOTE: this new version of this function does not create a new spatial reference from EPSG, but take the spatial projection from the inDirFilename to create the new spatial reference.
def projectShpfileIntoXY_New(workDir, file0, inDirFilename, fn, typeOfGeom):
	# set the working directory
	#workDir = "E:\\Documents\\NutrientsLecture2\\Maps"
	os.chdir(workDir)
	 
	# get the shapefile driver
	driver = ogr.GetDriverByName('ESRI Shapefile')

	# create the input SpatialReference
	#inSpatialRef = osr.SpatialReference()
	#inSpatialRef.ImportFromEPSG(4269)

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

	# open the input data source and get the layer
	#inDirFilename = r'E:\Documents\NutrientsLecture2\Maps\Catchment.shp'
	inDS = driver.Open(inDirFilename, 0)
	if inDS is None:
	  print 'Could not open file'
	  sys.exit(1)
	inLayer = inDS.GetLayer()
	geoSR = inLayer.GetSpatialRef()
	wkt = geoSR.ExportToWkt()
	inSpatialRef = osr.SpatialReference()
	inSpatialRef.ImportFromWkt(wkt)
	
	# create the CoordinateTransformation
	coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
	print 'here', coordTrans	

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
	  #print coordTrans

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
	
# Accumulating atributes of areas throug a River network
# - HydroID: Indentification number of a shapefile feature (usually a polygon)
# - HydroIDS: List of HydroID for all the shapefile features
# - NextDownID: Conectivity between features. So this is a list with the elements that
#   are downstream, so that every HydroID have a downstream element.
# - Att: List of attributes (e.g. poly areas) tha are going to be accumulated.
# - accVar: Accumulated value of Att at the HydroID feature.
def accumuThrouhtNetwork(HydroID,HydroIDS,NextDownID,Att, accVar):
	rows = [j for j, x in enumerate(NextDownID) if x == HydroID]
	dummy = []
	for row in rows:
		dummy.append(Att[row])
	
	#deraccVar=sum(dummy)
	accVar +=sum(dummy)

	for row in rows:
		HydroID=HydroIDS[row]
		#print 'here',row,HydroID
		accVar+=accumuThrouhtNetwork(HydroID,HydroIDS,NextDownID,Att, 0)
		
	return accVar
 
 # Compute the centroid of polygon features in a polygon shape file.
# - file: Polygon shape file. Unprojected or projected.
# - polyID: Field within the shape file to indentify the polygons.
# - outFile: '*.csv' file where the polyID, centroid_x and centroid_y are saved.
def centroidPolyShpFile(file, polyID, outFile):
    
    # Opening shapefile
    shfile, layer = openingShpFile(file)

    with open(outFile,'w') as f1:
        writer=csv.writer(f1, delimiter=',',lineterminator='\n')
        writer.writerow(['FID', polyID, 'CEN_X', 'CEN_Y'])        
        feature = layer.GetNextFeature()
        i = 0
        while feature:
            
             poly = feature.GetGeometryRef()
             # Ignoring empty polygons
             if poly !=None:
                 # Getting poly identification
                 pID = feature.GetField(polyID)             
                 
                 # Getting the centroid
                 centroid = poly.Centroid()
                 x = centroid.GetX()
                 y = centroid.GetY()
    
                 # Print on screen
                 print "i", i, pID, x, y
                 
                 # Prind into file
                 writer.writerow([i,pID,x,y])
            
             # destroy the features
             feature.Destroy()
             feature = layer.GetNextFeature()
             
             i += 1
        
        
        # close the data sources
        shfile.Destroy()

# Write a Numpy array to raster file (*.tif)
# - lon: 1D array of longitudes
# - lat: 1D array of latitudes
# - array: 2D array
# - filename: file name of the raster file
# - proj: Projection of the raster file. It must not ve UTM is data is in lat and lon.        
def writeNumpyArrayToRaster(lon, lat, array, filename,NoDataValue,proj):
    ## if file exists, delete it ##
    if os.path.isfile(filename):
        os.remove(filename)
   
    xmin,ymin,xmax,ymax = [lon.min(),lat.min(),lon.max(),lat.max()]
    nrows,ncols = np.shape(array)
    xres = (xmax-xmin)/float(ncols)
    yres = (ymax-ymin)/float(nrows)
    geotransform=([xmin,xres,0,ymax,0, -yres])
    #print geotransform
    # That's (top left x, w-e pixel resolution, rotation (0 if North is up), 
    #         top left y, rotation (0 if North is up), n-s pixel resolution)
    # I don't know why rotation is in twice???
    
    output_raster = gdal.GetDriverByName('GTiff').Create(filename,ncols, nrows, 1 ,gdal.GDT_Float32)  # Open the file
    
    output_raster.SetGeoTransform(geotransform)  # Specify its coordinates
    #srs = osr.SpatialReference()                 # Establish its coordinate encoding
    #srs.ImportFromEPSG(EPSGproj)                     # This one specifies WGS84 lat long.
                                                 # Anyone know how to specify the 
                                                 # IAU2000:49900 Mars encoding?
    #output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system 
                                                       # to the file
    output_raster.SetProjection(proj)
    outBand = output_raster.GetRasterBand(1)
    outBand.WriteArray(array)   # Writes my array to the raster    
    outBand.SetNoDataValue(NoDataValue)
    outBand.FlushCache()
    outBand.GetStatistics(0, 1)
    
    
# Project raster file
# - inRaster: unprojected raster file
# - outRaster: projected raster file
# - proj: Projection information. Usually from a proj. raster. 
def projectRaster(inRaster, outRaster, proj):
    #outdir = "Z:\\Luis\\PCIC\\"
    #inRaster = outdir + 'test.tif' 
    #outRaster = outdir + 'test_prj.tif' 
    cmd = 'gdalwarp -overwrite' + ' -t_srs ' + '"'+proj +'"'+ ' ' + inRaster + ' ' + outRaster
    print cmd
    print os.system(cmd) # if is 0 is normal execution
    #os.system(cmd)
    
# Getting the projection of a shape file.
# - filename: shape file name, including the path.
def getShpFileProj(filename):
    #file = 'E:\\SouthSaskRiv_SPARROW\\RivNet3\\CatchmentDemFillV1_proj.shp'
    shfile, layer = openingShpFile(filename)
    geoSR = layer.GetSpatialRef()
    proj = geoSR.ExportToWkt()
    shfile.Destroy()
    return proj  
    
# Return the bounding box of a raster.
# rasterfile: name of the raster file.     
def XminYminXmaxYmax_raster(rasterfile):
    
    dataset = gdal.Open(rasterfile, GA_ReadOnly)
    if dataset is None:
        print 'Could not open file'
        sys.exit(1)
    
    # Raster characteristics    
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize    
    geotransform = dataset.GetGeoTransform()
    #originX = geotransform[0]
    #originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    
    # Raster dimensions
    xmin = geotransform[0]
    ymin = geotransform[3]-pixelHeight*rows
    xmax = geotransform[0]+pixelWidth*cols
    ymax = geotransform[3]
    
    # Close raster file    
    dataset = None
    
    return ([xmin, ymin, xmax, ymax])

# Resampling a raster (DO NOT WORK!!!!)
# - rasterIn: input raster name
# - rasterOut: name of the resampled raster
# - rasterDim: xmin ymin xmax and ymax of a raster e.g. '-76.1800000 2.8100000 -74.4000000 5.3700000'           
# - xres: x resolution of resampling
# - yres: y resolution of resampling    
def resamplingRaster(rasterIn, rasterOut, rasterDim, xres, yres):
    
    cmd = 'gdalwarp -ts ' + xres + ' '+ yres + ' -r "cubic" -te ' + rasterDim + ' ' + rasterIn + ' ' + rasterOut 
    print cmd
    print os.system(cmd) # if is 0 is normal execution 
    
# Get the limits to clip a geospatial array.
# - lat: array with lat coordinates of the data array 
# - lon: array with lon coordinates of the data array
# - limits: list of [xmin, ymin, xmax, ymax]     
def limToclip2DArray(lat,lon,limits):
    dummy = list(abs(lat-limits[1]))
    minLatId = dummy.index(min(dummy))
    dummy = list(abs(lat-limits[3]))
    maxLatId = dummy.index(min(dummy))
    
    dummy = list(abs(lon-limits[0]))
    minLonId = dummy.index(min(dummy))
    dummy = list(abs(lon-limits[2]))
    maxLonId = dummy.index(min(dummy))
    
    return([minLonId, maxLonId+1, minLatId, maxLatId+1])    
    #clip_lat = lat[minLatId:maxLatId+1]
    #clip_lon = lat[minLonId:maxLonId+1]
    
    #clip_data =  clip_data[minLonId:maxLonId+1,minLatId:maxLatId+1]    

    #return([clip_lat, clip_lon, clip_data])    

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')
    
    
def plotMultipleMaps(lon,lat, data_dec, var, data_units):
    # Get some parameters for the Stereographic Projection
    lon_0 = lon.mean()
    lat_0 = lat.mean()
    #m = Basemap(width=5000000,height=3500000,
    #            resolution='l',projection='stere',\
    #            lat_ts=40,lat_0=lat_0,lon_0=lon_0)
    
    # projection, lat/lon extents and resolution of polygons to draw
    # resolutions: c - crude, l - low, i - intermediate, h - high, f - full
    # ll (lower left) ur (upper right)
    m = Basemap(projection='merc',llcrnrlon=lon.min(),llcrnrlat=lat.min(),urcrnrlon=lon.max(),urcrnrlat=lat.min(),resolution='i') 
                
    # Because our lon and lat variables are 1D, 
    # use meshgrid to create 2D arrays 
    # Not necessary if coordinates are already in 2D arrays.
    lons, lats = np.meshgrid(lon, lat)
    xi, yi = m(lons, lats)  
    
    for i in range(len(data_dec)):
        plt.figure()
        # Plot Data
        cs = m.pcolor(xi,yi,np.squeeze(data_dec[i]))
        
        # Add Grid Lines
        m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
        m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)
        
        # Add Coastlines, States, and Country Boundaries
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()
        
        # Add Colorbar
        cbar = m.colorbar(cs, location='bottom', pad="10%")
        cbar.set_label(data_units)
        
        # Add Title
        plt.title(var)
        
        plt.show() 
        
        

    

# Interpolate a 2D array into a grid.
# - x: coord. along the x axis of the array 
# - y: coord. along the y axis of the array
# - array: 2d array
# - factor: increase or decrease the number of rows and columns.
def interpol2Darray(x,y,array, factor):
    x_g,y_g = np.meshgrid(x,y)
    f = interpolate.interp2d(x_g, y_g, array, kind='cubic')    

    xmin,xmax = min(x),max(x)
    ymin,ymax = min(y),max(y)
    X = np.linspace(xmin,xmax,len(x)*factor)
    Y = np.linspace(ymin,ymax,len(y)*factor)
    #x_gnew,y_gnew = np.meshgrid(X,Y)
    return f(X,Y)


# Function that return the pixel types, the number, the area occupy and the
# percentage of the area. It works when the pixel are integer 
# (e.g. land clases pixels).
# - rasterfile: integer-value raster file.
def inventoryOfPixelsInOneBandRaster(rasterfile):
    # Reading the raster
    # register all of the drivers
    gdal.AllRegister()
    # open the image
    ds = gdal.Open(rasterfile)
    if ds is None:
    	print 'Could not open image'
    	sys.exit(1)
    
    # Getting image dimensions	
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    geo_t = ds.GetGeoTransform()
    #xOrigin = geo_t[0]
    #yOrigin = geo_t[3]
    pixelWidth = geo_t[1]
    pixelHeight = geo_t[5]
    pixArea = abs(pixelWidth*pixelHeight)    
    
    # Read bands
    #bands = ds.RasterCount
    # Read the whole band (DEMs have only one band)
    band = ds.GetRasterBand(1)
    #blockSize = band.GetBlockSize()
    #xBSize = blockSize[0]
    #xBSize = blockSize[1]
    
    #print xBSize, xBSize
    
    # Reading the band by rows and recording pixels and number
    uniqueAll = []
    countsAll = []
    for i in range(rows):
        #print "Reading block: ", i
        print "Reading row: ", i
        #data = band.ReadAsArray(0, 0, blockSize[0], blockSize[1])
        data = band.ReadAsArray(0, i, cols, 1)
        #y = np.bincount(np.ravel(data))
        #ii = np.nonzero(y)[0]
        #a=zip(ii,y[ii])
        
        unique, counts = np.unique(data, return_counts=True)
        uniqueAll.extend(unique)
        countsAll.extend(counts)
    
        #a=np.asarray((unique, counts)).T
    # Cleaning up memory
    band = None
    
    # Removing negative pixels
    dummy1 = [i for i in uniqueAll if i > 0]   
    dummy2 = [j for i,j in zip(uniqueAll,countsAll) if i > 0]
    uniqueAll = dummy1
    countsAll = dummy2
    
    # Counting the pixel    
    unique, counts = np.unique(np.array(uniqueAll), return_counts=True)
    counts = []
    unique = list(unique)
    for i in unique:
        print "Counting for pixel:", i
        dummy = [k for j,k in zip(uniqueAll,countsAll) if j == i]
        counts.append(sum(dummy))
        
    area = list(pixArea*np.array(counts))
    perc = list(np.array(counts)*100.0/sum(countsAll))
    
    return(unique, counts, area, perc)
	

def shpfilePolyAreas(file):
	"""
	Estimate the area of the features of a polygon shapefile.
	Input:
	- file: name and path of the shapefile. The file must be projected onto
	cartesian coordinates.
	Output: 
	- areaL: list of poly areas in km^2
	"""
	
	# Opening shapefile
	shfile, layer = openingShpFile(file)
	
	# Check the geometry type
	feature = layer.GetNextFeature()
	geom = feature.GetGeometryRef()
	if geom.GetGeometryName() != 'POLYGON':
		print 'Wrong geometry type, exiting...'
		shfile.Destroy()
		return

	# Iterating through layer features
	layer.ResetReading()
	feature = layer.GetNextFeature()
	i = 0
	areaL=[]
	while feature:
		geom = feature.GetGeometryRef()
		area = geom.GetArea()/1.e6 
		print 'Area of polygon ', i,':', area,' km^2'
		areaL.append(area) 
		
		i+=1
		feature.Destroy
		feature = layer.GetNextFeature()

	shfile.Destroy()
	
	return areaL	

def extractRasterValuesFromLAT_LON(rasterIn, lats, lons):
    """
    Extract raster values at the lat, lon coordinates and return them into data.
    """
    
    # register all of the drivers
    gdal.AllRegister()
    # open the image
    ds = gdal.Open( rasterIn)
    if ds is None:
        print 'Could not open image'
        sys.exit(1)
 
    # Getting image dimensions  
    # cols = ds.RasterXSize
    # rows = ds.RasterYSize
    # bands = ds.RasterCount
    #print cols, ' ',rows, ' ' ,bands
     
    # Getting georeference info
    geotransform = ds.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    #print originX, ' ', originY, ' ', pixelWidth, ' ', pixelHeight
    
    data = []
    for lat,lon in zip(lats,lons):
        # Reading the pixel 1,1 of the band no. 1
        x = lon
        y = lat
        xOffset = int((x - originX) / pixelWidth)
        yOffset = int((y - originY) / pixelHeight)
        band = ds.GetRasterBand(1) 
        data.append(band.ReadAsArray(xOffset, yOffset, 1, 1)[0][0]) # Here offset are 0
        
    return data
