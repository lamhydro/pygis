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
from osgeo import ogr
from osgeo import osr
import numpy as np
import csv

os.chdir("E:\\Documents\\NutrientsLecture2\\Maps") 

# Opening the catchment shapefile
file1 = 'Catchment.shp'
shfile1, layer1 = openingShpFile(file1)
# - Getting the spatial projection
geoSRlayer1 = layer1.GetSpatialRef()

# Opening the soiltype shapefile
file2 = r'E:\AAFC Soils Data\SK\dtl_100k_dbf.shp'
shfile2, layer2 = openingShpFile(file2)
# - Getting the spatial projection
geoSRlayer2 = layer2.GetSpatialRef()

# Transforming SR of layer2 into layer1's
coordTrans = osr.CoordinateTransformation(geoSRlayer2, geoSRlayer1)

feature1 = layer1.GetNextFeature()
i = 0
ofile  = open('KSAT_IN_HR_ave.csv', "wb")
writer = csv.writer(ofile)
header = ['SPARROWID','KSAT_IN_HR_ave']
writer.writerow(header)
while feature1:

	catch = feature1.GetGeometryRef()
	
	layer2.ResetReading() #need if looping again
	feature2 = layer2.GetNextFeature()
	cnt = 0
	interAr = 0
	KSAT_IN_HR_ave = 0
	while feature2:
		soil = feature2.GetGeometryRef()
		soil = soil.Clone()  
		soil.Transform(coordTrans)
		
		if catch.Intersect(soil):
			
			polyInter = catch.Intersection(soil)
			KSAT_IN_HR_ave += polyInter.GetArea()*feature2.GetField('KSAT_IN_HR')
			interAr += polyInter.GetArea()
			cnt += 1

		# destroy the features
		feature2.Destroy()
		feature2 = layer2.GetNextFeature()
	
	 
	if cnt == 0:
		KSAT_IN_HR_ave = 0
	else:
		KSAT_IN_HR_ave = KSAT_IN_HR_ave/interAr
	
	print 'Catch. No.: ',i ,' # of soil poly inter: ', cnt
	print 'Average KSAT_IN_HR: ', KSAT_IN_HR_ave
	
	writer.writerow([int(i),\
					float(KSAT_IN_HR_ave)])
	
	# destroy the features
	feature1.Destroy()
	feature1 = layer1.GetNextFeature()
	i += 1
	#if i == 1:
	#	break

ofile.close()

# close the data sources
shfile1.Destroy()
shfile2.Destroy()