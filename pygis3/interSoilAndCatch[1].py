import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import numpy as np
import csv

os.chdir(r"E:\SouthSaskRiv_SPARROW\land_to_waterDeliVar")

# Opening the catchment shapefile
file1 = 'E:\\SouthSaskRiv_SPARROW\\RivNet3\\CatchmentDemFillV1_proj.shp'
shfile1, layer1 = openingShpFile(file1)
# - Getting the spatial projection
geoSRlayer1 = layer1.GetSpatialRef()

# Opening the soiltype shapefile
file2 = 'ussoils_casoils_modify_SSKR_bbox.shp'
shfile2, layer2 = openingShpFile(file2)
# - Getting the spatial projection
geoSRlayer2 = layer2.GetSpatialRef()

# Transforming SR of layer2 into layer1's
coordTrans = osr.CoordinateTransformation(geoSRlayer2, geoSRlayer1)

feature1 = layer1.GetNextFeature()
i = 0
KSAT_IN_HR = []
GridIDs = []
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
	KSAT_IN_HR.append(KSAT_IN_HR_ave)
	GridIDs.append(feature1.GetField('GridID'))

	
	# destroy the features
	feature1.Destroy()
	feature1 = layer1.GetNextFeature()
	i += 1
	#if i == 1:
	#	break


# close the data sources
shfile1.Destroy()
shfile2.Destroy()

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

		
# Reordering sub. catch. slopes to streams. Writing into a file.
file = 'soilPermeability.csv'
with open(file,'w') as f1:
	writer=csv.writer(f1, delimiter=',',lineterminator='\n')
	writer.writerow(['FIDriv', 'KSAT_IN_HR'])
	for i,GridID in enumerate(GridIDcat):
		idx = GridIDs.index(GridID)
		row = [i,KSAT_IN_HR[idx]]
		writer.writerow(row)