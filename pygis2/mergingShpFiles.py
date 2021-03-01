# Delete all stream who lenght is <= to the catchment DEM resolution.

import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
#from osgeo import osr
#from gdalconst import *
import numpy as np 

# set directory
dir = "E:\\AAFC Soils Data\\Detailed_Soil_Survey_DSS_Compilations\\merged_dss"
os.chdir(dir) 

# Merging the shapefile with those merged elements and the shapefile with the unchanged elements.
listOfShpfiles = [os.path.join('E:\\AAFC Soils Data\\Detailed_Soil_Survey_DSS_Compilations\\dss_v3_ab_20140529','dss_v3_ab_dbf_trans.shp'), 
				os.path.join('E:\\AAFC Soils Data\\Detailed_Soil_Survey_DSS_Compilations\\dss_v3_mb_20130716','dss_v3_mb_dbf.shp'), 
				os.path.join('E:\\AAFC Soils Data\\Detailed_Soil_Survey_DSS_Compilations\\dss_v3_sk_20130506','dss_v3_sk_dbf.shp')]

#listOfShpfiles = [ 
#				os.path.join('E:\\AAFC Soils Data\\Detailed_Soil_Survey_DSS_Compilations\\dss_v3_mb_20130716','dss_v3_mb_dbf.shp'), 
#				os.path.join('E:\\AAFC Soils Data\\Detailed_Soil_Survey_DSS_Compilations\\dss_v3_sk_20130506','dss_v3_sk_dbf.shp')]	
			
mergedFile = os.path.join(dir,'dss_ab_mn_sk_dbf.shp')

projec = 0 
mergeListOfShpfiles(listOfShpfiles, mergedFile, projec)	
