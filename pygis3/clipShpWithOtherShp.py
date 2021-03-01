import sys, os
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr

clipshape = r'G:\QuAppelle_SPARROW\subcatchDelineation\QuAppelleRivBasinContour_proj.shp'
clipshape = r'H:\QuAppelle_SPARROW\subcatchDelineation\CatchmentFWaBu2_clippV2_merge.shp'
inshape   = r'G:\QuAppelle_SPARROW\QuAppelleRiverNetwork\HYD_AAFC_INCRML_NON_CTRB_DRAIN.shp'
inshape   = r'H:\QuAppelle_SPARROW\subcatchDelineation\QuAppelleRivBasinContour_proj.shp'
outshape  = r'G:\QuAppelle_SPARROW\subcatchDelineation\HYD_AAFC_INCRML_NON_CTRB_DRAIN_Clip.shp'
outshape  = r'H:\QuAppelle_SPARROW\subcatchDelineation\CatchmentFWaBu2_clippV2_merge_holes.shp'

cmd = 'ogr2ogr -clipsrc ' + clipshape + ' ' + outshape + ' ' + inshape
print cmd
print os.system(cmd) # if it is 0, it is normal execution!
