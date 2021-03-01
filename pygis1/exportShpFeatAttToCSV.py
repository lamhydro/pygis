#import GdalOgrPylib as go
import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import ogr
from osgeo import osr

dir = 'W:\\HowardAmanda_SRB_Water_Quality\\Database of SK Stations (WQ and Flow)'
filename = 'WQ_Sask.shp'
shpFile = os.path.join(dir, filename)
dir = 'E:\\WaterQualityData'
filename = 'WQ_Sask.csv'
csvFile =  os.path.join(dir, filename)
shpFileTableIntoCSV(shpFile, csvFile)