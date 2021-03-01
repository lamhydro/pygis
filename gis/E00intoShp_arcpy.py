import arcpy
from arcpy import env
env.workspace = "E:/StatisticsCanada/AgrCensus2001"
arcpy.ImportFromE00_conversion("gcar000b03a_e.e00", "E:/StatisticsCanada/AgrCensus2001", "gcar000b03a_e")