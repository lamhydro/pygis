import sys, os
if "C:\\Python27\\Lib\\site-packages" not in sys.path:
		sys.path.append("C:\\Python27\\Lib\\site-packages")
from osgeo import gdal
from gdalconst import *
import struct
import numpy
import matplotlib.pylab as plt
 

# set directory
os.chdir(r'C:\Users\Luis\Downloads\072e')
# register all of the drivers
gdal.AllRegister()
# open the image
ds = gdal.Open('072e_0100_deme.dem')
if ds is None:
	print 'Could not open image'
	sys.exit(1)

# Getting image dimensions	
cols = ds.RasterXSize
rows = ds.RasterYSize
bands = ds.RasterCount
print cols, ' ',rows, ' ' ,bands

# Getting georeference info
geotransform = ds.GetGeoTransform()
originX = geotransform[0]
originY = geotransform[3]
pixelWidth = geotransform[1]
pixelHeight = geotransform[5]
print originX, ' ', originY, ' ', pixelWidth, ' ', pixelHeight

# Reading the pixel 1,1 of the band no. 1
x = originX
y = originY
xOffset = int((x - originX) / pixelWidth)
yOffset = int((y - originY) / pixelHeight)
band = ds.GetRasterBand(1) 
data = band.ReadAsArray(xOffset, yOffset, 1, 1) # Here offset are 0


print 'Band Type=',gdal.GetDataTypeName(band.DataType)

min = band.GetMinimum()
max = band.GetMaximum()
if min is None or max is None:
	(min,max) = band.ComputeRasterMinMax(1)
print 'Min=%.3f, Max=%.3f' % (min,max)

if band.GetOverviewCount() > 0:
	print 'Band has ', band.GetOverviewCount(), ' overviews.'

if not band.GetRasterColorTable() is None:
	print 'Band has a color table with ', \
	band.GetRasterColorTable().GetCount(), ' entries.'
# Read the row # 1 of the band # 1	
scanline = band.ReadRaster( 0, 0, band.XSize, 1,band.XSize, 1, GDT_Float32 )
# Convert scanline
tuple_of_floats = struct.unpack('f' * band.XSize, scanline)

# Read the whole band
data2 = band.ReadAsArray(0, 0, cols, rows)

# Reading block by block in a band. The most efficient way to read data. Use one loop for the rows and one for the columns. Need to check that there is an entire block in both directions
blockSize = band.GetBlockSize()
xBSize = blockSize[0]
yBSize = blockSize[1]
count = 0
# loop through the rows	
for i in range(0, rows, yBSize):
	if i + yBSize < rows:
		numRows = yBSize
	else:
		numRows = rows - i
	# loop through the columns	
	for j in range(0, cols, xBSize):
		if j + xBSize < cols:
			numCols = xBSize
		else:
			numCols = cols - j
		# read the data and do the calculations		
		data = band.ReadAsArray(j, i, numCols, numRows).astype(numpy.float)
		mask = numpy.greater(data, 1000)
		count = count + numpy.sum(numpy.sum(mask))		
		print "i: ", i, '   j:', j

# print results
print 'Number of pixels > 1000:', count	

plt.imshow(mask)
plt.show()	

# Converting array data types
#data = data.astype(numpy.float) # using numpy
# Can do it in one step in the loop just above.
# data = band.ReadAsArray(j, i, nCols, nRows).astype(Numeric.Float)

# Creating a mask. Say we want to do some processing on all pixels with a value greater than 0. Syntax is the same for numpy
#mask = numpy.greater(data, 1000)
#print numpy.sum(numpy.sum(mask))

	

	
#print data[0,0]

#for row in range(rows):
#	for col in range(cols):
#		 data = band.ReadAsArray(xOffset, yOffset, row+1, col+1)
#		 print row, ' ', col
		 
#print numpy.mean(data)