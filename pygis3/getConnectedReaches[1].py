import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
from osgeo import ogr
from osgeo import osr
import numpy as np 

# set directory
dir = r"W:\Luis\forElmira\geometry"
os.chdir(dir) 

# Opening Flowline shape file
filename = r'W:\Luis\forElmira\geometry\NLFLOW_1v12_proj.shp'
#csvfile = r'W:\Luis\forElmira\SPARROWinputData\quardata.csv'
shfile, layerFlowline = openingShpFile(filename)

# Reading field names and field types
layerFlowlineFieldNames = getLayerFields(layerFlowline)

# Getting fields values
fields = ['FROM_JUNCT']
dummy = readLayerField(layerFlowline,fields)
FROM_JUNCTs = [item for sublist in dummy  for item in sublist]
layerFlowline.ResetReading() 
fields = ['TO_JUNCT']
dummy = readLayerField(layerFlowline,fields)
TO_JUNCTs = [item for sublist in dummy  for item in sublist]
shfile.Destroy()
	
# Extracting connected streams between and upstream and a downstream.
# - For Gleniffer Lake (Red Deer river)
#upstream = 72092
#downstream = 78229
# - For Oldman River Dam (Oldman river)
#upstream = 31505
#downstream = 30068
streamFID = [2599, 14485, 6562, 9368, 9992, 10343, 14664, 11848, 11701, 6371, 3758, 11847]
streamNames = ['MooseJaw', 'Ekapo', 'Iskwao', 'JumpingDeer', 'LastMountain', 
				'Loon', 'Pearl', 'Pheasant', 'RedFox', 'Ridge', 'Wascana', 'Indianhead']
#listOfStreams.append(upstream)
sys.setrecursionlimit(2000000000)	
#listOfStreams = getConnectedStreamsBetweenUpstreamAndDownstream(upstream, downstream, FROM_JUNCTs, TO_JUNCTs,  listOfStreams)
for i,j in zip(streamFID,streamNames):
	print ''
	print i, ' ', j
	listOfStreams = []
	listOfStreams.append(i)
	FROM_JUNCTs, TO_JUNCTs, listOfStreams = lookThroughRN(i, FROM_JUNCTs, TO_JUNCTs, listOfStreams)

	# Writing into csv file
	np.savetxt('connectedReaches_'+j+'.csv',listOfStreams,delimiter=',',fmt='%d',comments='')
	#np.savetxt('FIDriv_OldmanRivDam.csv',listOfStreams,delimiter=',',fmt='%d',comments='')