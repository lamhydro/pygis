# -*- coding: utf-8 -*-
"""
Created on Tue Dec 01 09:50:57 2015

@author: lmm333
"""

import csv

filename = '726700.isd.output'
with open(filename, "r") as f:
    lines = []
    for line in f:
        lines.append(line)

# Control and Mandatory Data Section
SF = {'lat':1000,'lon':1000,'spd':10,'t':10,'dp':10,'slp':10}
miss = {'lat':99999,'lon':999999,'spd':9999,'t':9999,'dp':9999,'slp':99999}
i = 0
MAN = []
ifheader = 1
for line in lines:
    splLine = line.split()
    
    # Mandatory data section
    if "MANDATORY" in splLine:
        if ifheader:
            dummy = lines[i+1].split()
            del dummy[0]
            del dummy[29]
            header = dummy
            ifheader = 0
            #writer.writerow(header)
            idkeys = []
            for key in SF.keys():
                if key in header:
                    idkeys.append(header.index(key))
        #print lines[i+2]
        dummy = lines[i+2].split()
        del dummy[0]
        keys = SF.keys()
        j = 0
        for id in idkeys:
            dummy[id] = int(dummy[id])
            if dummy[id] != miss[keys[j]]:
                dummy[id] = dummy[id]/SF[keys[j]]
            j += 1
        MAN.append(dummy)
    
    print i    
    i += 1 


# Additional Data Section        
i = 0
ADD = []
while i < len(lines):
    splLine = lines[i].split()
    if "ADD:" in  splLine:
        i = i + 2
        splLine = lines[i].split()
        lofl = []
        while "ADD:" in  splLine:
            dummy = splLine[8:len(splLine)]
            lofl.append(dummy)
            #print dummy
            i += 1
            splLine = lines[i].split()
        ADD.append(sum(lofl,[]))
        
    i += 1
    
# Remarks Data Section
i = 0    
REM = []
while i < len(lines):
    splLine = lines[i].split()
    if "REM:" in  splLine:
        i = i + 1
        splLine = lines[i].split()
        lofl = []
        while "REM:" in  splLine:
            dummy = splLine[8:len(splLine)]
            lofl.append(dummy)
            #print dummy
            i += 1
            splLine = lines[i].split()
        REM.append(sum(lofl,[]))
        
    i += 1    
    
MANfilename =  filename[:-11]+"_MAN_ADD.csv"
with open(MANfilename, 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for lMAN,lADD in zip(MAN,ADD):
        dummy = lMAN + lADD
        writer.writerow(dummy) 
            