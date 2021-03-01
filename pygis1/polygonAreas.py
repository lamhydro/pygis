import arcpy
arcpy.env.workspace = r'C:\Users\Luis\Downloads\nhn_rhn_05ck000_shp_en'
arcpy.CalculateAreas_stats('NHN_05CK000_1_0_HD_WATERBODY_2.shp','areaWaterbody.shp')
