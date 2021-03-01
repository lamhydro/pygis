	
# 
def flowPathLength(demCatch,idsMatrix, pixelWidth):
	nrow,ncol=demCatch.shape
	
	rowsVal=[]
	colsVal=[]
	rowNeighDrainAll=[]
	colNeighDrainAll=[]
	zNeighDrainAll=[]
	zNeighDrain=[]
	disNeighDrain=[]
	idsNeighDrain=[]
	ids=[]
	idsNeighAll=[]
	dirCode=[]
	typeOfCell=[]
	zPix=[]
	for row in range(nrow):
		for col in range(ncol):

			if demCatch[row,col] != 0.0:

				zNeigh=[]
				rowNeigh=[]
				colNeigh=[]
				idsNeigh=[]
				for i in [row-1, row, row+1]:
					for j in [col-1, col, col+1]:
						if (i!=row or j!=col):
							if (i in range(nrow)) and (j in range(ncol)):
								if demCatch[i,j] != 0.0:
									zNeigh.append(demCatch[i,j])
									rowNeigh.append(i)
									colNeigh.append(j)
									idsNeigh.append(idsMatrix[i,j])
				
				zPix.append(demCatch[row,col])
				idsNeighAll.append(idsNeigh)
				rowsVal.append(row)
				colsVal.append(col)
				ids.append(idsMatrix[row,col])
				rowNeighDrainAll.append(rowNeigh)
				colNeighDrainAll.append(colNeigh)
				zNeighDrainAll.append(zNeigh)
				
				if len(zNeigh):
					# Classification of type of cell
					if zNeigh.count(min(zNeigh)) > 1: 		# Drain to > 1 pixel
						#Flat pix to flat pix
						if min(zNeigh) == demCatch[row,col]:
							typeOfC = 0
						#Flat to slope pixels or slope to flat pixels
						elif min(zNeigh) < demCatch[row,col]:
							typeOfC = 1
						else: 
							typeOfC = -1 # Sink						
					elif zNeigh.count(min(zNeigh)) == 1:  	# Drain to 1 pixel
						if min(zNeigh) == demCatch[row,col]:
							typeOfC = 0
						elif min(zNeigh) < demCatch[row,col]:
							typeOfC = 2	 # Well defined pixels
						else:
							typeOfC = -1 # Sinks
					else:									# Drain to nowhere (isol. pix)
						typeOfC = -1
				
				else: # For isolated pixels with no neighbours
					typeOfC = -1
					print 'here'

				typeOfCell.append(typeOfC)		
				
				# Defining the direction of typeOfCell = 2 (#A pixel has one and only one pixel to drain)
				if typeOfC == 2:
					idMinZ = zNeigh.index(min(zNeigh))
					zNeighDrain.append(min(zNeigh))
					idsNeighDrain.append(idsMatrix[rowNeigh[idMinZ],colNeigh[idMinZ]])
					dz = demCatch[row,col]-min(zNeigh)
					if row==rowNeigh[idMinZ] or col==colNeigh[idMinZ]:
						disNeighDrain.append(math.sqrt(pixelWidth**2+dz**2))
					else:
						disNeighDrain.append(math.sqrt((pixelWidth*math.sqrt(2))**2+dz**2))
					dirCode.append(asignDirCode(row,col,rowNeigh[idMinZ],colNeigh[idMinZ]))
				else:
					zNeighDrain.append(-1)
					idsNeighDrain.append(-1)
					disNeighDrain.append(-1)
					dirCode.append(0)
					
				

					
	dirFreq=dict((i,dirCode.count(i)) for i in dirCode)
	#print dirFreq
	#print typeOfCell, dirCode, idsNeighDrain

	#sys.exit(0)

	
	# Defined direction typeOfCell = 1 (#Flat to slope pixels or slope to flat pixels)
	ii = 0
	dirCodeTyAll=[]
	dirCodeTyFreqAll=[]
	for row ,col in zip(rowsVal, colsVal):
		dirCodeTy=[]
		dirCodeTyFreq=[]
		if typeOfCell[ii] == 1: # or typeOfCell[ii] == 0:
			zNeigh   = zNeighDrainAll[ii]
			rowNeigh = rowNeighDrainAll[ii]
			colNeigh = colNeighDrainAll[ii]

			for i1 in list_duplicates_of(zNeigh,min(zNeigh)):
				dummy = asignDirCode(row,col,rowNeigh[i1],colNeigh[i1])
				dirCodeTy.append(dummy)
				if dummy in dirFreq.keys(): dirCodeTyFreq.append(dirFreq[dummy])
				else: dirCodeTyFreq.append(0)
				#print dummy
			
			prevDir = dirCodeTyFreq.index(max(dirCodeTyFreq)) 
			#print prevDir
			dirCode[ii] = dirCodeTy[prevDir]
			rowDrain,colDrain = asignRowColByDirCode(row,col,dirCodeTy[prevDir])
			idsNeighDrain[ii]=(idsMatrix[rowDrain,colDrain])
			zNeighDrain[ii]=demCatch[rowDrain,colDrain]
			dz=demCatch[row,col]-demCatch[rowDrain,colDrain]
			if row==rowDrain or col==colDrain:
				disNeighDrain[ii]=math.sqrt(pixelWidth**2 + dz**2)
			else:
				disNeighDrain[ii]=math.sqrt((pixelWidth*math.sqrt(2))**2 + dz**2)
						
		dirCodeTyAll.append(dirCodeTy)
		dirCodeTyFreqAll.append(dirCodeTyFreq)
		ii += 1 
	

	# Defined direction typeOfCell = 0 (Flat to flat pixel(s))
	i = 0
	flatAreasAll=[]
	count = 1
	nFlatPix=0
	for typeOfC in typeOfCell:
		if typeOfC == 0:

			inthere=0
			for lst in flatAreasAll:
				if ids[i] in lst:
					inthere=1
					break
		
			if inthere == 0:
				copyIds=ids[:] # Create a physically-based copy of ids
				# Getting the flat patches of dem
				dummy= conectFlatPix(zPix[i],i,[], idsNeighAll, zNeighDrainAll,copyIds)
				flatAreas=sorted(list(set(dummy)))
				
				# Check whether the flat sector is a sink sector.
				dummy=[]
				for j in flatAreas:
					idx = ids.index(j)
					dummy.append(zNeighDrainAll[idx])
				dummy = sum(dummy,[])
				if all(x >= zPix[idx]  for x in dummy):
					for j in flatAreas:
						idx = ids.index(j)
						typeOfCell[idx]=-1
						#print typeOfCell[idx]	
					
				
				listIdx=[]
				for j  in flatAreas:
					idx = ids.index(j)
						
					#print '--z: ', j, zPix[idx], typeOfCell[idx],dirCode[idx]
					if typeOfCell[idx]==0:
						listIdx.append(idx)
				
				while len(listIdx)>0:
					for idx in listIdx:
						idsNeigh  = idsNeighAll[idx]
						zNeigh   = zNeighDrainAll[idx]
						i1=0
						ty2=[]
						ty1=[]
						ty0De=[]
						for idN in idsNeigh:
							if zNeigh[i1] == zPix[idx]:
								if typeOfCell[ids.index(idN)] == 2:
									ty2.append(ids.index(idN))
								if typeOfCell[ids.index(idN)] == 1:
									ty1.append(ids.index(idN))
								if typeOfCell[ids.index(idN)] == 0 and dirCode[ids.index(idN)] != 0:
									ty0De.append(ids.index(idN))
							i1+=1
						if len(ty2)>0:
							rowDrain=rowsVal[ty2[0]]
							colDrain=colsVal[ty2[0]]
							dirCode[idx] = asignDirCode(rowsVal[idx],colsVal[idx],rowDrain,colDrain)
							#print '>>>>>',dirCode[idx]
							idsNeighDrain[idx]=(idsMatrix[rowDrain,colDrain])
							if row==rowDrain or col==colDrain:
								disNeighDrain[idx]=pixelWidth
							else:
								disNeighDrain[idx]=pixelWidth*math.sqrt(2)
							zNeighDrain[idx]=demCatch[rowDrain,colDrain]
							del listIdx[listIdx.index(idx)]
							break
						elif len(ty1)>0: 
							rowDrain=rowsVal[ty1[0]]
							colDrain=colsVal[ty1[0]]
							dirCode[idx] = asignDirCode(rowsVal[idx],colsVal[idx],rowDrain,colDrain)
							#print '>>>>>',dirCode[idx]
							idsNeighDrain[idx]=(idsMatrix[rowDrain,colDrain])
							if row==rowDrain or col==colDrain:
								disNeighDrain[idx]=pixelWidth
							else:
								disNeighDrain[idx]=pixelWidth*math.sqrt(2)
							zNeighDrain[idx]=demCatch[rowDrain,colDrain]
							del listIdx[listIdx.index(idx)]
							break
						elif len(ty0De)>0: 	
							rowDrain=rowsVal[ty0De[0]]
							colDrain=colsVal[ty0De[0]]
							dirCode[idx] = asignDirCode(rowsVal[idx],colsVal[idx],rowDrain,colDrain)
							#print '>>>>>',dirCode[idx]
							idsNeighDrain[idx]=(idsMatrix[rowDrain,colDrain])
							if row==rowDrain or col==colDrain:
								disNeighDrain[idx]=pixelWidth
							else:
								disNeighDrain[idx]=pixelWidth*math.sqrt(2)
							zNeighDrain[idx]=demCatch[rowDrain,colDrain]
							del listIdx[listIdx.index(idx)]
							break
				
				nFlatPix += len(flatAreas)
				flatAreasAll.append(flatAreas)
				count +=1
		i += 1
	print count, len(flatAreasAll), nFlatPix 
	print flatAreasAll
	return flatAreasAll
	sys.exit(0)
	
	# Checking loops
	i = 0
	idNeighLasts=[]
	for id in ids:
		if idsNeighDrain[i] != -1:
			#if newid not in ids: print 'here'
			idNeigh=[]
			idNeigh.append(id)
			
			newid=idsNeighDrain[i]
			ifLoop, idNeigh=loopIndeInNetwork(idNeigh,newid,ids,idsNeighDrain)
			if ifLoop: 
				print 'loop'
				sys.exit(0)
		i+=1
	
	#sys.exit(0)
	
	# Flow path length calculation
	i=0
	flowPathLen = []
	for id in ids:
		if idsNeighDrain[i] != -1:
			newid=idsNeighDrain[i]
			accuDis=disNeighDrain[i]
			#newids=ids
			#del newids[i]
			dummy = accumuThrouhtNetwork(newid,ids,idsNeighDrain,disNeighDrain,accuDis)
			flowPathLen.append(dummy)
			#print 'Flow path length: ', id ,dummy
			#sys.exit(0)
		i+=1
	#print 	flowPathLen, disNeighDrain
	#return sum(flowPathLen) / float(len(flowPathLen))
	
	
