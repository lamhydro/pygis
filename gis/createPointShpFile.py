def latDD(x):
  D = int(x[0:2])
  M = int(x[2:4])
  S = float(x[4:])
  DD = D + float(M)/60 + float(S)/3600
  return DD

def lonDD(x):
  D = int(x[0:3])
  M = int(x[3:5])
  S = float(x[5:])
  DD = D + float(M)/60 + float(S)/3600
  return DD

import arcpy, csv, os
from arcpy import env

#arcpy.ResetEnvironments()
arcpy.env.overwriteOutput = True


#Set variables
arcpy.env.workspace = "E:\\WaterQualityAndStreamFlowData\\waterQualityData\\staLocShapeFiles"
outFolder = arcpy.env.workspace
#pointFC = "NITRATE_STAT.shp"
pathCSVfiles = "E:\\WaterQualityAndStreamFlowData\\waterQualityData\\"
csvFiles = ["NITRATEstatInfo.csv", "NITROGEN DISSOLVED AMMONIAstatInfo.csv", "NITROGEN DISSOLVED NO3 & NO2statInfo.csv","NITROGEN DISSOLVEDstatInfo.csv", "NITROGEN TOTAL (CALCD.)statInfo.csv", "NITROGEN TOTAL AMMONIAstatInfo.csv","NITROGEN TOTAL KJELDAHLstatInfo.csv", "PHOSPHOROUS DISSOLVED ORTHOstatInfo.csv","PHOSPHOROUS TOTALstatInfo.csv"]
pointFC = ["NITRATEstatInfo.shp", "NITROGEN_DISSOLVED_AMMONIAstatInfo.shp", "NITROGEN_DISSOLVED_NO3NO2statInfo.shp","NITROGEN_DISSOLVEDstatInfo.shp", "NITROGEN_TOTAL_CALCDstatInfo.shp", "NITROGEN_TOTAL_AMMONIAstatInfo.shp","NITROGEN_TOTAL_KJELDAHLstatInfo.shp", "PHOSPHOROUS_DISSOLVED_ORTHOstatInfo.shp","PHOSPHOROUSTOTALstatInfo.shp"]
existShapefileForSRef = "W:\\HowardAmanda_SRB_Water_Quality\\Database of SK Stations (WQ and Flow)\\WQ_Sask.shp"

#Create shapefile and add field
# Deleting existing file
#if os.path.isfile(outFolder +  pointFC):
#   os.remove(outFolder +  pointFC)

# Getting the spatial reference
spatial_reference = arcpy.Describe(existShapefileForSRef).spatialReference

j = 0
for csvFile in csvFiles:

  #Create shapefile and add field
   arcpy.CreateFeatureclass_management(arcpy.env.workspace, pointFC[j], "POINT", "", "", "", spatial_reference)
   arcpy.AddField_management(pointFC[j], "STID", "TEXT","","", 16)
   arcpy.AddField_management(pointFC[j], "LON", "DOUBLE","","", 16)
   arcpy.AddField_management(pointFC[j], "LAT", "DOUBLE","","", 16)

   statLoc = open(pathCSVfiles + csvFile, "rb")

   headerLine = statLoc.readline()
   #print headerLine
   #I updated valueList to remove the '\n'
   valueList = headerLine.strip().split(",")
   #print valueList
   dateValueIndex = valueList.index('"Station.No"')
   latValueIndex = valueList.index('"Latitude..deg.min.sec."')
   lonValueIndex = valueList.index('"Longitude..deg.min.sec."')


   # Read each line in csv file
   cursor = arcpy.InsertCursor(pointFC[j])
   i = 0
   for point in statLoc.readlines():
      i += 1
      segmentedPoint = point.strip().split(",")
      # Get the lat/lon values of the current reading                    
      latValue = segmentedPoint[latValueIndex]
      lonValue = segmentedPoint[lonValueIndex]
      dateValue = segmentedPoint[dateValueIndex]
      vertex = arcpy.CreateObject("Point")
      vertex.ID = i 
      vertex.X = -1*lonDD(lonValue)
      vertex.Y = latDD(latValue)
      feature = cursor.newRow()
      feature.SHAPE = vertex
      feature.STID = dateValue
      feature.LON = vertex.X
      feature.LAT = vertex.Y
      cursor.insertRow(feature)
      del vertex
      del feature

   del cursor
   statLoc.close()
   j += 1