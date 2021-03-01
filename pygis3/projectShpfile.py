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
workDir = r"W:\Luis\Colin_QuAppelle\effective_areas"
file0 = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.shp"
inDirFilename = r'W:\Luis\Colin_QuAppelle\effective_areas\effective_area.shp'
fn = 'effective_area_proj.shp'
typeOfGeom = 'polygon'
projectShpfileIntoXY_New(workDir, file0, inDirFilename, fn, typeOfGeom)