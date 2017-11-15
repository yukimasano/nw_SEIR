# -*- coding: utf-8 -*-
"""
CreateDistance.py

This code creates the effective Distance Matrix based on
individuals contact data 
Output:  effective distance matrix as numpy array

@author: 
EnCt28648cf14f7c30972de440f01c53b7544e83c9ee78648cf14f7c30972de440f01puAufN5B6QB
rpWuQm1ZPfSb3bcvooZYGIwEmS

Decrypt it at https://encipher.it
"""
import numpy as np

A=np.load('day1.npy') # contact patterns day 1
B=np.load('day2.npy') # contact patterns day 2
metadata=np.loadtxt('metadata_primaryschool.txt',delimiter='\t',dtype='str')

#Aggregate over all time-slots, create initial effective distance matrix D
U=np.sum(A+B, axis=2) 
P1=(U +U.T)
P1=P1.astype(float)
g=np.sum(P1,axis=1)
P1=P1* (1./g)
D=np.ones((242,242) ,dtype=np.float)- np.log(P1)

for g in range(5):		# run 5 times to ensure convergence 
    for tp in np.argwhere(D!=np.NaN):       # iterate through all entries (tupels)
        a=np.array([[D[tp[0], tp[1]]][0]])        
        for j in np.argwhere(D[:,tp[1]]!=np.inf): # iterate through all contacts contacts          
            if j!=tp[1]:
                b=D[j,tp[1]] + D[tp[0],j]	  # create effective distance by summing
                a=np.append(a,b)
            for k in np.argwhere(D[:,j]!=np.inf)[0]: # iterate through contacts contacts contacts
                if k!=j[0] and k!=tp[1]: 
                    b=D[j,tp[1]] + D[k,j] + D[tp[0],k]
                    if b!=np.inf:
                        a=np.append(a,b)	
                    for m in np.argwhere(D[:,k]!=np.inf)[0]:
                        if m!=j[0] and m!=tp[1] and m!=k: # iterate through c c c c
                            b=D[j,tp[1]] + D[k,j] + D[m,k] +D[tp[0],m] 
                            if b!=np.inf:
                                a=np.append(a,b)
        D[tp[0],tp[1]]=np.min(a) # take the min. distance to be the effective distance
np.save('Deff.npy', D)
