import sys
import arcpy
from arcpy import env
from arcpy.sa import *

sys.path.append('C:\\Program Files (x86)\\ESRI\\WaterUtils\\ArcHydro\\bin')

#arcpy.ImportToolbox("C:\Program Files (x86)\ArcGIS\Desktop10.1\ArcToolbox\Toolboxes\Arc Hydro Tools.tbx", "archydrotools")

import ArcHydroTools

arcpy.CheckOutExtension("Spatial")

env.overwriteOutput = "1"


env.workspace = r'E:\Red_deer_SPARROW\GIS2'

ArcHydroTools.SetBatchTargetLocations("E:\\Red_deer_SPARROW\\GIS2\\demprcli")
#SetTargetLocations(in_appconfig=None, in_mapname=None, in_rasterlocation=None, in_vectorlocation=None)
ArcHydroTools.SetTargetLocations("HydroConfig", "Layers", "E:\\Red_deer_SPARROW\\GIS2", "E:\\Red_deer_SPARROW\\GIS2\\GIS2.gdb")



print 'Leveling the DEM\n' # RUN ALONE !!!!
#ArcHydroTools.LevelDEM("E:\\Red_deer_SPARROW\\GIS2\\demprcli", "E:\\Red_deer_SPARROW\\GIS2\\NHNWaterbody2.shp", "E:\\Red_deer_SPARROW\\GIS2\\LevelDEM", "")

print 'DEM reconditioning\n'
#DEMReconditioning(in_rawdem_raster=None, in_agreestream_features=None, number_cells_buffer=None, zdrop_smooth=None, zdrop_sharp=None, out_agreedem_raster=None, raise_negative=None)
ArcHydroTools.DEMReconditioning("LevelDEM", "NHNFlowline2.shp", "5", "10", "1000", "AgreeDEM")

print 'Assign Stream Slope\n'
#GenerateFNodeTNode(in_line_features=None)
#ArcHydroTools.GenerateFNodeTNode("NHNFlowline2.shp")
#AssignStreamSlope(in_stream_features=None, number_start_elevation=None, number_drop_elevation=None)
#ArcHydroTools.AssignStreamSlope("NHNFlowline2.shp", "10000", "10")

print 'Burning Stream Slope\n'
#BurnStreamSlope(in_dem_raster=None, in_stream_features=None, out_streamslope_raster=None, out_editpoints_features=None)
#ArcHydroTools.BurnStreamSlope("AgreeDEM", "NHNFlowline2.shp", "E:\\Red_deer_SPARROW\\GIS2\\StrSlpDEM", "E:\Red_deer_SPARROW\GIS2\GIS2.gdb\\Layers\\EditPoints")

print 'Building walls\n'
#BuildWalls(in_dem_raster=None, innerwall_height=None, innerwall_buffer=None, breachline_buffer=None, out_walleddem_raster=None, in_external_wall_features=None, in_internal_wall_features=None, in_breachline_features=None)
#ArcHydroTools.BuildWalls("StrSlpDEM", "500", "0", "0", "WalledDEM", "redDeerRiverNHN.shp", "redDeerRiverNHN.shp", "NHNFlowline2.shp")

print 'Sink Prescreening\n'
#SinkPrescreen(in_rawdem_raster=None, prescreen_area=None, out_prefildem_raster=None, out_sink_raster=None)
#ArcHydroTools.SinkPrescreen("StrSlpDEM", "1000000", "PreFillDEM", "Sink")

print 'Sink Evaluation\n'
#SinkEvaluation(in_dem_raster=None, out_sink_features=None, out_sink_drainage_features=None)
#ArcHydroTools.SinkEvaluation("PreFillDEM", "E:\Red_deer_SPARROW\GIS2\GIS2.gdb\\Layers\\SinkPoly", "E:\Red_deer_SPARROW\GIS2\GIS2.gdb\\Layers\\SinkDA")

print 'Sink Selection\n'
#SinkSelection(in_deranged_poly_features=None, min_depth=None, min_area=None, min_volume=None, min_drainage_area=None, overwrite_selection=None)
ArcHydroTools.SinkSelection("E:\Red_deer_SPARROW\GIS2\GIS2.gdb\\Layers\\SinkPoly", "0", "0", "0", "5000000", "")

print 'Fill Sinks 1\n'
#FillSinks(in_dem_raster=None, out_hydrodem_raster=None, fill_threshold=None, in_deranged_poly_features=None, use_issinkfield=None)
ArcHydroTools.FillSinks("PreFillDEM", "FilAll", "", "", "")
print 'Fill Sinks 2\n'
ArcHydroTools.FillSinks("PreFillDEM", "FilSink", "", "E:\Red_deer_SPARROW\GIS2\GIS2.gdb\\Layers\\SinkPoly", "1")

    