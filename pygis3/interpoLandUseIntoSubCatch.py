def world2Pixel(geoMatrix, x, y):
  """
  Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
  the pixel location of a geospatial coordinate
  """
  ulX = geoMatrix[0]
  ulY = geoMatrix[3]
  xDist = geoMatrix[1]
  yDist = geoMatrix[5]
  rtnX = geoMatrix[2]
  rtnY = geoMatrix[4]
  pixel = np.round((x - ulX) / xDist).astype(np.int)
  line = np.round((ulY - y) / xDist).astype(np.int)
  return (pixel, line)

# after http://geospatialpython.com/2011/02/clip-raster-using-shapefile.html
# This function will convert the rasterized clipper shapefile
# to a mask for use within GDAL.
def imageToArray(i):
    """
    Converts a Python Imaging Library array to a
    numpy array.
    """
    a=np.fromstring(i.tobytes(),'b')
    a.shape=i.im.size[1], i.im.size[0]
    return a
	
#Opening ESRI shapefile. Return the shapefile driver of file and its layer.		
def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
		print 'Could not open file'
		sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)


def interpolateLandUseIntoSubCatch(rasterfile, outdir):
    # set directory
    os.chdir(outdir)
    
    # Opening 'CatchmentDef.shp'
    file = 'E:\\SouthSaskRiv_SPARROW\\RivNet3\\CatchmentDemFillV1_proj.shp'
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
    ds = gdal.Open(rasterfile)
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
    blockSize = band.GetBlockSize()
    xBSize = blockSize[0]
    xBSize = blockSize[1]
    print xBSize, xBSize
    
    #data = band.ReadAsArray(0, 0, cols, rows).astype(np.float)
    #data = np.where(data>np.min(data),data,0)
    
    geo_t = ds.GetGeoTransform()
    xOrigin = geo_t[0]
    yOrigin = geo_t[3]
    pixelWidth = geo_t[1]
    pixelHeight = geo_t[5]
    print xOrigin, yOrigin, geo_t[1], geo_t[5]
    cellArea = abs(pixelWidth*pixelHeight)
    #sys.exit(0)
    
    feature = layer.GetNextFeature()
    jj = 0
    maxPi=[]
    geoMatrix=range(0,6)
    GridIDs = []
    AAFCcode_11=[]
    AAFCcode_21=[]
    AAFCcode_25=[]
    AAFCcode_31=[]
    AAFCcode_41=[]
    AAFCcode_42=[]
    AAFCcode_45=[]
    AAFCcode_46=[]
    AAFCcode_51=[]
    AAFCcode_61=[]
    AAFCcode_62=[]
    AAFCcode_71=[]
    AAFCcode_73=[]
    AAFCcode_74=[]
    AAFCcode_91=[]
    sumError = 0
    while feature:
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
    	
    	# Reading the rectangle of the raster occupy by the polygon
    	j = int(min(pixel))
    	i = int(min(line))
    	ncols = int(max(pixel) - j)+1
    	nrows = int(max(line) - i)+1
    	data = band.ReadAsArray(j, i, ncols, nrows)
    
    	# Create a new image with the raster dimension
    	rasterPoly = Image.new("L", (ncols, nrows),1)
    	rasterize = ImageDraw.Draw(rasterPoly)
    	listdata = [(pixel[ii]-j,line[ii]-i) for ii in xrange(len(pixel))]
    	#listdata = [(pixel[i],line[i]) for i in xrange(len(pixel))]
    	rasterize.polygon(listdata,0)
    	mask = 1 - imageToArray(rasterPoly)
    	ncell = np.sum(mask)
    
    	dataInPoly=data*mask
    	dime = dataInPoly.shape
    	dataInPolyFreq = Counter( np.reshape(dataInPoly, dime[0]*dime[1]) )
    	for k in dataInPolyFreq.keys():
    		dataInPolyFreq[k] = 100.*dataInPolyFreq[k]/ncell
     
    	#dataInPoly[np.where(dataInPoly == 0)] = -99999
    
    	#maxZ = np.max(dataInPoly[np.nonzero(dataInPoly)])
    	#minZ = np.min(dataInPoly[np.nonzero(dataInPoly)])
    	
    	#avAtmosDepo = np.sum(dataInPoly)/(ncell)
    	#rainAveCell = ncell*cellArea*rainAveM
    	#rainAveArea = feature.GetField('Shape_Area') * rainAveM
    	
    	print jj
    	
    	GridIDs.append(feature.GetField('GridID'))
    	AAFCcode_11.append(dataInPolyFreq[11])
    	AAFCcode_21.append(dataInPolyFreq[21])
    	AAFCcode_25.append(dataInPolyFreq[25])
    	AAFCcode_31.append(dataInPolyFreq[31])
    	AAFCcode_41.append(dataInPolyFreq[41])
    	AAFCcode_42.append(dataInPolyFreq[42])
    	AAFCcode_45.append(dataInPolyFreq[45])
    	AAFCcode_46.append(dataInPolyFreq[46])
    	AAFCcode_51.append(dataInPolyFreq[51])
    	AAFCcode_61.append(dataInPolyFreq[61])
    	AAFCcode_62.append(dataInPolyFreq[62])
    	AAFCcode_71.append(dataInPolyFreq[71])
    	AAFCcode_73.append(dataInPolyFreq[73])
    	AAFCcode_74.append(dataInPolyFreq[74])
    	AAFCcode_91.append(dataInPolyFreq[91])
    	
    	feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
    
    	feature = layer.GetNextFeature()
    	
    	#if jj == 1:
    	#	break
    		
    	jj += 1
    	
    
    #print 'Ave error of rainfall estimation: ', sumError/j, ' %'
    # Cleaning up memory
    band = None
    data = None	
    shfileCatch.Destroy()
    
    # Reading matching relationship of streams and subcatchments
    NIDriv = []
    GridIDcat = []
    with open('E:\\SouthSaskRiv_SPARROW\\RivNet3\\NIDrivAndGridIDcatDef.txt', 'r') as f:
        # do things with your file
    	header = f.readline()
    	for line in f:
    		columns = line.split()
    		NIDriv.append(columns[0])
    		GridIDcat.append(int(columns[1]))	
    
    		
    # Reordering sub. catch. values to streams. Writing into a file.
    file = rasterfile + '_inter.csv'
    with open(file,'w') as f1:
    	writer=csv.writer(f1, delimiter=',',lineterminator='\n')
    	# Note: see file 'AAFC_LULC_Classes.csv' in the current dir for codes.
    	writer.writerow(['FIDriv','AAFCcode_11','AAFCcode_21','AAFCcode_25','AAFCcode_31','AAFCcode_41','AAFCcode_42','AAFCcode_45','AAFCcode_46','AAFCcode_51','AAFCcode_61','AAFCcode_62','AAFCcode_71','AAFCcode_73','AAFCcode_74','AAFCcode_91'])
    	for i,GridID in enumerate(GridIDcat):
    		idx = GridIDs.index(GridID)
    		row = [i,AAFCcode_11[idx],AAFCcode_21[idx],AAFCcode_25[idx],AAFCcode_31[idx],AAFCcode_41[idx],AAFCcode_42[idx],AAFCcode_45[idx],AAFCcode_46[idx],AAFCcode_51[idx],AAFCcode_61[idx],AAFCcode_62[idx],AAFCcode_71[idx],AAFCcode_73[idx],AAFCcode_74[idx],AAFCcode_91[idx]]
    		writer.writerow(row)

#import GdalOgrPylib as go
import sys, os
#if r"C:\Anaconda\Lib\site-packages\PIL" not in sys.path:
#    sys.path.append(r"C:\Anaconda\Lib\site-packages\PIL")
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from gdalconst import *
import struct
import numpy as np
import matplotlib.pylab as plt
import Image,ImageDraw
import csv
from collections import Counter

years = ['1990','2000','2010']
       
for year in years:
    outdir = "G:\\data\\AAFC_LANDUSE\\" + year + 'landUse'
    print " "
    print 'Output directory: ', outdir
    print " "   
    for file in os.listdir(outdir):
        if file.endswith(year+".tif"): 
            print " "
            print '-> Interpolating for: ', file
            print " " 
            
            interpolateLandUseIntoSubCatch(file, outdir)      