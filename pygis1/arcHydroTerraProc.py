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

