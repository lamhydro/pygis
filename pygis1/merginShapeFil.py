# Merge a bunch of shapefiles with attributes quickly!
import arcpy

# HD_WATERBODY_2
files = [
    r'E:\GeoBase\NHN\nhn_rhn_05ca000_shp_en\NHN_05CA000_1_0_HN_HYDROJUNCT_0.shp',
    r'E:\GeoBase\NHN\nhn_rhn_05cb000_shp_en\NHN_05CB000_1_0_HN_HYDROJUNCT_0.shp',
    r'E:\GeoBase\NHN\nhn_rhn_05cc000_shp_en\NHN_05CC000_1_0_HN_HYDROJUNCT_0.shp',
    r'E:\GeoBase\NHN\nhn_rhn_05cd000_shp_en\NHN_05CD000_1_0_HN_HYDROJUNCT_0.shp',
    r'E:\GeoBase\NHN\nhn_rhn_05ce000_shp_en\NHN_05CE000_1_0_HN_HYDROJUNCT_0.shp',
    r'E:\GeoBase\NHN\nhn_rhn_05cf000_shp_en\NHN_05CF000_1_0_HN_HYDROJUNCT_0.shp',
    r'E:\GeoBase\NHN\nhn_rhn_05cg000_shp_en\NHN_05CG000_1_0_HN_HYDROJUNCT_0.shp',
    r'E:\GeoBase\NHN\nhn_rhn_05ch000_shp_en\NHN_05CH000_1_0_HN_HYDROJUNCT_0.shp',
    r'E:\GeoBase\NHN\nhn_rhn_05cj000_shp_en\NHN_05CJ000_1_0_HN_HYDROJUNCT_0.shp',
    r'E:\GeoBase\NHN\nhn_rhn_05ck000_shp_en\NHN_05CK000_1_0_HN_HYDROJUNCT_0.shp'
         ]

arcpy.env.workspace = r'E:\Red_deer_SPARROW\GIS'
arcpy.Merge_management(files,'NHNHydrojunct.shp')

#return

#w = shapefile.Writer()
#for f in files:
#  r = shapefile.Reader(f)
#  w._shapes.extend(r.shapes())
#  w.records.extend(r.records())
#w.fields = list(r.fields)
#w.save("merged")
