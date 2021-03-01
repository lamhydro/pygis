# Merging features in a shape file

import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library

# Input to function
infile = r'E:\SouthSaskRiv_SPARROW\maps\SouthSaskRivBasin_proj.shp'
infile = r'E:\SaskRiv_SPARROW\GenMaps\SaskRivSubBasins_proj.shp'
outfile = r'E:\SouthSaskRiv_SPARROW\maps\SouthSaskRivBasinContour_proj.shp'
outfile = r'E:\SaskRiv_SPARROW\GenMaps\SaskRivSubBasinsContour_proj.shp'

common_attribute = 'PROVCD_2'
common_attribute = 'TEMPORAL' # This field was created on purpose to do the merging.

# Function to merge
mergeFeatuVectorFile(infile,outfile, common_attribute)