def accumuThrouhtNetwork(HydroID,HydroIDS,NextDownID,Att, accVar):
	rows = [j for j, x in enumerate(NextDownID) if x == HydroID]
	dummy = []
	for row in rows:
		dummy.append(Att[row])
	
	#deraccVar=sum(dummy)
	accVar +=sum(dummy)

	for row in rows:
		HydroID=HydroIDS[row]
		#print 'here',row,HydroID
		accVar+=accumuThrouhtNetwork(HydroID,HydroIDS,NextDownID,Att, 0)
		
	return accVar


#HydroIDS=range(1,16)
HydroIDS=[12,4,20,1000,15,1,1100,14000,5000,60,130,7,300,8000,900]
#NextDownID=[-1, 1,2,2,4,4,1,7,7,1,10,10,10,13,13]
NextDownID=[1,20,1000,-1,130,1000,1,130,4,4,1,1000,20,7,7]
Att=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5] #[(x**2)/0.5 for x in range(15)]
			
i = 0
accumVar = []			
for HydroID in HydroIDS:
	rows = [j for j, x in enumerate(NextDownID) if x == HydroID]
	#print len(rows)
	if len(rows)== 0:
		print HydroID, Att[i]
	else:
	#indices1 = [j for j, x in enumerate(NextDownID) if x == HydroID]
	#print indices1
		accVar = 0
		print HydroID, accumuThrouhtNetwork(HydroID,HydroIDS,NextDownID,Att, Att[i])
	#print accumVar[i]
	i+=1
	#if i==1: break