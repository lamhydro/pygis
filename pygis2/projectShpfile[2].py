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
workDir = "E:\\AAFC Soils Data\\ABandSK"
file0 = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.shp"
inDirFilename = "E:\\AAFC Soils Data\\ABandSK\\AG30G_proj_dbf_and_dtl_100k_dbf.shp"
fn = 'AG30G_proj_dbf_and_dtl_100k_dbf_proj.shp'
typeOfGeom = 'polygon'

projectShpfileIntoXY(workDir, file0, inDirFilename, fn, typeOfGeom)