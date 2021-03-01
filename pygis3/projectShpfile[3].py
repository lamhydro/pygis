# Delete all stream who lenght is <= to the catchment DEM resolution.

import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
#if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
#    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import numpy as np 

# Projecting the shapefile
workDir = "G:\\QuAppelle_SPARROW\\subcatchDelineation"
#file0 = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.shp"
file0 = r"G:\QuAppelle_SPARROW\nonContriAreas\HYD_AAFC_INCRML_NON_CTRB_DRAIN_QuAppelle2.shp"
#file0 = r"G:\QuAppelle_SPARROW\nonContriAreas\HYD_AAFC_INCRML_NON_CTRB_DRAIN.shp"
#inDirFilename = r"E:\GeoBase\NHNQuAppelle\nhn_merged\WORKUNIT_LIMIT_2.shp"
inDirFilename = r"G:\QuAppelle_SPARROW\subcatchDelineation\CatchmentFWaBu2.shp"
#inDirFilename = r'G:\QuAppelle_SPARROW\subcatchDelineation\QuAppelleRivBasinContour.shp'
fn = 'CatchmentFWaBu2_reproj.shp'
#fn = 'QuAppelleRivBasinContour_proj2.shp'
typeOfGeom = 'polygon'
#projectShpfileIntoXY_New(workDir, file0, inDirFilename, fn, typeOfGeom)
projectShpfileIntoXY(workDir, file0, inDirFilename, fn, typeOfGeom)