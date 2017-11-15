# -*- coding: utf-8 -*-
"""
CreateNetworks.py

This algorithm aggregates the temporally resolved network data
default= 20min aggregation, by setting mins=1/3 we get 20sec resolution.

Output: Tensor A20 for day 1, tensor B20 for day 2 along with the the times as vectors.

@author: 
EnCt28648cf14f7c30972de440f01c53b7544e83c9ee78648cf14f7c30972de440f01puAufN5B6QB
rpWuQm1ZPfSb3bcvooZYGIwEmS

Decrypt it at https://encipher.it
"""
import numpy as np
def createnw(data,metadata,mins):
    tt=-1
    maxtime=np.ceil((data[-1,0] - data[0,0] )/(20*3*mins)) # 20min     
    numIndividuals=len(metadata[:, 0])
    startid=int(metadata[0][0])
    A= np.zeros((numchildren+1,numIndividuals+1, maxtime+1),dtype=np.int)
    told=0  
    
    for row in range(len(data[:,0])):
        t=data[row,0]
        id1=int(np.argwhere(str(data[row,1])== metadata[:,0]))
        id2=int(np.argwhere(str(data[row,2])== metadata[:,0]))
        if (t>= (told+(20*3*mins))) and t!=told: 	#start new timeslot
            tt+=1
            told=t
        if id1>id2:					#fill lower triangular
            A[id1][id2][tt]+=1
        else:
            A[id2][id1][tt]+=1
    return A, range(tt)

data=np.loadtxt('primaryschool_wo_class.csv', delimiter=',', dtype=np.int)
firstday=data[0:60623,:]
secondday=data[60623:,:]
metadata=np.loadtxt('metadata_primaryschool.txt', delimiter='\t', dtype='S16')


# create 20min aggregated data
[A20,time] =createnw(firstday,metadata,20)
[B20,time2] =createnw(secondday,metadata,20)

# save data as numpy objects
np.save('day1.npy', A)
np.save('day2.npy', B)
np.save('numbers.npy',no)
np.save('times1.npy',time)
np.save('times2.npy',time2)
