# Name: PolylineToRaster.py
# Description: Converts polyline features to a raster dataset.
# Requirements: ArcInfo

# Import system modules
import arcpy
from arcpy import env

# Set environment settings
env.workspace = "E:/Red_deer_SPARROW/RiverNet/nhn_Red_Deer_Riv"

# Set local variables
inFeatures = "NHNFlowline_def1.shp"
valField = "OBJECTID" 
outRaster = "E:/Red_deer_SPARROW/RiverNet/nhn_Red_Deer_Riv/NHNFlowline_def1.tif"
assignmentType = "MAXIMUM_COMBINED_LENGTH"
priorityField = "PRIORITY"
cellSize = 0.001 # 0.0001

# Execute PolylineToRaster
arcpy.PolylineToRaster_conversion(inFeatures, valField, outRaster, 
                                  assignmentType, priorityField, cellSize)
