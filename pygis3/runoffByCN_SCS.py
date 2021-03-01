# Estimation of the runoff volume from a precipitation volume using 
# the curve number method fro SCS.

import sys, os
sys.path.append('C:\\Users\\lmm333\\Dropbox\\Public\\pyLib')
from GdalOgrPylib import  * # Personal library
import numpy as np

# set directory
os.chdir("E:\\Documents\\NutrientsLecture2\\Maps") 

# Precipitation in inches
P = 5.0

# 10 yr return period precipitation intensity (inches/hr)
intensi = 3

# Opening the catchment shapefile
file = 'Catchment_proj.shp'
shfile, layer = openingShpFile(file)

# Read the C rational method roughness coeff.
filenameRationalMet = 'E:\\Documents\\NutrientsLecture2\\RationalMetclassification.csv'
RationalMetclassification = np.genfromtxt(filenameRationalMet, delimiter=',', dtype=None, missing_values={0:"N/A"})
nrowC = len(RationalMetclassification[:,0])

# Read the CN curve number table
filenameCNclass = 'E:\\Documents\\NutrientsLecture2\\CNclassification.csv'
CNclassification = np.genfromtxt(filenameCNclass, delimiter=',', dtype=None, missing_values={0:"N/A"})
nrow = len(CNclassification[:,0])
row2 = CNclassification[2,2:10]
nrow2 = len(row2)
minInf = [float(row2[i]) for i in range(0,nrow2,2)]
maxInf =[float(row2[j]) for j in range(1,nrow2,2)]
row0 = list(CNclassification[0,:])
typeOfSoil = make_unique(row0)
typeOfSoil = [typeOfSoil[x] for x in [2,4,5,6]]
ncol = len(CNclassification[2,:])

# Read land use table
filenameLandUse = 'landUse.csv'
landUse = np.genfromtxt(filenameLandUse, delimiter=',', dtype=None, missing_values={0:"N/A"})
ncolLandUse = len(landUse[0,:])

# Read soil infiltration table
filenameSoilInf = 'KSAT_IN_HR_ave.csv'
KSAT_IN_HR_ave = np.genfromtxt(filenameSoilInf, delimiter=',', dtype=None, missing_values={0:"N/A"})

# Calculating the Runoff volume
feature = layer.GetNextFeature()
nfeatures = len(KSAT_IN_HR_ave)-1 # -1 because of the header
#soilClassi = []
CNminlist = []
CNmaxlist = []
Cmin = list(RationalMetclassification[2:nrowC-1,2])
Cmax = list(RationalMetclassification[2:nrowC-1,3])
for i in range(0,nfeatures):

	inf = float(KSAT_IN_HR_ave[i+1,1])

	# Soil classification (A,B,C,D) based on infiltration 
	k = 0 
	for l,j in zip(minInf,maxInf):
		if inf>l and inf<=j:
			#soilClassi.append(typeOfSoil[k])
			soilClassi = typeOfSoil[k]
			break
		k+=1
		
	# Curve number CN for minInf values
	idx = row0.index(soilClassi)
	CNmin = list(CNclassification[3:nrow,idx])
	CNmax = list(CNclassification[3:nrow,idx+1])
	landUsePr = list(landUse[i+1,1:ncolLandUse])
	CNmin = int(round(sum([int(l)*float(j)/100 for l,j in zip(CNmin,landUsePr)])))
	CNmax = int(round(sum([int(l)*float(j)/100 for l,j in zip(CNmax,landUsePr)])))
	CNminlist.append(CNmin)
	CNmaxlist.append(CNmax)
	
	# Runoff volume estimation using SCS
	S = 1000/CNmin - 10
	Qmin = (P-0.2*S)**2/(P+0.8*S)
	S = 1000/CNmax - 10
	Qmax = (P-0.2*S)**2/(P+0.8*S)
	
	catch = feature.GetGeometryRef()
	areaCatch =  catch.GetArea() # in m2
	print i, Qmin, Qmax, ' inches', areaCatch, 'm3'
	
	# Runoff estimation using Rational Method
	CminAv = sum([float(l)*float(j)/100 for l,j in zip(Cmin,landUsePr)])
	CmaxAv = sum([float(l)*float(j)/100 for l,j in zip(Cmax,landUsePr)])
	Qmin = 0.000247105*areaCatch*intensi*CminAv # in cfs
	Qmax = 0.000247105*areaCatch*intensi*CmaxAv # in cfs
	
	#print i, Qmin*35.3146662127, Qmax*35.3146662127, ' m3s'
	
	
	
	# destroy the features
	feature.Destroy()
	feature = layer.GetNextFeature()

# close the data sources
shfile.Destroy()