def conectFlatPix(z, idx, flatPix, idsNeighAll, zNeighDrainAll, idsCopy):
	#if typeOfCell[idx] == 0:
		#print typeOfCell[idx], neighAll[idx]
	#if count > len(idsCopy): return flatPix
	#if len(flatPix)>= 2*len(idsCopy): return flatPix
	#if idsCopy[idx] not in flatPix:
	#print idsNeighAll[idx], zNeighDrainAll[idx]
	flatPix.append(idsCopy[idx])
	idsCopy[idx]=-100
	zNeigh=zNeighDrainAll[idx]
	idsNeigh=idsNeighAll[idx]
	#if zNeigh.count(z) > 0:
	i = 0
	dummy=[]
	for zN in zNeigh:
		if zN == z:
			#if idsNeigh[i] not in flatPix:
			if idsNeigh[i] in idsCopy:
				dummy.append(idsNeigh[i])	
				flatPix.append(idsNeigh[i])
		i+=1
	for ii in dummy:
		if ii in idsCopy:
			idx = idsCopy.index(ii)
			conectFlatPix(z,idx,flatPix, idsNeighAll, zNeighDrainAll,idsCopy)
	return flatPix
	#if re == 0: return 	flatPix
	#return flatPix							
	#else:
	#	return flatPix
	#else:
	#return flatPix
	
	
