# import required modulesa
from ftplib import FTP
import os

def handleDownload(block):
        file.write(block)
        print ".",
    
#Define the variables
ftpServer = 'ftp2.cits.rncan.gc.ca'  # or specify the IP address of the server
#ftpServer = r'ftp.chc.nrc.ca'
ftpUser = "anonymous"
#ftpUser = "sparrow-glftp"
ftpPass = "luis.marin@usask.ca"
#ftpPass = "nrc$ocre88!"
#ftpFilePath = ['/pub/geobase/official/cded/50k_dem/072/',	'/pub/geobase/official/cded/50k_dem/082/','/pub/geobase/official/cded/50k_dem/083/']
ftpFilePath = ['/pub/geobase/official/cded/50k_dem/063/']
#ftpFilePath = ['/pub/geobase/official/cded/50k_dem/073/']
#localDir = r"E:\GeoBase\CDED\redDeerRiverDEM"
localDir = r"W:\Luis\geobase\cded"
filematch = ''

# Set local dir, so that downloaded files are saved here.
os.chdir(localDir)

for ftpFilePa in ftpFilePath:
	
	print 'Conecting to server'

	ftp = FTP(ftpServer)
	ftp.login(ftpUser, ftpPass)
	ftp.cwd(ftpFilePa)
	ftp.retrlines('LIST')
	a=ftp.nlst(filematch)

	print 'Accessing files'
	
	for filename in ftp.nlst(filematch):
		# Open the file for writing in binary mode
		print 'Opening local file ' + filename
		file = open(filename, 'wb')

		# Download the file a chunk at a time
		# Each chunk is sent to handleDownload
		# We append the chunk to the file and then print a '.' for progress
		# RETR is an FTP command
		print 'Getting ' + filename
		ftp.retrbinary('RETR ' + filename, handleDownload)


		# Clean up
		print 'Closing file ' + filename
		file.close()

	print 'Closing FTP connection'
	ftp.close()

