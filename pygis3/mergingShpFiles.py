# 

import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr
#from osgeo import osr
#from gdalconst import *
import numpy as np 

# set directory
dir = r"W:\Luis\Colin_QuAppelle\Gross_areas"
os.chdir(dir) 

# Merging the shapefile with those merged elements and the shapefile with the unchanged elements.
#['05JG004', '05JG005','05JG007','05JG010','05JG011','05JG013','05JG014']
listOfShpfiles = [os.path.join(dir,'05JG004_gross_area.shp'), 
				os.path.join(dir,'05JG005_gross_area.shp'), 
				os.path.join(dir,'05JG007_gross_area.shp'),
				os.path.join(dir, '05JG010_gross_area.shp'),
				os.path.join(dir, '05JG011_gross_area.shp'),
				os.path.join(dir, '05JG013_gross_area.shp'),
				os.path.join(dir, '05JG014_gross_area.shp')]
mergedFile = os.path.join(dir,'gross_area.shp')
projec = 0 
mergeListOfShpfiles(listOfShpfiles, mergedFile, projec)	

# Create *.prj file
#spatialRef = osr.SpatialReference()
#spatialRef.ImportFromEPSG(26912)
#spatialRef = osr.SpatialReference()
#spatialRef.ImportFromEPSG(2927)   

#spatialRef.MorphToESRI()
#file = open('effective_area.prj', 'w')
#print spatialRef.ExportToWkt()
#file.write(spatialRef.ExportToWkt())
#file.close()

# # Open shape file
# input_file = 'effective_area.shp'
# driver = ogr.Open(input_file).GetDriver()
# datasource = driver.Open(input_file, 0)
# input_layer = datasource.GetLayer()

# dest_srs = ogr.osr.SpatialReference()
# dest_srs.ImportFromEPSG(32632)
# dest_layer = output_data_source.CreateLayer(table_name,
                            # dest_srs,
                            # input_layer.GetLayerDefn().GetGeomType(),
                            # 'OVERWRITE=YES', 'GEOMETRY_NAME=geom', 'DIM=2', 'FID=id')

# # adding fields to new layer
# layer_definition = ogr.Feature(input_layer.GetLayerDefn())
# for i in range(layer_definition.GetFieldCount()):
    # dest_layer.CreateField(layer_definition.GetFieldDefnRef(i))

# # adding the features from input to dest
# for i in range(0, input_layer.GetFeatureCount()):
    # feature = input_layer.GetFeature(i)
    # dest_layer.CreateFeature(feature)

# input_layer.Destroy()



# # shfileCatch, layer = openingShpFile(file)

# # SR = osr.SpatialReference()
# # SR.SetWellKnownGeogCS("NAD83");

# # # Getting the spatial projection
# # #geoSR = layer.GetSpatialRef(inSpatialRef)
# # wkt = SR.ExportToWkt()
# # print 'Spatial projection:', wkt

# #shfileCatch.Destroy()
