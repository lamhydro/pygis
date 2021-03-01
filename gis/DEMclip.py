# Cliping a raster with feature geometrty.

# By: Luis Morales, GIWS

# Updated: 26 Jun 13

# Warnings:

import sys, os
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.1\\arcpy')
sys.path.append('C:\\Python27\\ArcGIS10.1')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.1\\bin')
import arcpy

#object = r'E:\GeoBase\CDED\redDeerRiverDEM\redDeerRiverCatch.shp'
#raster = r'E:\GeoBase\CDED\redDeerRiverDEM\reddeerdempr'
object = r'E:\Red_deer_SPARROW\GIS\redDeerRiverCatch.shp'
#raster = r'E:\PRISM\MeanTempGrids\tmean_14_PrXY_redDeer_r30.tif'
raster = r"E:\GeoBase\CDED\redDeerRiverDEM_50k\reddeerdempr.tif"
#object = r'E:\Red_deer_SPARROW\GIS\redDeerRiverCatch.shp'
#raster = r'E:\CaPAdata\preciAv2002_2013_PrXY_RedDeer_r30.tif'
#objFile = '/NHN_05DC000_1_0_WORKUNIT_LIMIT_2.shp'
#raster = '/demnhn05dc000'

rasterClip = r'E:\PRISM\MeanTempGrids\tmean_14_PrXY_redDeer_r30_Cli.tif'
rasterClip = r"E:\GeoBase\CDED\redDeerRiverDEM_50k\demprcli.tif"
# set workspace environment
#arcpy.env.workspace = dirPath

# Clip Raster Dataset with feature geometry
#rasterPath = os.path.join(rasterDir, rasterFile)
#objPath = os.path.join(objDir, objFile)
#rasterPathCl = os.path.join(rasterDir, rasterFileClip)
#rasterPath = rasterDir  + rasterFile
#objPath = objDir + objFile
#rasterPathCl = rasterDir + rasterFileClip

#print objPath
#print rasterPath
#print rasterPathCl

arcpy.Clip_management(raster, "#", rasterClip, object, "0", "ClippingGeometry")
#arcpy.Clip_management(rasterPath, "#", rasterPathCl, objPath, "0", "ClippingGeometry")