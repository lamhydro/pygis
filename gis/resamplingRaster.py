##====================================
##Resample
##Usage: Resample_management in_raster out_raster {cell_size} {NEAREST | BILINEAR | CUBIC | MAJORITY}

try:
    import arcpy
    #arcpy.env.workspace = "E:/Red_deer_SPARROW/RiverNet/nhn_Red_Deer_Riv"
    #arcpy.env.workspace = "E:/Runoff"
    #arcpy.env.workspace = "E:/CaPAdata"
    #arcpy.env.workspace = "E:/PRISM/MeanTempGrids"
    arcpy.env.workspace = "E:/AtmosphericDepo/CMAQ_RedDeer"
    ##Resample raster to a higher 10m x 10m resolution
    #arcpy.Resample_management("agreedem", "agreedemRes", "10", "CUBIC")
    #arcpy.Resample_management("runoff_14", "runoff_14_r30", "30", "CUBIC")
    #arcpy.Resample_management("preciAv2002_2013_PrXY_RedDeer.tif", "preciAv2002_2013_PrXY_RedDeer_r30.tif", "30", "CUBIC")
    arcpy.Resample_management("inpRas.tif", "out.tif", "30", "CUBIC")
except:
    print "Resample example failed."
    print arcpy.GetMessages()
