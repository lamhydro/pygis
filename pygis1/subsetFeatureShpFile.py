# import modules
def subsetFeatuShp(condition,shapefileOut,shapefileIn):
	"""
	Extract a subset of features from a shapefile using ''where''
	"""
	cmd = 'ogr2ogr -f "ESRI Shapefile" -where ' + condition+ ' "'+shapefileOut+'"' + ' ' + shapefileIn
	print cmd
	#print os.system(cmd) # if is 0 is normal execution
  
	return (os.system(cmd))

import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal
from osgeo import ogr
from osgeo import osr


# Input information
shapefileIn  = r'E:\aafcWatershed2012\shpFiles\HYD_AAFC_MAJOR_BASIN_aux_proj.shp'
#shapefileIn  = r'E:\aafcWatershed2012\shpFiles\HYD_AAFC_PF_SUB_BASIN_aux_proj.shp'
fieldname = 'MAJOR_BASI'
#fieldname = 'SUBBASIN_P'
fieldvalue = ['Saskatchewan River']
#fieldvalue = ['Red Deer River', 'North Saskatchewan River', 'Battle River', 'Bow River','Oldman River','Seven Persons Creek','Bigstick Lake','South Saskatchewan River','Sounding Creek','Swift Current Creek','Eagle Creek','Carrot River','Saskatchewan River']
shapefileOutDir = r'E:\SaskRiv_SPARROW\GenMaps'
shapefileOutName = 'SaskRivBasin.shp'
#shapefileOutName = 'SaskRivSubBasins.shp'
shapefileOut = os.path.join(shapefileOutDir, shapefileOutName)
	
# if file exists, delete it ##
if os.path.isfile(shapefileOut):
	 os.remove(shapefileOut)

# Subset of features from a  shapefile
condition='"'
lengthfieldvalue = len(fieldvalue)
for fieldval in fieldvalue:
 
	#condition += '"'+fieldname+'='+"'"+str(fieldval)+"'"+'"'
	condition += fieldname+'='+"'"+str(fieldval)+"'"
	if lengthfieldvalue > 1:
		condition +=' or '

if lengthfieldvalue > 1:
	condition =condition[:-4]		
condition +='"'
cmdOut = subsetFeatuShp(condition,shapefileOut,shapefileIn)
if not cmdOut:
	 print cmdOut, ': Normal Execution!'
else:
	 print cmdOut
