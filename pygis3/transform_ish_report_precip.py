# -*- coding: utf-8 -*-
"""
Created on Tue Dec 01 09:50:57 2015

@author: Luis A. Morales-Marin. GIWS, 2015. (lmoralesma@gmail.com)

PURPOSE
Read an output report produced with  'read_ish.f'. The script organize the 
different kind of data saved into the report. Basically, in the report the data
is organized by block where each block belong to a specific date and time. 
To see the details about data types go to 
http://rda.ucar.edu/datasets/ds463.3/docs/ish-format-document_2011sep.pdf.

The Mandatory Data has been divided by the Scale Factor. Other type of data
(e.g. # Additional Data) must be divided by the corresponding SF. Units of data
are especified in the document aforementioned.

HOW TO RUN
To Run the script in iPython type (Windows machine):
run 'W:/Luis/Lucia/transform_ish_report.py'  W:/Luis/Lucia/726700.isd.output

To run in linux machine bach console:
python W:/Luis/Lucia/transform_ish_report.py  W:/Luis/Lucia/726700.isd.output

"""

import csv
import sys

filename = sys.argv[1]
print ' '
print 'Reading ish report: ', filename
print ' '

# Reading lines
with open(filename, "r") as f:
    lines = []
    for line in f:
        lines.append(line)
        
        
# Saving data into CSV file    
SF = {'lat':1000,'lon':1000,'spd':10,'t':10,'dp':10,'slp':10}
miss = {'lat':99999,'lon':999999,'spd':9999,'t':9999,'dp':9999,'slp':99999}
i = 0
#MAN = []
ifheader = 1
outfilename =  filename[:-11]+"_precip.csv"
print ' '
print 'Organizing and saving ish report into: ', outfilename
print ' '    
with open(outfilename, 'wb') as f:
    writer = csv.writer(f)
    while i < len(lines):
        if lines[i] == '\n':
            i = i + 2
            
        # Mandatory data section 
        MAN = []    
        splLine = lines[i].split()    
        if "MAN:" in  splLine: 
            # Header
            if ifheader:
                dummy = splLine
                del dummy[0]
                del dummy[29]
                header = dummy
                ifheader = 0
                idkeys = []
                for key in SF.keys():
                    if key in header:
                        idkeys.append(header.index(key))
                writer.writerow(header)        
                i = i + 1
            
            # Data   
            dummy = lines[i].split()
            del dummy[0]
            keys = SF.keys()
            j = 0
            for id in idkeys:
                dummy[id] = int(dummy[id])
                if dummy[id] != miss[keys[j]]:
                    dummy[id] = dummy[id]/SF[keys[j]]
                j += 1
            MAN = dummy
        i = i + 1
        
        # Additional Data Section  
        ADD = []
        splLine = lines[i].split()
        if "ADD:" in  splLine:
            i = i + 2
            splLine = lines[i].split()
            lofl = []
            while "ADD:" in  splLine:
                dummy = splLine[8:len(splLine)]
                if 'AA' in dummy[0]:
                    lofl.append(dummy)
                #print dummy
                i += 1
                splLine = lines[i].split()
            ADD = sum(lofl,[])
        #i = i + 1
        
        # Remarks Data Section
        REM = []
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
#            REM = sum(lofl,[])
        #i = i+1
        
        # Element Quality Data Section
        EQD = []
        splLine = lines[i].split()
        if "EQD:" in  splLine:
            i = i + 2
            splLine = lines[i].split()
            lofl = []
            while "EQD:" in  splLine:
                dummy = splLine[8:len(splLine)]
                lofl.append(dummy)
                #print dummy
                i += 1
                splLine = lines[i].split()
#            EQD = sum(lofl,[])
        i = i+1
        
        # Saving data into file
        #dummy = MAN + ADD + REM + EQD 
        dummy = MAN + ADD
        if dummy != []:
            writer.writerow(dummy) 
        #i += 1