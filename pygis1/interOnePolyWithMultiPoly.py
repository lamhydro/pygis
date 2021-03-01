# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 22:57:55 2016

@author: lmm333
"""


import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
from osgeo import ogr
from osgeo import osr
import numpy as np 
import csv

# set directory
dir = r"W:\JeffersonW\thuan"
os.chdir(dir) 

# Opening shape file
shfileOneP, layerOneP= openingShpFile('Slaveriver.shp')

shfileMulP, layerMulP= openingShpFile('rectangular.shp')


mulP = layerMulP.GetNextFeature()
oneP = layerOneP.GetNextFeature()
i = 0
with open('intersectArea.csv','w') as f1:
    writer=csv.writer(f1, delimiter=',',lineterminator='\n')
    writer.writerow(['ET_STATION', 'intersectArea_m2'])
    while mulP:
        cell = mulP.GetGeometryRef()
        poly = oneP.GetGeometryRef()
        
        
        if cell.Intersect(poly):
            inter = cell.Intersection(poly)
            ET_STATION  = mulP.GetField('ET_STATION')
            area = inter.GetArea()
            print ET_STATION, '  ', "Area = ", area, " m2"
            writer.writerow([ET_STATION, area])
        
        mulP.Destroy() # For memory management purposes we need to make sure that we get rid of things such as features when done with them
        mulP = layerMulP.GetNextFeature()
        
        i += 1
    
    oneP.Destroy()

# close the data sources
shfileOneP.Destroy()
shfileMulP.Destroy()