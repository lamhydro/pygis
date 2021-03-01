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

outdir = 'Z:\\Luis\NationalLandCoverDatabase_USA\\2001\\nlcd_2001_landcover_2011_edition_2014_10_10\\nlcd_2001_landcover_2011_edition_2014_10_10\\'
outdir = "E:\\SouthSaskRiv_SPARROW\\sourcesVariables\\LandUse\\"
inRaster = outdir + 'nlcd_2001_landcover_2011_edition_2014_10_10_BBoldman.tif' 
outRaster = outdir + 'nlcd_2001_landcover_2011_edition_2014_10_10_BBoldman_proj.tif' 
cmd = 'gdalwarp -overwrite' + ' -t_srs ' + '"'+wkt +'"'+ ' ' + inRaster + ' ' + outRaster
print cmd
print os.system(cmd) # if is 0 is normal execution