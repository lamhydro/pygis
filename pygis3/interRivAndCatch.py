# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:13:04 2016

@author: lmm333
"""

import sys,os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
#if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
#    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal,ogr
#from osgeo import osr
import numpy as np 
import csv

# set directory
dir = r'H:\QuAppelle_SPARROW\subcatchDelineation'
os.chdir(dir)

# Opening the river shapefile
file1 = 'NLFLOW_1v12_proj.shp'
shfile1, layer1 = openingShpFile(file1)
# - Getting the spatial projection
geoSRlayer1 = layer1.GetSpatialRef()

# Opening catchment shapefile
file2 = 'CatchmentFWaBu2_clippV2.shp'
#file2 = 'stationInfoPHOSPHORUS TOTAL (P).shp'
shfile2, layer2 = openingShpFile(file2)
# - Getting the spatial projection
geoSRlayer2 = layer2.GetSpatialRef()

# Coord. transformation
coordTrans = osr.CoordinateTransformation(geoSRlayer2, geoSRlayer1)

# Reading river order
NIDriv = list(np.genfromtxt('streamOrderV2.csv', dtype=None, delimiter=',', skip_header=1,  usecols=0))
StreamOrder = list(np.genfromtxt('streamOrderV2.csv', dtype=None, delimiter=',', skip_header=1,  usecols=1))

#NIDriv = []
#GridIDcat = []
#with open('NIDrivAndGridIDcatDef.txt', 'r') as f:
#    # do things with your file
#	header = f.readline()
#	for line in f:
#		columns = line.split()
#		NIDriv.append(columns[0])
#		GridIDcat.append(int(columns[1]))

# 
i = 0
feature1 = layer1.GetNextFeature()
isubcAll = []
#isubcVaAll = []
#rivNoSubc = []

with open('rivMatchSubcV2.csv', "wb") as ofile:
    writer = csv.writer(ofile)
    writer.writerow(['NIDriv','NIDcatch','Linter(m)','RivOr'])
    
    while feature1:
        print 'Matching river %s and subcatchment' % i    
        
        riv = feature1.GetGeometryRef()
        
        layer2.ResetReading() #need if looping again
        feature2 = layer2.GetNextFeature()
        j = 0
        isubc = []
        isubcVa = [] 
        while feature2:
            #print j
            catch = feature2.GetGeometryRef()
            if catch != None:
                catch = catch.Clone()  
                catch.Transform(coordTrans)
                cond1 = catch.Intersect(riv)
                
                
                cond2 = riv.Within(catch)
                #if not cond1 and not cond2:
                if  cond1 or  cond2:    
                    isubc.append(j)
                    intersection = catch.Intersection(riv)
                    isubcVa.append(intersection.Length())
            
            # destroy the features
            feature2.Destroy()
            feature2 = layer2.GetNextFeature()
            j += 1
        
        
        if  isubcVa == []:
            #isubcAll.append(None)
            val = None
            valMax = None
        else:
            idmax = isubcVa.index(max(isubcVa))
            #isubcAll.append(isubc[idmax])
            val = isubc[idmax]
            valMax = max(isubcVa)
            
        writer.writerow([NIDriv[i], val, valMax, StreamOrder[i] ])    

        #if i == 10:
        #    break
        # destroy the features
        feature1.Destroy()
        feature1 = layer1.GetNextFeature()    
        
        i += 1
        


# close the data sources
shfile1.Destroy()
shfile2.Destroy()

