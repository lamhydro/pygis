# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 14:52:09 2016

@author: lmm333
"""

import sys, os
#if r"C:\Anaconda\Lib\site-packages\PIL" not in sys.path:
#    sys.path.append(r"C:\Anaconda\Lib\site-packages\PIL")
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from gdalconst import *
import numpy as np
import csv

os.chdir(r"W:\Luis\Yanping")

ds = gdal.Open("G:\\data\\AAFC_LANDUSE\\2010landUse\\IMG_AAFC_LANDUSE_2010.tif")
if ds is None:
    print 'Could not open image'
    sys.exit(1)

cols = ds.RasterXSize
rows = ds.RasterYSize
bands = ds.RasterCount
    
geo_t = ds.GetGeoTransform()
xOrigin = geo_t[0]
yOrigin = geo_t[3]
pixelWidth = geo_t[1]
pixelHeight = geo_t[5]
yOrigin_low = yOrigin-rows*pixelHeight

filename = 'rasterFile.csv' 
if os.path.isfile(filename):
        os.remove(filename)
with open(filename,'w') as f:
    writer = csv.writer(f, delimiter=',',lineterminator='\n')
    xs = [xOrigin+pixelWidth*i for i in range(cols)]
    ys = [yOrigin_low+pixelHeight*i for i in range(rows)]
    writer.writerow(['Xs'])
    writer.writerow(xs)
    writer.writerow(['Ys'])
    writer.writerow(ys)
    
    for k in range(bands):
        band = ds.GetRasterBand(k+1)
        writer.writerow(['Band_' + str(k+1)])
        for i in range(rows):
    #        row = []
            print i
            data = band.ReadAsArray(0, i, cols, 1)
            #for j in range(cols):
            #    data = band.ReadAsArray(j, i, 1, 1)
                #if data == None:
                    
                #    row.append(-9999999)
                #else:
            #    row.append(data)
            writer.writerow(list(data[0]))
            #if i == 2:
            #    break

ds = None        

