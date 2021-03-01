# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 20:54:58 2015

@author: lmorales
"""

def read_WFD_land_lat_long_z_nc(filename):
  fh = Dataset(filename, mode='r')
  
  #print fh.variables.keys
  # Saving variables
  land = fh.variables['land'][:]
  Longitude = fh.variables['Longitude'][:]
  Latitude = fh.variables['Latitude'][:]
  #Grid_lat = fh.variables['Grid_lat'][:]
  #Grid_lon = fh.variables['Grid_lon'][:]
  Z = fh.variables['Z'][:]
  
  #print fh.variables.keys.units
   
  fh.close()
  return(land, Longitude, Latitude, Z) 


from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas
from pandas import Series, DataFrame

# Reading 'WFD-land-lat-long-z.nc'
land2, Longitude, Latitude, Z = read_WFD_land_lat_long_z_nc('/home/lmorales/Documents/WATCH_WFD/WFD-land-lat-long-z.nc')

years = ['1955','1956','1957','1958','1959','1960','1961','1962','1963','1964','1965']
#years = ['1955']
months = ['01','02','03','04','05','06','07','08','09','10','11','12']
#months = ['01','02']
variable = 'Rainf_WFD_CRU' #['Tair_WFD', 'LWdown_WFD', 'SWdown_WFD', 'PSurf_WFD', 'Wind_WFD','Rainf_WFD_CRU'] # CHANGE HERE!!!!!!!!!!
units = '[mm/s]' #'[W/m2]' '[oC]' '[Pa]' 

dir_name = '/media/lmorales/My Book/data/WATCH_WFD/' + variable

# Bounding box
lon_lim = (-127.750,-120.503) # min, max
lat_lim = (54.126, 58.000) # 

varBBspatMeanAll = np.array([])
varBBmaxAll = np.array([])
varBBminAll = np.array([])
i = 0
tntime = 0
for year in years:
  for month in months:


    # Open ncdf file
    base_filename = variable + '_' + year + month + '.nc'
    print 'Reading: ', base_filename
    nc_file = os.path.join(dir_name, base_filename)
    fh = Dataset(nc_file, mode='r')

    #print fh.variables.keys

    # Saving variables
    nav_lon = fh.variables['nav_lon'][:]
    nav_lat = fh.variables['nav_lat'][:]
    land = fh.variables['land'][:]
    time = fh.variables['time'][:]
    timestp = fh.variables['timestp'][:]
    if variable == 'Rainf_WFD_CRU':
        var = fh.variables['Rainf'][:]
    else:
        var = fh.variables[variable[:-4]][:] # CHANGE HERE!!!!!!!!!!

    fh.close()

    # Slicing lon,lat vectors using the bounding box
    idxLon = np.where((Longitude >= lon_lim[0]) & (Longitude <= lon_lim[1]))[0]
    lonBB = Longitude[idxLon]
    mask = (Longitude >= lon_lim[0]) & (Longitude <= lon_lim[1])
    lonBBunique = np.unique(lonBB)

    latMask = mask*Latitude
    idxLat = np.where((latMask >= lat_lim[0]) & (latMask <= lat_lim[1]))[0]
    latBB = Latitude[idxLat]
    latBBunique = np.unique(latBB)
    latBBunique = sorted(latBBunique,reverse=True)

    # Slicing variable matrix
    varBB = var[:,idxLat]
    if variable == 'Tair_WFD':
    	varBB = varBB - 273.15 # From Fare to Cel
    varBBspatMean = varBB.mean(axis=1)
    varBBmax = varBB.max(axis=1)
    varBBmin = varBB.min(axis=1)

    # dimensions
    ntime = len(time)
    m = len(latBBunique)
    n = len(lonBBunique)
    tntime += ntime

    # Stacking arrays
    varBBspatMeanAll = np.r_[varBBspatMeanAll,varBBspatMean]
    varBBmaxAll = np.r_[varBBmaxAll,varBBmax]
    varBBminAll = np.r_[varBBminAll,varBBmin]

    i += 1

dTime = int(time[1]-time[0])
timeAll = range(0,dTime*tntime,dTime)

t = []
iniDate = years[0]+'-'+months[0]+'-'+'01T00:00'
for i in timeAll:
    aux=np.datetime64(iniDate) + np.timedelta64(i, 's')
    t.append(aux)
t1 = np.array(t)

tsMean = Series(varBBspatMeanAll, index=t1)
tsMax = Series(varBBmaxAll, index=t1)
tsMin = Series(varBBminAll, index=t1)


aonao = DataFrame({'Mean' : tsMean, 'Max' : tsMax, 'Min' : tsMin})

aonao.plot()
plt.ylabel(variable + ' ' + units)
figfile = dir_name + '/' + variable + '.png'
savefig(figfile)
#ts.plot()

    
#plt.plot(t1,a)
#plt.ylabel('PSurf [pa]')
#plt.show()


