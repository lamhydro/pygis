
import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
import numpy as np 

# Projecting the shapefile
workDir = "E:\\SouthSaskRiv_SPARROW\\maps"
file0 = "E:\\Red_deer_SPARROW\\RiverNet2\\CatchmentDef.shp"
inDirFilename = "E:\\SouthSaskRiv_SPARROW\\maps\\SouthSaskRivBasinContour_proj.shp"
fn = 'SouthSaskRivBasinContour_proj2.shp'
typeOfGeom = 'polygon'

workDir = "E:\\SouthSaskRiv_SPARROW\\maps"
file0 = "Z:\\Luis\\HYD_AAFC_INCRML_NON_CTRB_DRAIN_FGDB (1)\\HYD_AAFC_INCRML_NON_CTRB_DRAIN.shp"
inDirFilename = "E:\\SouthSaskRiv_SPARROW\\maps\\SouthSaskRivBasinContour_proj2.shp"
fn = 'SouthSaskRivBasinContour_proj3.shp'
typeOfGeom = 'polygon'

workDir = "E:\\SouthSaskRiv_SPARROW\\maps"
file0 = "E:\\SouthSaskRiv_SPARROW\\maps\\SouthSaskRivBasin.shp"
inDirFilename = "E:\\SouthSaskRiv_SPARROW\\maps\\drain_l_prj_SSKRnetwork.shp"
fn = 'drain_l_prj_SSKRnetwork_proj.shp'
typeOfGeom = 'line'

workDir = "W:\\Luis\QuAppelle\\QuAppelle River shoreline\\Cross_Section\\Cross_Section"
file0 = "W:\Luis\QuAppelle\QuAppelle River shoreline\y_quapp_Sshore_elevation.shp"
inDirFilename = "W:\\Luis\QuAppelle\\QuAppelle River shoreline\\Cross_Section\\Cross_Section\\Waypoints_sonarAppelle.shp"
fn = 'Waypoints_sonarAppelle_proj.shp'
typeOfGeom = 'point'

#W:\Luis\QuAppelle\QuAppelle River shoreline\Cross_Section\Cross_Section\projectShpfile.py

projectShpfileIntoXY_New(workDir, file0, inDirFilename, fn, typeOfGeom)