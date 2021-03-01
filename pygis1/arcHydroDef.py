
import sys, os
#sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.1\\arcpy')
#sys.path.append('C:\\Python27\\ArcGIS10.1')

# IMPORTANT NOTES:
# 1) Run without any layer or raster activated in the current arcmap document.
# 2) Specify the complete path for every file.

import arcpy
from arcpy import env
from arcpy.sa import *

FillSinks 						= 0
FlowDirection 					= 0
AdjustFlowDirectioninLakes		= 0
FlowAccumulation				= 0
StreamDefinition				= 0
StreamSegmentation				= 0
CatchmentGridDelineation		= 0
CatchmentPolyProcessing			= 1
DrainageLineProcessing			= 1
AdjointCatchment				= 1
DrainagePointProcessing			= 1
HydroNetworkGeneration			= 1

sys.path.append('C:\\Program Files (x86)\\ESRI\\WaterUtils\\ArcHydro\\bin')

#arcpy.ImportToolbox("C:\Program Files (x86)\ArcGIS\Desktop10.1\ArcToolbox\Toolboxes\Arc Hydro Tools.tbx", "archydrotools")

import ArcHydroTools

arcpy.CheckOutExtension("Spatial")

env.overwriteOutput = "1"


#env.workspace = r'E:\Red_deer_SPARROW\RiverNet2'

#ArcHydroTools.SetBatchTargetLocations("E:\\Red_deer_SPARROW\\RiverNet\\nhn_Red_Deer_Riv\\demprcli")
#SetTargetLocations(in_appconfig=None, in_mapname=None, in_rasterlocation=None, in_vectorlocation=None)
ArcHydroTools.SetTargetLocations("HydroConfig", "Layers",
                                 "E:\\Red_deer_SPARROW\\RiverNet2",
                                 "E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb")

#sys.exit(0)

# WARNING LevelDEM does not work using the NHNWaterbody.shp since there is a problem asociated with the shp file.
#print 'Leveling the DEM\n' # RUN ALONE !!!!
#ArcHydroTools.LevelDEM("demprcli", "NHNWaterbody.shp", "E:\\Red_deer_SPARROW\\RiverNet2\\LevelDEM", "")



#print 'DEM reconditioning\n'
#DEMReconditioning(in_rawdem_raster=None, in_agreestream_features=None, number_cells_buffer=None, zdrop_smooth=None, zdrop_sharp=None, out_agreedem_raster=None, raise_negative=None)
#ArcHydroTools.DEMReconditioning("LevelDEM", "NHNFlowline_def1.shp", "5", "10", "1000", "AgreeDEM")

#print 'Assign Stream Slope\n'
#GenerateFNodeTNode(in_line_features=None)
#ArcHydroTools.GenerateFNodeTNode("NHNFlowline_def1.shp")
#AssignStreamSlope(in_stream_features=None, number_start_elevation=None, number_drop_elevation=None)
#ArcHydroTools.AssignStreamSlope("NHNFlowline_def1.shp", "10000", "10")

if FillSinks:
    print 'Fill Sinks \n' #OK
    #FillSinks(in_dem_raster=None, out_hydrodem_raster=None, fill_threshold=None, in_deranged_poly_features=None, use_issinkfield=None)
    #ArcHydroTools.FillSinks("E:\\Red_deer_SPARROW\\RiverNet2\\demprcli", "E:\\Red_deer_SPARROW\\RiverNet2\\FilAll", "", "", "")
    #print 'Fill Sinks 2\n'
    #ArcHydroTools.FillSinks("E:\\Red_deer_SPARROW\\RiverNet2\\filall", "FilSink", "", "E:\Red_deer_SPARROW\GIS2\GIS2.gdb\\Layers\\SinkPoly", "1")

if FlowDirection: 
    print 'Flow direction \n' # OK
    #ArcHydroTools.FlowDirection_archydro(in_hydrodem_raster, {in_external_wall_features}, out_flow_direction_raster)
    ArcHydroTools.FlowDirection("E:\\Red_deer_SPARROW\\RiverNet2\\filall",
                                "E:\\Red_deer_SPARROW\\RiverNet2\\FdrFilled","")

if AdjustFlowDirectioninLakes:
    print 'Adjust Flow Direction in Lakes \n' # OK (but not used)
    #AdjustFlowDirectioninLakes(in_flow_direction_raster=None, in_lake_features=None, in_stream_raster=None, out_bowlflowdirection_raster=None):
    ArcHydroTools.AdjustFlowDirectioninLakes("E:\\Red_deer_SPARROW\\RiverNet2\\FdrFilled",
                                             "E:\\Red_deer_SPARROW\\RiverNet2\\NHNWaterbody.shp",
                                             "E:\\Red_deer_SPARROW\\RiverNet2\\NHNFlowline_def1.tif",
                                             "E:\\Red_deer_SPARROW\\RiverNet2\\bowlfdr")

