# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 08:51:34 2015

@author: lmorales
"""

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')
        
def writeNumpyArrayToRaster(lon, lat, array, filename,NoDataValue, proj):
    ## if file exists, delete it ##
    if os.path.isfile(filename):
        os.remove(filename)
   
    xmin,ymin,xmax,ymax = [lon.min(),lat.min(),lon.max(),lat.max()]
    nrows,ncols = np.shape(array)
    xres = (xmax-xmin)/float(ncols)
    yres = (ymax-ymin)/float(nrows)
    geotransform=([xmin,xres,0,ymax,0, -yres])   
    # That's (top left x, w-e pixel resolution, rotation (0 if North is up), 
    #         top left y, rotation (0 if North is up), n-s pixel resolution)
    # I don't know why rotation is in twice???
    
    output_raster = gdal.GetDriverByName('GTiff').Create(filename,ncols, nrows, 1 ,gdal.GDT_Float32)  # Open the file
    
    output_raster.SetGeoTransform(geotransform)  # Specify its coordinates
    #srs = osr.SpatialReference()                 # Establish its coordinate encoding
    #srs.ImportFromEPSG(4269)                     # This one specifies WGS84 lat long.
                                                 # Anyone know how to specify the 
                                                 # IAU2000:49900 Mars encoding?
    #output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system 
                                                       # to the file
    output_raster.SetProjection(proj)
    outBand = output_raster.GetRasterBand(1)
    outBand.WriteArray(array)   # Writes my array to the raster    
    outBand.SetNoDataValue(NoDataValue)
    outBand.FlushCache()
    outBand.GetStatistics(0, 1)
    
# Project raster file
# - inRaster: unprojected raster file
# - outRaster: projected raster file
# - proj: Projection information. Usually from a proj. raster. 
def projectRaster(inRaster, outRaster, proj):
    #outdir = "Z:\\Luis\\PCIC\\"
    #inRaster = outdir + 'test.tif' 
    #outRaster = outdir + 'test_prj.tif' 
    cmd = 'gdalwarp -overwrite' + ' -t_srs ' + '"'+proj +'"'+ ' ' + inRaster + ' ' + outRaster
    print cmd
    print os.system(cmd) # if is 0 is normal execution  
    
# Getting the projection of a shape file.
# - filename: shape file name, including the path.
def getShpFileProj(filename):
    #file = 'E:\\SouthSaskRiv_SPARROW\\RivNet3\\CatchmentDemFillV1_proj.shp'
    shfile, layer = openingShpFile(filename)
    geoSR = layer.GetSpatialRef()
    proj = geoSR.ExportToWkt()
    shfile.Destroy()
    return proj    
    
def plotMultipleMaps(lon,lat, data_dec, var, data_units):
    # Get some parameters for the Stereographic Projection
    lon_0 = lon.mean()
    lat_0 = lat.mean()
    #m = Basemap(width=5000000,height=3500000,
    #            resolution='l',projection='stere',\
    #            lat_ts=40,lat_0=lat_0,lon_0=lon_0)
    
    # projection, lat/lon extents and resolution of polygons to draw
    # resolutions: c - crude, l - low, i - intermediate, h - high, f - full
    # ll (lower left) ur (upper right)
    m = Basemap(projection='merc',llcrnrlon=lon.min(),llcrnrlat=lat.min(),urcrnrlon=lon.max(),urcrnrlat=lat.min(),resolution='i') 
                
    # Because our lon and lat variables are 1D, 
    # use meshgrid to create 2D arrays 
    # Not necessary if coordinates are already in 2D arrays.
    lons, lats = np.meshgrid(lon, lat)
    xi, yi = m(lons, lats)  
    
    for i in range(len(data_dec)):
        plt.figure()
        # Plot Data
        cs = m.pcolor(xi,yi,np.squeeze(data_dec[i]))
        
        # Add Grid Lines
        m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
        m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)
        
        # Add Coastlines, States, and Country Boundaries
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()
        
        # Add Colorbar
        cbar = m.colorbar(cs, location='bottom', pad="10%")
        cbar.set_label(data_units)
        
        # Add Title
        plt.title(var)
        
        plt.show() 
        
def XminYminXmaxYmax_raster(rasterfile):
    
    dataset = gdal.Open(rasterfile, GA_ReadOnly)
    if dataset is None:
        print 'Could not open file'
        sys.exit(1)
    
    # Raster characteristics    
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize    
    geotransform = dataset.GetGeoTransform()
    #originX = geotransform[0]
    #originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    
    # Raster dimensions
    xmin = geotransform[0]
    ymin = geotransform[3]-pixelHeight*rows
    xmax = geotransform[0]+pixelWidth*cols
    ymax = geotransform[3]
    
    # Close raster file    
    dataset = None
    
    return ([xmin, ymin, xmax, ymax])
    
# Resampling a raster.
# - rasterIn: input raster name
# - rasterOut: name of the resampled raster
# - rasterDim: xmin ymin xmax and ymax of a raster e.g. '-76.1800000 2.8100000 -74.4000000 5.3700000'           
# - xres: x resolution of resampling
# - yres: y resolution of resampling    
def resamplingRaster(rasterIn, rasterOut, rasterDim, xres, yres):
    
    cmd = 'gdalwarp -ts ' + xres + ' '+ yres + ' -r "cubic" -te ' + rasterDim + ' ' + rasterIn + ' ' + rasterOut 
    print cmd
    print os.system(cmd) # if is 0 is normal execution 


from netCDF4 import Dataset
import numpy as np
import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
if "C:\\Python27\\ArcGIS10.1\\Lib\\site-packages" not in sys.path:
    sys.path.append("C:\\Python27\\ArcGIS10.1\\Lib\\site-packages")
from osgeo import gdal
#from osgeo import ogr
from osgeo import osr
#from gdalconst import *
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Closing all figures
plt.close("all")

# Data directory
dir = 'Z:\\Luis\\PCIC\\'
#dir = 'G:\\Data\\PCIC\\'

# Escenario directory
escena = 'rcp26' #


# Stat. downscale method
stdown = 'BCSD' # "BCSD" "BCCAQ"

# Variable
#var = 'tasmax' # 'tasmax' 'pr' 'tasmin'

# Initial date
dateini = '19500101'

# End date
dateend = '21001231'

fileProj = 'E:\\SouthSaskRiv_SPARROW\\RivNet3\\CatchmentDemFillV1_proj.shp'

# subdirectory
subdir = 'historicalAND' + escena + '\\'

# GCModel
gcms = ['CanESM2'] # ['CanESM2','HadGEM2-ES','MPI-ESM-LR','GFDL-ESM2G','MIROC5']

for gcm in gcms:
    print gcm
    # Filenames
    filenames = []
    #for ext in ['.nc.nc','.nc (1).nc','.nc (2).nc']:
    for ext in ['.nc.nc']:    
        filenames.append('pr+tasmax+tasmin_day_'+ stdown + '+ANUSPLIN300+' + gcm + '_historical+' + escena + '_r1i1p1_'+ dateini + '-' + dateend + ext)
    #pr+tasmax+tasmin_day_BCSD+ANUSPLIN300+CanESM2_historical+rcp26_r1i1p1_19500101-21001231.nc
    
    for filename in filenames:
        
        print '-->', filename
        
        # Path to file
        pathToFile = dir + subdir + filename
        
        # Open ncdf file
        try:
            nc = Dataset(pathToFile, mode='r')
        except RuntimeError, e:
            print 'Unable to open *.nc file'
            print e
            sys.exit(1)
        
        # Print variable names
        varNames = []
        for f in nc.variables:
            varNames.append(f)
            print(f)
        
        # Set time array
        time = nc.variables['time'][:]
        ntime = len(time) 
        timeNew = []
        year = 1950
        for day in range(ntime):
            dummy = datetime.date(int(year),01,01) + datetime.timedelta(days=day)
            dummy = str(dummy)
            dummy = dummy.replace("-","")
            timeNew.append(int(dummy))
        time=np.array(timeNew) 
        
        # Set lon and lat
        lon = nc.variables['lon'][:]
        lat = nc.variables['lat'][:]
        
        # main variable
        var = varNames[3]
        data_units = nc.variables[var].units 
        
        # 30 years average
        dummy = nc.variables[var][0]*0.
        j = 1
        delta =  ntime/5
        data_dec = []  
        for i in range(ntime):
            print i    
            if j == delta:
                data_dec.append(dummy/delta)
                dummy = nc.variables[var][0]*0.
                j = 1
            else:
                dummy += nc.variables[var][i]
                j+=1
        
        nc.close()
        
        per = np.arange('1950', '2110', np.timedelta64(30, 'Y'))
        #ndec =
        j = 0
        #for i in range(len(data_dec)):
        for i in range(1):    
            
            print '----> ' + var + ' Period: ' + per[j].astype(str) + '_' +per[j+1].astype(str)
            
            # Saving into raster file
            # - Getting projection
            #inDataset = gdal.Open('E:\\SouthSaskRiv_SPARROW\\land_to_waterDeliVar\\pcp30_14_PrXY_BB_SSKR_r30.tif')
            #proj = inDataset.GetProjection()
                
            proj = getShpFileProj(fileProj)
            
            # - Flipping the matrix as the origin point is in the upper left corner.            
            reversed_arr = np.flipud(data_dec[0])
            # - Writing into raster file
            rasterfile = dir + subdir + var + '_' + gcm + '_' + escena +'_'+ per[j].astype(str) + '-' + per[j+1].astype(str) + '.tif'
            #rasterfile = 'Z:\\Luis\\PCIC\\test.tif'
            writeNumpyArrayToRaster(lon, lat, reversed_arr, rasterfile,-32768, proj)
        
            # Project raster file
            #projectRaster(rasterfile, rasterfile[:-4] + '_prj.tif', proj)
            #if os.path.isfile(rasterfile):
            #			os.remove(rasterfile)
                
            # Clipping raster file with shapefile Bounding Box
            #clippingRasterFilewithShapefile(rasterfile,
            #                                'E:\\SouthSaskRiv_SPARROW\\maps\\SouthSaskRivBasinContour_proj2.shp',
            #                               rasterfile[:-4] + '_prj_BB.tif')
            #if os.path.isfile(rasterfile[:-4] + '_prj.tif'):
            #			os.remove(rasterfile[:-4] + '_prj.tif')                                
            
            # Resampling raster file
            #if os.path.isfile(rasterfile[:-4] + '_prj_BB.tif'):
            #			os.remove(rasterfile[:-4] + '_prj_BB.tif')
            j +=1                                  
            
        
        # Spatial average data
        #dataSpaAv = [] 
        #for i in range(ntime):
        #    print(i)
        #    data = nc.variables[var][i]
        #    dataSpaAv.append(data.mean())
        
         
        # Decadal average
        #window_size = len(time)/150
        #dataSpaAv_dec = movingaverage(dataSpaAv, window_size)
        
          
        
        # Plotting spatial average data at daily time steps
        #plt.plot(time, dataSpaAv)
        #plt.plot(time, dataSpaAv_dec,'r')
        #plt.ylabel(data_units)
        #plt.xlabel('Day')
        #plt.show()
            
        #dummy = nc.variables[var][0] + nc.variables[var][1]
        

        
        
