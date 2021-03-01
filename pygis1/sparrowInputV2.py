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
	i=0
	while featurePoint:

		geomPoint = featurePoint.GetGeometryRef()
		if geomPoint.Within(geomPoly): # It does not work for a point touching the polygon edge.
		#if geomPoly.Intersect(geomPoint):
			#return featurePoint.GetField('HydroID')
			return i

		featurePoint.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
		featurePoint = layerPoint.GetNextFeature()
		i += 1
		
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

# Opening ' AdjointCatchment.shp'
shfileAdjC, AdjCLay = openingShpFile('AdjointCatchment.shp')
# - Get the fields' names
field_namesAdjC = getLayerFields(AdjCLay)
# - Get features' attributes
HydroAdjCatch = np.array(readLayerField(AdjCLay,field_namesAdjC))

# Getting the accumulated area
HydroID =  CatchmentDef[:,3]
DrainID = HydroAdjCatch[:,3]
accuArea = []
for id in HydroID:
	row = np.where(DrainID==id)[0]	
	accuArea.append(list(HydroAdjCatch[row,1]))
	
# Getting the lake area drained by each catchment
# - Reading the '[Edge lakearea]' file
f = open('streamLakeArea.txt', 'r')
catchLakeArea = [0]*len(CatchmentDef[:,3])
i = 0
for line in f:
	if i > 0:
		columns = line.split()
		feature = EdgeLay.GetFeature( int(columns[0]) )
		field = feature.GetField('DrainID')
		row = np.where(HydroID==field)[0]
		catchLakeArea[row] = float(columns[1])
	
	i += 1
	
# Reading accumulated annual average discharge
accumAnnualRunoff=[]
with open('accumAnnualRunoff.csv', 'rb') as f:
	reader = csv.reader(f)
	i = 0
	for row in reader:
		if i>0:
			accumAnnualRunoff.append(float(row[1]))
		i+=1

# Estimating hydraulic load in (year/m)
hydraulicLoad = []
for Qc,Al in zip(accumAnnualRunoff,catchLakeArea):
	hydraulicLoad.append(Al/(Qc*60*60*24*365))
			

# Reading fromNodeToNode file
fnode      = []
tnode      = []
stream_len = []
with open('fromNodeToNode.csv', 'rb') as f:
	reader = csv.reader(f)
	i = 0
	for row in reader:
		if i>0:
			fnode.append(float(row[1]))
			tnode.append(float(row[2]))
			stream_len.append(float(row[3]))
		i+=1
			
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



# Getting the Min and Max Z for each catchment and the slope.
f = open('catchMinMax.txt', 'r')
minMax = [ map(float,line.split('\t')) for line in f ]
f.close()
HydroID =  CatchmentDef[:,3]
NextDownID = CatchmentDef[:,5]
catchSlope = []
i = 0
for id in HydroID:
	rows = np.where(NextDownID==id)[0]
	if len(rows)==0:
		slope = (minMax[i][1]-minMax[i][0])/float(stream_len[i])
	else:
		minUp = []
		for row in rows:
			minUp.append(minMax[row][0])
		slope = (max(minUp)-minMax[i][0])/float(stream_len[i])
	if slope < 0.001:
		catchSlope.append(0.001)
	else:
		catchSlope.append(slope)	
	i += 1
	
minMax = None	

# Estimation  discharge fraction in a bifurcation
bifFac = []
for fno in fnode:
	 bifFac.append(1.0/fnode.count(fno))


# Matching the water quality station positions  and the catchment
# - Opening 'wqdata_sites.shp'
shfileWQ, WQLay= openingShpFile('wqdata_sites.shp')
# - Get the fields' names
field_namesWQ = getLayerFields(WQLay)
# - Get features' attributes
WQDef = np.array(readLayerField(WQLay,field_namesWQ))
wq_lat = [0]*len(CatchmentDef[:,3])
wq_lon = [0]*len(CatchmentDef[:,3])
wq_staN = [0]*len(CatchmentDef[:,3])
CatchLay.ResetReading() #need if looping again
for i in range(len(CatchmentDef[:,3])):
	WQLay.ResetReading() #need if looping again
	id = pointWithinPoly(CatchLay, WQLay,i)
	print id
	if id != None:
		wq_staN[i] = WQDef[id,0]
		wq_lat[i]  = WQDef[id,3]
		wq_lon[i]  = WQDef[id,4]

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
				

				
# Saving info for each catchment
ofile  = open('reddeerdata.csv', "wb")
writer = csv.writer(ofile)
CatchLay.ResetReading() #need if looping again
feature = CatchLay.GetNextFeature()
i = 0
header = ['SPARROW ID','HydroID','fnode','tnode','StreamLength','StreamOrder','NextDownID','Shape_Area','AccumArea','TotalLakeAreaKm2', 'catchSlope', 'frac','lat','lon','staid']
writer.writerow(header)

while feature:
	
	if accuArea[i] == []:
		accuAreaIn = 0.0
	else:
		accuAreaIn = accuArea[i][0]
	
	writer.writerow(['SPARROW_ID_'+str(i),\
					int(CatchmentDef[i,3]),\
					int(fnode[i]),\
					int(CatchmentDef[i,7]),\
					float(stream_len[i]),\
					int(CatchmentDef[i,6]),\
					int(CatchmentDef[i,5]),\
					CatchmentDef[i,2],\
					accuAreaIn,\
					catchLakeArea[i],\
					catchSlope[i],\
					bifFac[i],\
					wq_lat[i],\
					wq_lon[i],\
					wq_staN[i]])

		
	feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
	feature = CatchLay.GetNextFeature()

	i += 1

	#if i == 30:
	#	break
	
ofile.close()

# Also need to close DataSource objects 
# when done with them
shfileCatch.Destroy()
shfileEdge.Destroy()
shfileJunc.Destroy()
shfileAdjC.Destroy()

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