def accumuThrouhtNetwork(id,ids,idsNeighDrain,disNeighDrain,accuDis):
	#print accuDis 
	#if id in ids:
	if id == -1: 
		return accuDis+1
	else:
		row=ids.index(id)
	#else:
	#	return accuDis
	#print row
	newid=idsNeighDrain[row]
	#if newid == -1: return accuDis
	accuDis+=disNeighDrain[row]
	#newids=ids
	#del newids[row]
	accuDis+=accumuThrouhtNetwork(newid,ids,idsNeighDrain,disNeighDrain,0)
	return accuDis
	
# Identification of loops
def loopIndeInNetwork(idNeigh,id,ids,idsNeighDrain):
	#print idNeigh
	idNeigh.append(id)
	row=ids.index(id)
	newid=idsNeighDrain[row]
	
	if newid in idNeigh: 
		#print newid,idNeigh, 'loop'
		return 1, idNeigh
	if newid == -1: 
		return 0, idNeigh
		
	return loopIndeInNetwork(idNeigh,newid,ids,idsNeighDrain)
		

def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def asignDirCode(row,col,rowDrain,colDrain):
	if   row==rowDrain and col+1==colDrain:   return 1
	elif row+1==rowDrain and col+1==colDrain: return 2
	elif row+1==rowDrain and col==colDrain:   return 3
	elif row+1==rowDrain and col-1==colDrain: return 4
	elif row==rowDrain and col-1==colDrain:   return 5
	elif row-1==rowDrain and col-1==colDrain: return 6
	elif row-1==rowDrain and col==colDrain:   return 7
	else:                                     return 8
	
