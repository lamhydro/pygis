# Delete all stream who lenght is <= to the catchment DEM resolution.

import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import numpy as np 

# Projecting the shapefile
workDir = r'Z:\Luis\HYD_AAFC_INCRML_NON_CTRB_DRAIN_FGDB (1)'
file0 = r'E:\SouthSaskRiv_SPARROW\maps\SouthSaskRivBasinContour_proj2.shp'
#file0 = r'E:\AAFC Soils Data\ABandSK\AG30G_proj_dbf_and_dtl_100k_dbfRedDeer.shp'
#file0 = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.shp"
inDirFilename = r'Z:\Luis\HYD_AAFC_INCRML_NON_CTRB_DRAIN_FGDB (1)\HYD_AAFC_INCRML_NON_CTRB_DRAIN.shp'
fn = 'HYD_AAFC_INCRML_NON_CTRB_DRAIN_reproj.shp'
typeOfGeom = 'polygon'
projectShpfileIntoXY(workDir, file0, inDirFilename, fn, typeOfGeom)

#filein = r'Z:\Luis\HYD_AAFC_INCRML_NON_CTRB_DRAIN_FGDB (1)\HYD_AAFC_INCRML_NON_CTRB_DRAIN.shp'
#fileout = r'Z:\Luis\HYD_AAFC_INCRML_NON_CTRB_DRAIN_FGDB (1)\HYD_AAFC_INCRML_NON_CTRB_DRAINnew.shp'
#cmd = 'ogr2ogr -t_srs EPSG:3857 ' + '"'+fileout + '" '+'"' + filein +'" '
#print cmd
#print os.system(cmd) # if is 0 is normal execution