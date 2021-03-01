import sys, os
import csv

# set directory
os.chdir("Z:\\Luis\\STATSGO\\merge_ussoils_10and17shp")

# Reading ascii file
with open('ussoils_100.muid_atts.txt', 'r') as f:

	with open('MUIDandPERM.csv','w') as f1:
		header = f.readline()
		
		writer = csv.writer(f1, delimiter=',',lineterminator='\n')
		writer.writerow(['MUID', 'PERM_in/hr'])

		# do things with your file	
		for line in f:
			
			lineSplit = line.split(',')
		
			row = [lineSplit[1],float(lineSplit[7])]
			writer.writerow(row)
				
		