def asignRowColByDirCode(row,col,dirCode):
	if   dirCode == 1: return row,col+1 
	elif dirCode == 2: return row+1,col+1
	elif dirCode == 3: return row+1,col 
	elif dirCode == 4: return row+1,col-1 
	elif dirCode == 5: return row,col-1 
	elif dirCode == 6: return row-1,col-1 
	elif dirCode == 7: return row-1,col 
	else:              return row-1,col+1 	


import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal
from gdalconst import *
import numpy as np
import math

# set directory
os.chdir("W:\\Luis") 

# Register all of the drivers
gdal.AllRegister()

# Reading the DEM raster
# open the image
#ds = gdal.Open('E:\\GeoBase\\CDED\\082n16\\082n16_0201_deme1.tif')
ds = gdal.Open('W:\\Luis\\filled_dem_melkamu1.tif')
if ds is None:
	print 'Could not open image'
	sys.exit(1)
print '\n \n'

# Getting raster dimensions	
cols = ds.RasterXSize
rows = ds.RasterYSize
bands = ds.RasterCount
print cols, rows, bands

geo_t = ds.GetGeoTransform()

# Get the band
band = ds.GetRasterBand(1)

# get data
data = band.ReadAsArray(0, 0, cols, rows)

idsMatrix=np.array(range(rows*cols))
idsMatrix=idsMatrix.reshape([rows,cols])
flatAreasAll=flowPathLength(data,idsMatrix,geo_t[1])
#print 'Ave. flow path length: ', aveFlowPathLen



# Writing a new raster file
driver = ds.GetDriver()
newRasterfn='filled_dem_melkamu1_FlatAreas.tif'
outRaster = driver.Create(newRasterfn, cols, rows, 1, GDT_Float32)
outBand = outRaster.GetRasterBand(1)
outBand.SetNoDataValue(0.0)

k = 0
nFlatAreas = len(flatAreasAll)
for i in range(rows):
	for j in range(cols):
		outBand.WriteArray(np.zeros((1,1)), j, i)
		for jj in flatAreasAll:
			for ii in jj:
				if k == ii:
					a=np.zeros((1,1))
					a[0,0] = data[i,j]
					outBand.WriteArray(a, j, i)

		k += 1

# flush data to disk, set the NoData value and calculate stats
outBand.FlushCache()
outBand.GetStatistics(0, 1)
#outRaster.SetNoDataValue(ds.GetNoDataValue())
#stats = outRaster.GetStatistics(0, 1)

# georeference the image and set the projection
geoTransform = ds.GetGeoTransform()
outRaster.SetGeoTransform(geoTransform)
proj = ds.GetProjection()
outRaster.SetProjection(ds.GetProjection())	
			
			
# Cleaning up memory
ds = None
outRaster = None


sys.exit(0)
































# set directory
#os.chdir(r'C:\Users\Luis\Downloads\072e')
os.chdir("E:\\Red_deer_SPARROW\\RiverNet2")

# Opening 'CatchmentDef.shp'
#file = 'New_Shapefile.shp'
file = 'CatchmentDef.shp'
shfileCatch, layer = openingShpFile(file)

# Getting the spatial projection
geoSR = layer.GetSpatialRef()
geoSRop = layer.GetSpatialRef()
wkt = geoSR.ExportToWkt()
print 'Spatial projection:', geoSR

