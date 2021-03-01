import os, sys
from fnmatch import fnmatch
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr

#ogr2ogr -t_srs some_shapefile.prj output_vector.shp input_vector.shp
#Z:\Luis\STATSGO\merge_ussoils_10and17shp\reprojectShapeFil.py
some_shapefile_prj = r'E:\Red_deer_SPARROW\RiverNet2\CatchmentDef.prj'
output_vector = r'Z:\Luis\STATSGO\merge_ussoils_10and17shp\ussoils_10and17_trans.shp'
input_vector = r'Z:\Luis\STATSGO\merge_ussoils_10and17shp\ussoils_10and17.shp'
#cmd = 'ogr2ogr -t_srs ' + some_shapefile_prj + ' ' + output_vector + ' ' + input_vector 
# using EPSG:4269 to transform into 'GCS_North_American_1983'
cmd = 'ogr2ogr -t_srs EPSG:4269 '  + output_vector + ' ' + input_vector 
print cmd
print os.system(cmd)