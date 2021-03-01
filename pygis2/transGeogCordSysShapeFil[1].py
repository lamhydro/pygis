import os, sys
from fnmatch import fnmatch
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr

#ogr2ogr -t_srs some_shapefile.prj output_vector.shp input_vector.shp
#Z:\Luis\STATSGO\merge_ussoils_10and17shp\reprojectShapeFil.py
some_shapefile_prj = r'E:\Red_deer_SPARROW\RiverNet2\CatchmentDef.prj'
output_vector = 'E:\\AAFC Soils Data\\Detailed_Soil_Survey_DSS_Compilations\\dss_v3_ab_20140529\\dss_v3_ab_dbf_trans.shp'
input_vector = 'E:\\AAFC Soils Data\\Detailed_Soil_Survey_DSS_Compilations\\dss_v3_ab_20140529\\dss_v3_ab_dbf.shp'
#cmd = 'ogr2ogr -t_srs ' + some_shapefile_prj + ' ' + output_vector + ' ' + input_vector 
# using EPSG:4269 to transform into 'GCS_North_American_1983'
cmd = 'ogr2ogr -t_srs EPSG:4269 '  + ' "'+ output_vector + '" ' + ' "'+ input_vector + '" '
print cmd
print os.system(cmd)