if FlowAccumulation:
    print 'Flow Accumulation \n' # OK (Does not work using bowlfdr. Using fdrfilled instead.)
    #FlowAccumulation(in_flow_direction_raster=None, out_flow_accumulation_raster=None)
    ArcHydroTools.FlowAccumulation("E:\\Red_deer_SPARROW\\RiverNet2\\fdrfilled",
                                   "E:\\Red_deer_SPARROW\\RiverNet2\\Fac")

if StreamDefinition:
    print 'Stream Definition \n'  # OK (Fac need to be included plus the path.)
    number_cells = 200
    area_sqkm = number_cells*(475.561132/65007) # Check this values directly from the arcHydro tools in arcGIS
    #StreamDefinition(in_flowaccumulation_raster=None, number_cells=None, out_stream_raster=None, area_sqkm=None)
    ArcHydroTools.StreamDefinition("E:\\Red_deer_SPARROW\\RiverNet2\\Fac",
                                   number_cells,"E:\\Red_deer_SPARROW\\RiverNet2\\Str",
                                   area_sqkm)

if StreamSegmentation:
    print 'Stream Segmentation \n'  # OK
    #StreamSegmentation(in_stream_raster=None, in_flow_direction_raster=None, out_streamlink_raster=None, in_sink_watershed_raster=None, in_sink_link_raster=None)
    ArcHydroTools.StreamSegmentation("E:\\Red_deer_SPARROW\\RiverNet2\\Str",
                                     "E:\\Red_deer_SPARROW\\RiverNet2\\FdrFilled",
                                     "E:\\Red_deer_SPARROW\\RiverNet2\\StrLnk", "", "")

if CatchmentGridDelineation:
    print 'Catchment Grid Delineation \n' # OK
    #CatchmentGridDelineation(in_flow_direction_raster=None, in_link_raster=None, out_catchment_raster=None)
    ArcHydroTools.CatchmentGridDelineation("E:\\Red_deer_SPARROW\\RiverNet2\\fdrfilled",
                                           "E:\\Red_deer_SPARROW\\RiverNet2\\strlnk",
                                           "E:\\Red_deer_SPARROW\\RiverNet2\\Cat")

if CatchmentPolyProcessing:
    print 'Catchment Polygon Processing \n' # OK 
    #CatchmentPolyProcessing(in_catchment_raster=None, out_catchment_features=None)
    ArcHydroTools.CatchmentPolyProcessing("E:\\Red_deer_SPARROW\\RiverNet2\\cat",
                                          "E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\Catchment")

if DrainageLineProcessing:
    print 'Drainage Line Processing \n' # OK
    #DrainageLineProcessing(in_link_raster=None, in_flow_direction_raster=None, out_drainageline_features=None)
    ArcHydroTools.DrainageLineProcessing("E:\\Red_deer_SPARROW\\RiverNet2\\strlnk",
                                         "E:\\Red_deer_SPARROW\\RiverNet2\\fdrfilled",
                                         "E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\DrainageLine")

# Produce a blank feature file, so it need:
# 1) set the right path in ApUtilities -> Set Target Locations -> HydroConfig. 
# 2) active in arcMap the two shapefile DrainageLine and Catchment
# 3) from hydrotools choose the option: Terrain Preprocessing -> Adjoint Catchment Processing
# 4) AdjointCatchment feature is created. Contain the upstream accumulated areas of the DrainID catchment. DrainID coincide with the HydroID in the catchment feature.
if AdjointCatchment: # Neet to be 
    print 'Adjoint Catchment Processing \n'
    #AdjointCatchment(in_drainageline_features=None, in_catchment_features=None, out_adjoint_features=None)
    ArcHydroTools.AdjointCatchment("E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\DrainageLine",
                                   "E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\Catchment",
                                   "E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\AdjointCatchment")

if DrainagePointProcessing:
    print 'Drainage point processing \n'
    #DrainagePointProcessing(in_flowacc_raster=None, in_catchment_raster=None, in_catchment_features=None, out_drainagepoint_features=None)
    ArcHydroTools.DrainagePointProcessing("E:\\Red_deer_SPARROW\\RiverNet2\\Fac",
                                          "E:\\Red_deer_SPARROW\\RiverNet2\\cat",
                                          "E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\Catchment",
                                          "E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\DrainagePoint")

if HydroNetworkGeneration:
    print ' Hydro Network Generation \n'
    #HydroNetworkGeneration(in_drainageline_features=None, in_catchment_features=None, in_drainagepoint_features=None, network_name=None, out_hydroedge_features=None, out_hydrojunction_features=None):
    ArcHydroTools.HydroNetworkGeneration("E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\DrainageLine",
                                         "E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\Catchment",
                                         "E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\DrainagePoint",
                                         "ArcHydro", "E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\HydroEdge",
                                         "E:\\Red_deer_SPARROW\\RiverNet2\\riverNet2.gdb\\Layers\\HydroJunction")
    
