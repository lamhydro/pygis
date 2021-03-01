#! /usr/bin/python

from ftplib import FTP
import os
import os.path
import sys

######### WARNING DOWNLOAD MANUALLY 195705

def downloadFTPFiles(ftpServer, user, passwd, ftpFilePath, localDir,filename):
  
        print 'Conecting to server'
      
        ftp = FTP(ftpServer, user, passwd)
        #ftp.login()
        #print ftp.retrlines('LIST')
        ftp.cwd(ftpFilePath)
        #ftp.retrlines('LIST')
        #a=ftp.nlst(filematch)
  
        print 'Accessing files'
          
        #for filename in ftp.nlst(filematch):
        # Open the file for writing in binary mode
        print 'Opening local file ' + filename
        local_filename = os.path.join(localDir, filename)
        file = open(local_filename, 'wb')
  
        # Download the file a chunk at a time
        # Each chunk is sent to handleDownload
        # We append the chunk to the file and then print a '.' for progress
        # RETR is an FTP command
        print 'Getting ' + filename
        ftp.retrbinary('RETR ' + filename, file.write)

        # Clean up
        print 'Closing file ' + filename
        file.close()
            
        print 'Closing FTP connection'
        ftp.close()
        
        print '\n'
  

#variable='Tair_WFD'
#ftpServer = 'trmmopen.nascom.nasa.gov'  # or specify the IP address of the server
#ftpServer = 'gdata1.sci.gsfc.nasa.gov'
ftpServer = 'ftp.iiasa.ac.at'
#ftpMainDir = '/ftp/incoming/G3/OPS/cache/'
#ftpMainDir =  variable + '/'
#ftpSpecDir = 'TRMM_3B43.007'

scenario = 'B1' # 'B1' 'A2' 'Control'

model = 'IPSL' # 'CNRM' 'ECHAM5' 'IPSL'

## For CNRM
#if model == 'CNRM':
#    if variable in ['T','Tmin','Tmax','pr','pr_SNOWF']:
#        
#        if scenario == 'A2':
#            subdir = '/WorkBlock3/IPSL/BC/A2/'
#        elif scenario == 'B1':
#            subdir = '/WorkBlock3/IPSL/BC/B1/'
#        else:
#            subdir = '/WorkBlock3/IPSL/BC/Control/'
#    else:
#        if scenario == 'A2':
#            subdir = '/WorkBlock3/IPSL/Original_Gregorian/A2_yearly/'
#        elif scenario == 'B1':
#            subdir = '/WorkBlock3/IPSL/Original_Gregorian/B1_yearly/'
#        else:
#            subdir = '/WorkBlock3/IPSL/Original_Gregorian/20C3M_yearly/'     
#   

# For IPSL
biasCorre = 0
if model == 'IPSL':
    if biasCorre:
        variables = ['T','Tmin','Tmax','pr','pr_SNOWF']
        if scenario == 'A2':
            ftpFilePath = 'WorkBlock3/IPSL/BC/A2/'
        elif scenario == 'B1':
            ftpFilePath = 'WorkBlock3/IPSL/BC/B1/'
        else:
            ftpFilePath = 'WorkBlock3/IPSL/BC/Control/'
    else:
        variables = ['huss', 'ps', 'rsds','wss','soll','solldown','snowf','pr','tas']
        if scenario == 'A2':
            ftpFilePath = 'WorkBlock3/IPSL/Original_Gregorian/A2_yearly/'
        elif scenario == 'B1':
            ftpFilePath = 'WorkBlock3/IPSL/Original_Gregorian/B1_yearly/'
        else:
            ftpFilePath = 'WorkBlock3/IPSL/Original_Gregorian/20C3M_yearly/'     
years = ['2001','2002']

user = 'watch-r'
passwd = 'wWread77'

#IPCM4_SRB1_1_DM_huss_2001_0.5deg_land.nc.gz
#IPCM4_SRA2_1_DM_huss_2001_0.5deg_land.nc.gz
variables = ['wss','soll','solldown','snowf','pr','tas']

for variable in variables:
 for year in years:
     if biasCorre:
         filename = variable + '_BCed_1960_1999_' + year + '.nc.gz'
     else:
         filename = 'IPCM4_SR' + scenario + '_1_DM_' + variable + '_' + year + '_0.5deg_land.nc.gz'
         
     localDir = '/home/lmorales/Documents/WATCH_21st/' + ftpFilePath
     #ftpFilePath = ftpFilePath + filename
     downloadFTPFiles(ftpServer, user, passwd, ftpFilePath, localDir,filename)
