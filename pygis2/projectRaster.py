#import GdalOgrPylib as go
import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from gdalconst import *


# Opening the shape file
file = r'E:\Red_deer_SPARROW\RiverNet2\CatchmentDef.shp'
shfile, layer = openingShpFile(file)

# Getting spatial projection
geoSR = layer.GetSpatialRef()
wkt = geoSR.ExportToWkt()

# close the data sources
shfile.Destroy()

outdir = 'Z:\\Luis\\CanadaDEM\\'
inRaster = outdir + 'dem_canada' 
outRaster = outdir + 'dem_canada_proj.tif' 
cmd = 'gdalwarp -overwrite' + ' -t_srs ' + '"'+wkt +'"'+ ' ' + inRaster + ' ' + outRaster
print cmd
print os.system(cmd) # if is 0 is normal execution