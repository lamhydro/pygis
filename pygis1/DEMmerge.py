# Merging a series of raster files contained in multiple directories. Firstly, it copies all 
# raster in an directory 'deleteDir' and then using the arcpy routines merge all the rasters
# into a single file 'mergeDem'. At the end, 'deleteDir' is deleted.

# By: Luis Morales, GIWS

# Updated: 26 Jun 13

# Warnings:
# 1) Delete all files related to mergeDem before executing the script.
import sys, os
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.1\\arcpy')
sys.path.append('C:\\Python27\\ArcGIS10.1')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.1\\bin')

import arcpy, shutil
from arcpy import env

# Input info
mainDir = r'E:\GeoBase\CDED\redDeerRiverDEM_50k'
deleteDir = 'temp'
mergeDem = 'RedDeerRivDEM'

# Create a temp dir
deleted = os.path.join(mainDir, deleteDir)
print deleted
if not os.path.exists(deleted):
            os.makedirs(deleted)
            #os.chmod(deleted, stat.S_IWRITE)
            print "created"

# Copying files to temp dir
listT = []
for directories in os.listdir(mainDir):
    dir = os.path.join(mainDir, directories)
    if os.path.isdir(dir) and (not dir == deleted):
        print  dir

        # Produce a list of raster datasets
        env.workspace = dir
        rasters = arcpy.ListRasters()

        # Copying rasters files into a directory
        for raster in rasters:
            raster = os.path.join(dir, raster)
            shutil.copy(raster, deleted)
            
        list = ";".join(rasters)
        listT.append(list)


# Joing the raster files into a list
listD = ";".join(listT)


# GEOPROCESING OPERARATION: Merging rasters
arcpy.env.overwriteOutput = 1 # Set overwrite
env.workspace = deleted
arcpy.MosaicToNewRaster_management(listD, mainDir, mergeDem, "", "", "", 1, "MINIMUM") 


# Deleting temp dir
if os.path.exists(deleted):
            shutil.rmtree(deleted)
            print "deleted"
