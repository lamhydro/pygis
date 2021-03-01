
# Removing duplicate rows in mx2 column	
def remove_duplicates(x): 
	d = {} 
	for (a,b) in x: 
		d[(a,b)] = (a,b) 
	return np.array(list(d.values()))
	
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

def pointWithinPoly(layerPoly, layerPoint,polyID):
	featurePoint = layerPoint.GetNextFeature()
	featurePoly  = layerPoly.GetFeature(polyID)
	geomPoly=featurePoly.GetGeometryRef()
	while featurePoint:

		geomPoint = featurePoint.GetGeometryRef()
		#if geomPoint.Within(geomPoly): # It does not work for a point touching the polygon edge.
		if geomPoly.Intersect(geomPoint):
			return featurePoint.GetField('HydroID')

		featurePoint.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		featurePoint = layerPoint.GetNextFeature()
		
def getXYcoordFeature(layer, featureID):
	feature  = layer.GetFeature(featureID)
	geom = feature.GetGeometryRef()
	np = geom.GetPointCount()
	xycoord = [(geom.GetX(i), geom.GetY(i)) for i in range(np) ]
	
	return xycoord
	
def findApoint(layerPoint, XYpoint):
	feature = layerPoint.GetNextFeature()
	i = 0
	while feature:

		geom = feature.GetGeometryRef()
		xcoor = geom.GetX()
		ycoor = geom.GetY()
		ifx = xcoor == XYpoint[0]
		ify = ycoor == XYpoint[1]
		if ifx and ify:
			return i
	
		feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		feature = layerPoint.GetNextFeature()
		i += 1
	
import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import csv
import numpy as np
#import GdalOgrPylib	

#files = ['CatchmentDef.shp','HydroEdgeDef.shp','HydroJunctionDef.shp']
#names = ['CatchmentDef','HydroEdgeDef','HydroJunctionDef']

os.chdir("E:\\Red_deer_SPARROW\\RiverNet2")

# Opening 'CatchmentDef.shp'
shfileCatch, CatchLay= openingShpFile('CatchmentDef.shp')
# - Get the fields' names
field_namesCatch = getLayerFields(CatchLay)
# - Get features' attributes
CatchmentDef = np.array(readLayerField(CatchLay,field_namesCatch))

# Opening 'HydroEdgeDef.shp'
shfileEdge, EdgeLay = openingShpFile('HydroEdgeDef.shp')
# - Get the fields' names
field_namesEdge = getLayerFields(EdgeLay)
# - Get features' attributes
HydroEdgeDef = np.array(readLayerField(EdgeLay,field_namesEdge))

# Opening 'HydroJunctionDef.shp'
shfileJunc, JuncLay = openingShpFile('HydroJunctionDef.shp')
# - Get the fields' names
field_namesJunc = getLayerFields(JuncLay)
# - Get features' attributes
HydroJunctionDef = np.array(readLayerField(JuncLay,field_namesJunc))

# featurePoint = JuncLay.GetFeature(6815)
# geomPoint = featurePoint.GetGeometryRef()
# featurePoly = CatchLay.GetFeature(6889)#6877
# geomPoly = featurePoly.GetGeometryRef()
# #print int(geomPoly.Within(geomPoint)) #NO
# #print int(geomPoint.Touches(geomPoly)) #NO
# #print int(geomPoint.Within(geomPoly)) #NO
# #print int(geomPoint.Intersect(geomPoly)) #NO
# #print int(geomPoint.Disjoint(geomPoly)) #YES
# print int(geomPoly.Intersect(geomPoint)) #NO
# featureEdge = EdgeLay.GetFeature(6777)
# geomEdge = featureEdge.GetGeometryRef()
# xS = geomEdge.GetX(0)
# yS = geomEdge.GetY(0)
# xE = geomEdge.GetX(geomEdge.GetPointCount()-1)
# yE = geomEdge.GetY(geomEdge.GetPointCount()-1)
# print xS,'  ', yS
# print xS==geomPoint.GetX(),'  ', yS==geomPoint.GetY(0)


tnode = range(len(CatchmentDef[:,3]))
HydroID = CatchmentDef[:,3]
HydroID_Junc = HydroJunctionDef[:,1]
fnode = range(len(CatchmentDef[:,3]))
stream_len = range(len(CatchmentDef[:,3]))
for i in range(len(HydroEdgeDef)):
	DrainID = HydroEdgeDef[i,3]
	rowCatch = np.where(HydroID==float(DrainID))[0] # Position in the catchment matrix.
	#tnode.append(int(CatchmentDef[row,7]))
	tnode[rowCatch] = int(CatchmentDef[rowCatch,7])
	# there is something wrong here with tnode[i]
	# XY coord of a edge

	XYedge = getXYcoordFeature(EdgeLay, i)
	npo = len(XYedge)
	
	# Position of tnode in the HydroJunctionDef matrix
	row= np.where(HydroID_Junc==str(tnode[rowCatch]))[0]
	
	# XY coord of a point
	XYjunc = getXYcoordFeature(JuncLay, int(row))
	
	# for 1 point
	p1x=XYedge[0][0] == XYjunc[0][0]
	p1y=XYedge[0][1] == XYjunc[0][1]
	# for 2 point
	p2x=XYedge[npo-1][0] == XYjunc[0][0]
	p2y=XYedge[npo-1][1] == XYjunc[0][1]
	
	if p1x and p1y:
		XYfnode = [XYedge[npo-1][0], XYedge[npo-1][1]]
		print 'first'
	else:
		XYfnode = [XYedge[0][0], XYedge[0][1]]
		print 'last'

	JuncLay.ResetReading() #need if looping again 		
	row = findApoint(JuncLay, XYfnode)
	#fnode.append(HydroID_Junc[row])
	fnode[rowCatch] = int(HydroID_Junc[row])
	print i, fnode[rowCatch], tnode[rowCatch]
	
	# Getting length of streams
	stream_len[rowCatch] = HydroEdgeDef[i,1]
	
	#if i == 30:
	#	break
	
