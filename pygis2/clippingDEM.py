# Clipping DEM

import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library

# Input to function
rasterIn = r'E:\SouthSaskRiv_SPARROW\land_to_waterDeliVar\pcp30_14_PrXY_BB_SSKR_r30.tif'
rasterIn = r'E:\SouthSaskRiv_SPARROW\sourcesVariables\LandUse\lcv_utm_aafc_30m_2000_v12More_SSKR_PrXY_BB_fillZeros.tif'
shpfile = r'E:\SouthSaskRiv_SPARROW\maps\SouthSaskRivBasinContour_proj2.shp'
rasterOut = r'E:\SouthSaskRiv_SPARROW\land_to_waterDeliVar\pcp30_14_PrXY_BB_SSKR_r30_clipp.tif'
rasterOut = r'E:\SouthSaskRiv_SPARROW\sourcesVariables\LandUse\lcv_utm_aafc_30m_2000_v12More_SSKR_PrXY_BB_fillZeros_clipp.tif'

#clippingRasterFilewithShapefile(rasterIn,shpfile,rasterOut)
clippingRasterFilewithShapefile2(rasterIn,shpfile,rasterOut)