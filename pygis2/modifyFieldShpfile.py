import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import numpy as np 

# set directory
dir = "Z:\\Luis\\STATSGO\\merge_ussoilsAndcasoils"
os.chdir(dir) 

# Reading MUID and PERM (permeability)
MUIDs = np.genfromtxt(r'Z:\Luis\STATSGO\merge_ussoils_10and17shp\MUIDandPERM.csv', dtype=None, delimiter=',', skip_header=1,  usecols=0)
MUIDs = list(MUIDs)
PERMs = np.genfromtxt(r'Z:\Luis\STATSGO\merge_ussoils_10and17shp\MUIDandPERM.csv', dtype=None, delimiter=',', skip_header=1,  usecols=1)
PERMs = list(PERMs)

# Opening shape file
filename = 'ussoils_casoils.shp'
shfile, layer= openingShpFile(os.path.join(dir, filename))

# Reading field names and field types
layerFieldNames = getLayerFields(layer)

# Correct KSAT_IN_HR
feature = layer.GetNextFeature()
k = 0
KSAT_IN_HR = []
while feature:
	
	MUID = feature.GetField('MUID')
	if  MUID == None:
		KSAT_IN_HR.append(feature.GetField('KSAT_IN_HR'))
	else:
		idx = MUIDs.index(MUID)
		val = PERMs[idx]
		if val < 0.:
			val = 0.
		KSAT_IN_HR.append(val)
	
	print k	
		
	feature.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
	feature = layer.GetNextFeature()
	
	k += 1
#shfile.Destroy()

#sys.exit(0)
# Creating a new layer by modifiying fields of the original.
fieldnamesToChange = ['KSAT_IN_HR']
fieldvaluesToChange = [KSAT_IN_HR] # List of lists
copyShpFileModifyUserSpecFields(dir,filename[:-4]+'_modify.shp', layer, layerFieldNames, fieldnamesToChange, fieldvaluesToChange)

shfile.Destroy()
