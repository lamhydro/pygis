# NOT USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import sys, os
import csv

# set directory
os.chdir("Z:\\Luis\\STATSGO\\ussoils_17.e00")

# Reading ascii file
with open('ussoils_17.e00', 'r') as f:
    # do things with your file
	
	j = 1
	lines = []
	for i,line in enumerate(f):
		if (i >= 653223-1 and i<=684725-1): # '-1' because the counter begins in 1.
			lines.append(line.strip())
			if j == 3: 
				wholeLine = ' '.join(lines)
				print wholeLine
				lines = []
				j = 0
			j +=1
		#print i
		