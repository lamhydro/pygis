# XXX

# By: Luis Morales, GIWS

# Updated: 26 Jun 13

# Warnings:

import arcpy

dirPath = r'E:\GeoBase\nhn_rhn_05dc000_shp_en'
filename = 'NHN_05DC000_1_0_WORKUNIT_LIMIT_2.shp'

# set workspace environment
arcpy.env.workspace = dirPath

try:
    # set local variables
    #in_dataset = "citylim_unk.shp" #"forest.shp"
    
    # get the coordinate system by describing a feature class
    #dirPathFilename = os.path.join(dirPath, filename)
    dsc = arcpy.Describe(filename)
    coord_sys = dsc.spatialReference
    print coord_sys
    
    # run the tool
    #arcpy.DefineProjection_management(in_dataset, coord_sys)
    
    # print messages when the tool runs successfully
    print(arcpy.GetMessages(0))
    
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))