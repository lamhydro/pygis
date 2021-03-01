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

# Data directory
dire = 'Z:\\Branko_NARCCAP_Files\\'

# Regional models (http://www.narccap.ucar.edu/data/model-info.html)
model = 'crcm' # 'crcm'  'ecp2'  'ECP2'  'hrm3'  'HRM3'  'mm5i'  'rcm3'  'RCM3'

# Global circulation models (http://www.narccap.ucar.edu/data/model-info.html)
driver = 'cgcm3' # 'ccsm'  'cgcm3'  'ncep' 'gfdl'  'hadcm3'

state = 'future' # 'current'  'future' ''

table = 'Table 3' # 'Table 1' 'Table 2' 'Table 3'

#Z:\Branko_NARCCAP_Files\NARCCAP crcm cgcm3-future Table 3
#Z:\Branko_NARCCAP_Files\NARCCAP crcm ncep Table 1

subdirState = dire + 'NARCCAP ' + model + ' ' +  driver + '-' + state + ' ' + table + '\\'
subdirNoState = dire + 'NARCCAP ' + model + ' ' +  driver + ' ' + table + '\\'


# see file Z:\Branko_NARCCAP_Files\DatabaseUpdates\ListOfParameters.txt for explanation
variable = 'prc' # 'tasmax'  'tasmin'  'pr'  'tas'  'ts'  'prc'  'prw'  'ta'  'huss' 'uas'  'vas' 'rlut' 'rsdt' 'rsut' 'rsds' 'rlds' 'mrro' 'mrros'

yearCu = '' # '1968' '1971'  '1976'  '1981'  '1986'  '1991'  '1996'
yearFu = '2038' # '2038' '2041'  '2046'  '2051'  '2056'  '2061'  '2066' 

#mrro_CRCM_cgcm3_2038010103
# nc file name
nc_file = subdirState + variable + '_' + model.upper() + '_' + driver + '_' + yearFu + '010103' + '.nc'

# Open ncdf file
nc = Dataset(nc_file, mode='r')
# Print variable names
varNames = []
for f in nc.variables:
    varNames.append(f)
    print(f)


time = nc.variables['time'][:]
lon = nc.variables['lon'][:]
lat = nc.variables['lat'][:]
mrros = nc.variables['prc'][:]

mrros_units = nc.variables['prc'].units    
    

nc.close()

# Remove nc file
#os.remove(nc_file)





scenario = 'A2' # 'B1' 'A2' 'Control'

model = 'IPSL' # 'CNCM3' 'ECHAM5' 'IPSL'

# For IPSL
biasCorre = 1
if model == 'IPSL':
    if biasCorre:
        variables = ['T','Tmin','Tmax','pr','pr_SNOWF']
        if scenario == 'A2':
            ftpFilePath = 'WorkBlock3/IPSL/BC/A2/'
        elif scenario == 'B1':
            ftpFilePath = 'WorkBlock3/IPSL/BC/B1/'
        else:
            ftpFilePath = 'WorkBlock3/IPSL/BC/Control/'
            years = [str(i) for i in range(1960,2001)]
    else:
        variables = ['huss', 'ps', 'rsds','wss','soll','solldown','snowf','pr','tas']
        if scenario == 'A2':
            ftpFilePath = 'WorkBlock3/IPSL/Original_Gregorian/A2_yearly/'
        elif scenario == 'B1':
            ftpFilePath = 'WorkBlock3/IPSL/Original_Gregorian/B1_yearly/'
        else:
            ftpFilePath = 'WorkBlock3/IPSL/Original_Gregorian/20C3M_yearly/'     
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
                gz_filename = variable + '_BCed_1960_1999_' + year + '.nc.gz'
            else:
                if scenario == 'A2' or scenario == 'B1':
                    gz_filename = 'IPCM4_SR' + scenario + '_1_DM_' + variable + '_' + year + '_0.5deg_land.nc.gz'
                else:
                    gz_filename = 'IPCM4_20C3M_1_DM_' + variable + '_' + year + '_0.5deg_land.nc.gz'
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
            if variable in ['huss', 'ps', 'rsds','wss','soll','solldown','snowf','pr','tas']:
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
                print nc.variables[varNames[3]].units
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
    