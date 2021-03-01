import os, sys
#if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
#    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
osgeopath = "C:/Program Files (x86)/GDAL"
path = "E:/Red_deer_SPARROW/RiverNet2/riverNet2.gdb"  # path to .shp files
newpath = "E:/Red_deer_SPARROW/RiverNet2"
newfilename = "AdjointCatchment.shp"
filename="AdjointCatchment"


#cmd = osgeopath + '/' + 'ogr2ogr ' + '-f "ESRI Shapefile" ' + '-where "GRID_CODE = 1" ' + path + '/' + newfilename + ' ' + path + '/' + filename
cmd = '"' +  osgeopath + '/' + 'ogrinfo"'  + path + ' ' + filename
print cmd
print os.system(cmd)
#cmd = '"' + osgeopath + '/' + 'ogr2ogr" ' + '-f "FileGDB" ' + path + ' ' + filename + ' ' + newpath + '/' + newfilename 
#cmd = '"' + osgeopath + '/' + 'ogr2ogr" ' + '-f "FileGDB" ' + '-where "NextDownID = -1" ' + path + ' ' + newfilename + ' ' + path + ' ' + filename
#print cmd
#print os.system(cmd)

