# read *.r2c files which contain precipitation data from CaPA re-analysis data.

def read_r2c_header(filename):
	# Open file
	f = open(filename, 'r')

	# Loop over lines and extract variables of interest
	for line in f:
		
		# Read header information
		line = line.strip()
		columns = line.split()
		name = columns[0]
		if name == ':Projection':
			Projection = columns[1]
		elif name == ':Ellipsoid':
			Ellipsoid = columns[1]
		elif name == ':xOrigin':
			xOrigin = float(columns[1])
		elif name == ':yOrigin':
			yOrigin = float(columns[1])
		elif name == ':AttributeName':
			AttributeName = columns[1]
		elif name == ':AttributeUnit':
			AttributeUnit = columns[1]
		elif name == ':xCount':
			xCount = int(columns[1])
		elif name == ':yCount':
			yCount = int(columns[1])
		elif name == ':xDelta':
			xDelta = float(columns[1])
		elif name == ':yDelta':
			yDelta = float(columns[1])
		elif name == ':endHeader':
			break
	f.close()
	return(Projection, Ellipsoid, xOrigin, yOrigin, AttributeName, AttributeUnit,  xCount, yCount, xDelta, yDelta)
			
			#break 
	#f.close()
	#return(AttributeUnit)
	

def read_r2c_data(filename):
	# Open file
	f = open(filename, 'r')

	# Loop over lines and extract variables of interest
	date = []
	time = []
	i = 0
	frame = 0
	preci = []
	for line in f:
		line = line.strip()
		columns = line.split()
		name = columns[0]
		# Save time
		if name == ':Frame':
			dummy = columns[3]
			date.append(dummy[1:])
			dummy = columns[4]
			time.append(dummy[:-1])
			#print date[i], time[i]
			i +=1
			frame = 1
			l = []
		elif frame and name != ':EndFrame':
			l.append(map(float, columns))
		elif name == ':EndFrame':
			frame = 0
			preci.append(np.array(l))
	
	return(date, time, preci)

	f.close()

# Opening ESRI shapefile. Return the shapefile driver of file and its layer.		
def openingShpFile(file):
		
	driver = ogr.GetDriverByName('ESRI Shapefile')

	shapefile = driver.Open(file, 0)
	if shapefile is None:
		print 'Could not open file'
		sys.exit(1)

	# Opening a layer	
	return shapefile, shapefile.GetLayer(0)
	
	
import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
import numpy as np
import matplotlib.pylab as plt
import time
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from gdalconst import *

os.chdir('E:\\CaPAdata')
	
path = 'E:\CaPAdata'
filenames = ['PR_0mb_2002-01-01-2002-12-31.r2c',
'PR_0mb_2003-01-01-2003-12-31.r2c',
'PR_0mb_2004-01-01-2004-12-31.r2c',
'PR_0mb_2005-01-01-2005-12-31.r2c',
'PR_0mb_2006-01-01-2006-12-31.r2c',
'PR_0mb_2007-01-01-2007-12-31.r2c',
'PR_0mb_2008-01-01-2008-12-31.r2c',
'PR_0mb_2009-01-01-2009-12-31.r2c',
'PR_0mb_2010-01-01-2010-12-31.r2c',
'PR_0mb_2011-01-01-2011-12-31.r2c',
'PR_0mb_2012-01-01-2012-06-30.r2c',
'PR_0mb_2012-01-01-2012-12-31.r2c',
'PR_0mb_2013-01-01-2013-11-04.r2c']


