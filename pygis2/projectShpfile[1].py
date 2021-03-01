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
workDir = "Z:\\Luis\\STATSGO\\merge_ussoils_10and17shp"
file0 = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.shp"
inDirFilename = "Z:\\Luis\\STATSGO\\merge_ussoils_10and17shp\\ussoils_10and17_trans.shp"
fn = 'ussoils_10and17_trans_proj.shp'
typeOfGeom = 'polygon'

projectShpfileIntoXY(workDir, file0, inDirFilename, fn, typeOfGeom)