import sys, os
sys.path.append('/home/lmm333/Dropbox/Public/pyLib')
from GdalOgrPylib import  * # Personal library
from osgeo import ogr
from osgeo import osr
import numpy as np 

# Projecting the shapefile
workDir = "/media/Data3/athabasca_RBM/ARB_CAPA" 
file0 = "/media/Data3/MESH/MESH_SED_ARB/ARB_map/sediment_data/sediment_data/Athabasca_river_basin_station_alberta_parks_sediment_location.shp"
inDirFilename = "/media/Data3/athabasca_RBM/ARB_CAPA/MESH_drainage_database.shp"
fn = 'MESH_drainage_database_proj.shp'
typeOfGeom = 'polygon'

projectShpfileIntoXY(workDir, file0, inDirFilename, fn, typeOfGeom)