#fig = plt.figure()
#ax = fig.add_subplot(111)
preciAvT =[]
#i = 0
for filename in filenames:
	
	print 'Reading: ' + filename
 
	# Reading the header
	Projection, Ellipsoid, xOrigin, yOrigin, AttributeName, AttributeUnit, xCount, yCount, xDelta, yDelta = read_r2c_header(filename)
	print Projection, Ellipsoid, xOrigin, yOrigin, AttributeName, AttributeUnit, xCount, yCount, xDelta, yDelta
	
	# Reading the data
	datee, timee, preci = read_r2c_data(filename)

	# Average precipitation intensity
	#print len(datee),len(preci), len(preci[0]), len(preci[0][0])
	#preciAv = sum(preci)/len(preci) # Average
	#preciAv = preciAv*1000/6 # from m per 6h to mm per 1h
	preciAv = sum(preci)*1000 # Accumulated in mm
	preciAvT.append(preciAv)

	# Plotting 
	#plt.cla()
	#cax = ax.imshow(preciAv, interpolation='nearest')
	#cbar = fig.colorbar(cax)
	#ax.set_title('Mean Preci '+'('+ 'mm/h' +') '+ datee[0][:4])
	#plt.show()
	#plt.draw()
	#time.sleep(1)
	#plt.pause(0.1)

	# Clearing memory
	preci = None
	preciAV = None
	datee = None
	timee = None
	
	#if i == 1:
	#	break
	#i += 1 

nyears = len(filenames)
#preciAvTav = ( sum(preciAvT[0:nyears-2]) + (307/365)*preciAvT[nyears-1] )/nyears# Acummulated average mm/y
preciAvTav = sum(preciAvT[0:nyears-2])/(nyears-1)
preciAvT = None
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.imshow(preciAvTav, interpolation='nearest')
cbar = fig.colorbar(cax)
ax.set_title('Av. Accum. Preci '+'('+ 'mm/y' +') '+ '2002 - 2013')
plt.show()
#preciAvTav = None

# Getting projection from existing raster
#ds = gdal.Open(r'E:\Runoff\runoff_14')


# Creating a raster files
driver = gdal.GetDriverByName('GTiff')
outDataset = driver.Create('preciAv2002_2012.tif', xCount, yCount, 1, gdal.GDT_Float32)
proj = osr.SpatialReference()  
proj.SetWellKnownGeogCS( "NAD83" );  # Same result with  "WGS84" 
outDataset.SetProjection(proj.ExportToWkt()) 
geotransform = (xOrigin, 0.1, 0, yOrigin, 0, 0.1)  
outDataset.SetGeoTransform(geotransform)
outBand = outDataset.GetRasterBand(1)
outBand.WriteArray(preciAvTav, 0, 0)
outBand.FlushCache()
outBand.GetStatistics(0, 1)
#geotransform = ds.GetGeoTransform()
#outDataset.SetGeoTransform(geotransform)
#proj = ds.GetProjection()
#outDataset.SetProjection(proj)  
outDataset = None
preciAvTav = None 

# Reprojecting raster
# Opening the shape file
file = r'E:\Red_deer_SPARROW\RiverNet2\CatchmentDef.shp'
shfile, layer = openingShpFile(file)
geoSR = layer.GetSpatialRef()
wkt = geoSR.ExportToWkt()
# Get the extension
extent = layer.GetExtent()
inputfile = r'E:\CaPAdata\preciAv2002_2012.tif'
outputdir = r'E:\CaPAdata\preciAv2002_2012_PrXY.tif'
cmd = 'gdalwarp -overwrite' + ' -t_srs ' + '"'+wkt +'"'+ ' ' + inputfile + ' ' + outputdir
print cmd
print os.system(cmd) # if is 0 is normal execution

# Clipping for redDeer
rasterIn = r'E:\CaPAdata\preciAv2002_2012_PrXY.tif'
rasterOut = r'E:\CaPAdata\preciAv2002_2012_PrXY_RedDeer.tif'
cmd = 'gdal_translate' + ' -projwin ' + str(extent[0]-1000) + ' ' + str(extent[3]+1000) + ' ' + str(extent[1]+10000) + ' ' + str(extent[2]-10000) + ' -of GTiff ' + rasterIn + ' ' + rasterOut
print cmd
print os.system(cmd) # if is 0 is normal execution