# Reading the raster
# register all of the drivers
gdal.AllRegister()
# open the image
ds = gdal.Open('filall')
if ds is None:
	print 'Could not open image'
	sys.exit(1)
print '\n \n'
demWKT = ds.GetProjectionRef()
print 'Spatial projection:', demWKT

geoSRop.ImportFromWkt(demWKT)
# wkt from above, is the wicket from the shapefile
geoSR.ImportFromWkt(wkt)
# now make sure we have the shapefile geom

# Getting image dimensions	
cols = ds.RasterXSize
rows = ds.RasterYSize
bands = ds.RasterCount
# Read the whole band (DEMs have only one band)
band = ds.GetRasterBand(1) 
data = band.ReadAsArray(0, 0, cols, rows).astype(np.float)
#mask = np.greater(data,0)
data = np.where(data>np.min(data),data,0)

#sys.exit(0)

geo_t = ds.GetGeoTransform()

feature = layer.GetNextFeature()
j = 0
ofile  = open('aveFlowPathLength.csv', "wb")
writer = csv.writer(ofile)
header = ['SPARROWID','aveFlowPathLength_M']
writer.writerow(header)
#recursionlimit = sys.getrecursionlimit()
sys.setrecursionlimit(100000000)
while feature:

	#if j==7992: #9:2679 192 1372
	# Geting the geometry of the polygons
	geom = feature.GetGeometryRef()
	points = []
	#print j, ' ', geom.GetGeometryType(),'  ', geom.GetGeometryCount()
	if geom.GetGeometryType() == 6: # For multipolygons
		for idpol in range(geom.GetGeometryCount()):
			pts = geom.GetGeometryRef(idpol).Boundary()
			pts.AssignSpatialReference(geoSR)
			pts.TransformTo(geoSRop)
			for p in range(pts.GetPointCount()):
				points.append((pts.GetX(p), pts.GetY(p)))
	else:							# For polygons
		pts = geom.GetGeometryRef(0) #0 for the outer polygon
		pts.AssignSpatialReference(geoSR)
		pts.TransformTo(geoSRop)
		for p in range(pts.GetPointCount()):
			points.append((pts.GetX(p), pts.GetY(p)))

	pnts = np.array(points).transpose()

	#transforming between pixel/line (P,L) raster space, and projection coordinates (Xp,Yp) space.
	pixel, line = world2Pixel(geo_t,pnts[0],pnts[1])

	# Create a new image with the raster dimension
	rasterPoly = Image.new("L", (cols, rows),1)
	rasterize = ImageDraw.Draw(rasterPoly)
	listdata = [(pixel[i],line[i]) for i in xrange(len(pixel))]
	rasterize.polygon(listdata,0)
	mask = 1 - imageToArray(rasterPoly)
	
	#plt.imshow(mask)
	#plt.show()
	
	dataInPoly=data*mask
	print np.sum(mask),dataInPoly[dataInPoly>0].max(), dataInPoly[dataInPoly>0].min() 

	
	nrow,ncol=dataInPoly.shape
	idsMatrix=np.array(range(nrow*ncol))
	idsMatrix=idsMatrix.reshape([nrow,ncol])
	#print np.min(idsMatrix), np.max(idsMatrix)
	
	minZ=dataInPoly[dataInPoly>0].min()
	minZindex = np.where(dataInPoly==minZ)
	if len(minZindex[0])>1:
		idPixToCut=int(len(minZindex[0])/2)
		print idPixToCut
		dataInPoly[minZindex[0][idPixToCut],minZindex[1][idPixToCut]]=minZ-0.1

	# Calculation of average flow path length.
	#if np.sum(mask)> recursionlimit: # 
	#sys.setrecursionlimit(np.sum(mask))
	aveFlowPathLen=flowPathLength(dataInPoly,idsMatrix,geo_t[1])
	print 'Ave. flow path length: ',j, aveFlowPathLen
	#sys.setrecursionlimit(recursionlimit)
	
	# Cleaning the memory
	dataInPoly = None
	
	
	writer.writerow([int(j),\
					float(aveFlowPathLen)])

	
	#fig = plt.figure()
	#ax = fig.add_subplot(111)
	#cax = ax.imshow(dataInPoly, interpolation='nearest')	

	feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them

	feature = layer.GetNextFeature()
	
	#if j == 0: # 9:
	#	break
		
	j += 1

ofile.close()

# Cleaning up memory
band = None
data = None	
