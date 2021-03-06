# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 08:51:34 2015

@author: lmorales
"""

from netCDF4 import Dataset
import numpy as np
#import matplotlib.pyplot as plt
import os
import sys
import gzip
import datetime

#import glob
rootDir = '/home/lmorales/Documents/WATCH_21st/'
rootDir = '/media/lmorales/My Book/data/'

years = ['2001','2002']
years = [str(i) for i in range(2001,2101)]

scenario = '20C3M' # 'B1' 'A2' '20C3M'

model = 'ECHAM5' # 'CNCM3' 'ECHAM5' 'IPSL'

# For CNCM3
biasCorre = 0
if model == 'ECHAM5':
    if biasCorre:
        variables = ['T','Tmax','Tmin','pr','pr_PRSN']
        if scenario == 'A2':
            ftpFilePath = 'WorkBlock3/echam_bc_data_yearly/'
        elif scenario == 'B1':
            ftpFilePath = 'WorkBlock3/echam_bc_data_yearly/'
        else:
            ftpFilePath = 'WorkBlock3/echam_bc_data_yearly/'
            years = [str(i) for i in range(1960,2001)]
    else:
        variables = ['huss','ps','rlds','rls','rsds','wss']
        if scenario == 'A2':
            ftpFilePath = 'WorkBlock3/echam_data_yearly/scenario_A2/'
        elif scenario == 'B1':
            ftpFilePath = 'WorkBlock3/echam_data_yearly/scenario_B1/'
        else:
            ftpFilePath = 'WorkBlock3/echam_data_yearly/control/'
            years = [str(i) for i in range(1960,2001)]     
                
# Site location where the data is extracted from
ptLat = 49.581691
ptLon = -98.830418 

i = 0
dir_name = rootDir + ftpFilePath

for variable in variables:
    outfilename = variable + '_' + years[0] + '_' + years[len(years)-1] + '.dat'   
    fileout = os.path.join(dir_name, outfilename)
    #if i == 2:
    #    break 
    with file(fileout, 'w') as outfile:
        for year in years:
            print i
            
            # Uncompressing nc file
            if biasCorre:
                if scenario == 'A2' or scenario == 'B1':
            		gz_filename = scenario + '_' + variable + '_BCed_1960_1999_'+ year + '.nc.gz'
                else:
				gz_filename = variable + '_BCed_1960_1999_'+ year + '.nc.gz'	            
            else:
            	if scenario == 'A2' or scenario == 'B1':
            		gz_filename = 'MPEH5_SR' + scenario + '_3_DM_' + variable + '_' + year + '_0.5deg_land.nc.gz'
            	else:
            		gz_filename = 'MPEH5_' + scenario + '_3_DM_' + variable + '_' + year + '_0.5deg_land.nc.gz'	
            print 'Saving: ', gz_filename
            gz_file = os.path.join(dir_name, gz_filename) 
            #if os.path.isdir(gz_file) == False:
            inF = gzip.open(gz_file, 'rb')
            # uncompress the gzip_path INTO THE 's' variable
            s = inF.read()
            inF.close()
            # get gzip filename (without directories)
            gzip_fname = os.path.basename(gz_file)
            # get original filename (remove 3 characters from the end: ".gz")
            fname = gzip_fname[:-3]
            uncompressed_path = os.path.join(dir_name, fname)
            # store uncompressed file data from 's' variable
            open(uncompressed_path, 'w').write(s)
            
            # Open ncdf file
            nc_file = os.path.join(dir_name, gz_filename[:-3]) 
            nc = Dataset(nc_file, mode='r')
            # Print variable names
            varNames = []
            for f in nc.variables:
                varNames.append(f)
                print(f)
            
            #print nc.ncattrs()
            # Saving variables
            # Note: 'pr_SNOWF' only has time and snow    
            if variable != 'pr_SNOWF':    
                lon = nc.variables['lon'][:]
                print nc.variables['lon'].units
                lat = nc.variables['lat'][:]
                print nc.variables['lat'].units
            if variable in ['huss','ps','rlds','rls','rsds','wss']:
                time = nc.variables['time'][:]
                timeNew = []
                for day in range(len(time)):
                    dummy = datetime.date(int(year),01,01) + datetime.timedelta(days=day)
                    dummy = str(dummy)
                    dummy = dummy.replace("-","")
                    timeNew.append(int(dummy))
                time=np.array(timeNew)   
                
            else:    
                time = nc.variables['time'][:]
            print nc.variables['time'].units
            if variable != 'pr_SNOWF':  
                var = nc.variables[varNames[3]][:]
                #print nc.variables[varNames[3]].units
            else:
                var = nc.variables[varNames[1]][:]
                print nc.variables[varNames[1]].units
            
            nc.close()
            
            # Remove nc file
            os.remove(nc_file)
            
            # Getting the row and the column
            # Note: for 'pr_SNOWF' the row and the column
            # are the estimated for a variable in the
            # prior loop, 'pr'
            if variable != 'pr_SNOWF':
                delLat = abs(lat[:]-ptLat)
                idxLat = np.where(delLat == min(delLat))
                delLon = abs(lon[:]-ptLon)
                idxLon = np.where(delLon == min(delLon))
                
            
            # Slicing variable
            varTime = var[:,idxLat,idxLon]
            varTime=np.reshape(varTime, len(time))
            
            # Transforming variable units
            # - Temperature
            if variable == 'T' or variable == 'Tmax' or variable == 'Tmin' or variable == 'tas':
                varTime = varTime - 273.15 # From Fare to Cel
            # - Rainfall
            #if variable == 'pr':
                
                
            # Combining
            TimeAndVar = np.array([time,varTime])
            TimeAndVar = TimeAndVar.T
            
            # Saving into the file            
            np.savetxt(outfile, TimeAndVar)
            
            i += 1
    