# sys.exit(0)

# # Getting length of streams
# stream_len = []
# DrainID = HydroEdgeDef[:,3]
# # Contain all the catchment that has at leas 1 upstream catchment 
# # (not headwater catchments)
# NextDownIDJunctionID = remove_duplicates(CatchmentDef[:,[5,7]])
# fnodeNew = np.zeros(len(CatchmentDef[:,3]))
# i = 0
# for HydroID in CatchmentDef[:,3]:
	
	# # Getting length of streams
	# row= np.where(DrainID==str(int(HydroID)))[0]
	# stream_len.append(HydroEdgeDef[rowEdge,1])
	
	# #WARNING. this section is comment since exist some from nodes(fnode) out of the catchment so the function pointWithinPoly can find fnode in such cases, so NaN values are saved in those cases. This part must be used with carefull.
	# # # Getting fnote (upstream note)
	# # row = np.where(NextDownIDJunctionID[:,0]==HydroID)[0]
	# # if len(row)==0:
	
		# # CatchLay.ResetReading() #need if looping again
		# # JuncLay.ResetReading() #need if looping again 
		# # # For those headwater catchment, the function pointWithinPoly
		# # # get the node (upstream note=fnote)  within the catchment.
		# # fnode[i] = pointWithinPoly(CatchLay, JuncLay, i)
		# # #fnode.append(-1)
	# # else:
		# # fnode[i]=NextDownIDJunctionID[row,1]
		
	
	# i += 1
	# print i
	# if i == 30:
		# break
				

ofile  = open('ttest.csv', "wb")
writer = csv.writer(ofile)
CatchLay.ResetReading() #need if looping again
feature = CatchLay.GetNextFeature()
i = 0
header = ['SPARROW ID','HydroID','fnode','tnode','StreamLength','StreamOrder','NextDownID','Shape_Area']
writer.writerow(header)

while feature:
	
	writer.writerow(['SPARROW_ID_'+str(i),\
					int(CatchmentDef[i,3]),\
					int(fnode[i]),\
					int(CatchmentDef[i,7]),\
					float(stream_len[i]),\
					int(CatchmentDef[i,6]),\
					int(CatchmentDef[i,5]),\
					CatchmentDef[i,2]])	
		
	feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
	feature = CatchLay.GetNextFeature()

	i = i + 1

	#if i == 30:
	#	break
	
ofile.close()

# Also need to close DataSource objects 
# when done with them
shfileCatch.Destroy()
shfileEdge.Destroy()
shfileJunc.Destroy()

sys.exit(0)

#sys.exit(0)
# Getting the upstream note
#pointWithinPoly(CatchmentDefLay , HydroJunctionDefLay)
print 'here'
featurePoint = JuncLay.GetFeature(0)
featurePoly  = CatchLay.GetFeature(0)
print 'here'
sys.exit(0)
# Also need to close DataSource objects 
# when done with them
shapefile.Destroy()


i = 0
cnt = 0
while featurePoint:

	geomPoly=featurePoly.GetGeometryRef()
	geomPoint = featurePoint.GetGeometryRef()
	if geomPoint.Within(geomPoly):
		cnt = cnt + 1
		print i

	featurePoint.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
	featurePoint = HydroJunctionDefLay.GetNextFeature()

	i = i + 1

print cnt


tnote = CatchmentDef[:,7]
hyseq = CatchmentDef[:,6]

sys.exit(0)




# i = 0
# for file in files:
        # shapefile =driver.Open(file, 0)
        # if shapefile is None:
                # print 'Could not open file'
                # sys.exit(1)

        # # Opening a layer	
        # layer = shapefile.GetLayer(0)

        # # Get the fields' names
        # field_names = getLayerFields(layer)
        # # Get features
        # exec(names[i] + ' = ' +'np.array(readLayerField(layer,field_names))')
        # print file
        # i += 1

# # Getting length of streams
# row = []
# DrainID = HydroEdgeDef[:,3]
# for HydroID in CatchmentDef[:,3]:
        # row.append(np.where(DrainID==str(int(HydroID)))[0])
# stream_len = HydroEdgeDef[row,1]

# Getting the upstream note
#pointWithinPoly(layerPoly, layerPoint)

# Getting length of fnode
#row = []
#JunctionID = CatchmentDef[:,7]
#for HydroID in CatchmentDef[:,3]:
#        print np.where(JunctionID==HydroID)[0]
#stream_len = HydroEdgeDef[row,1]



# Loop through all of the features
idfield_names = [1,3,6]
feature = layer.GetNextFeature()
ofile  = open('ttest.csv', "wb")
writer = csv.writer(ofile)
while feature:
		
	# get the x,y coordinates for the point
	#geom = feature.GetGeometryRef()
		
	row = ['SPARROW_ID']
	for idfield_name in idfield_names:
		row.append(feature.GetField(field_names[idfield_name]))
		
	#print row
	writer.writerow(row)
		
	feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
	feature = layer.GetNextFeature()

ofile.close()
