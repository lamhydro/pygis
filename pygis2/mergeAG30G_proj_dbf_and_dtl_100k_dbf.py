# Mergin two shapefiles. Note that the file fields and the field numbers are not the same.

import os, sys
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr

root = r"E:\AAFC Soils Data\ABandSK"

file1 = r"E:\AAFC Soils Data\SK\dtl_100k_dbf.shp"
file2 = r"E:\AgriAlbSoilsData\ag30gs\Ag30gs\AG30G_proj_dbf.shp"

nameMergedFile = 'AG30G_proj_dbf_and_dtl_100k_dbf.shp'
mergedFile = os.path.join(root, nameMergedFile)
## if file exists, delete it ##
if os.path.isfile(mergedFile):
        os.remove(mergedFile)
		
# Merging files		
cmd = 'ogr2ogr ' + '"'+ mergedFile+'"' + ' ' + '"'+file1+'"'
print os.system(cmd)
# Merge (append) 'file2' to the 'main' file
cmd = 'ogr2ogr -update -append ' + '"'+ mergedFile+'"' + ' ' + '"'+file2+'"' + ' -nln ' + nameMergedFile[:-4] 
print os.system(cmd)		
		

# Clipping the resulting merged file using Red-Deer catchment contour.
sourcefile = mergedFile
outputfile = mergedFile[:-4]+'RedDeer.shp'
extentfile = r'E:\GeoBase\CDED\redDeerRiverDEM\redDeerRiverCatchPrXY.shp'
cmd = 'ogr2ogr -f "ESRI Shapefile" -clipsrc ' + extentfile + ' "'+outputfile+'" ' + '"'+sourcefile+'"' 
print cmd
print os.system(cmd)
 

		