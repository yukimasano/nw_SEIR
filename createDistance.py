# -*- coding: utf-8 -*-
"""
CreateDistance.py

This code creates the effective Distance Matrix based on
individuals contact data 
Output:  effective distance matrix as numpy array

@author: Yuki Asano
"""
import matplotlib.pyplot as plt
import numpy as np

A=np.load('day1.npy')
B=np.load('day2.npy')
day1=np.load('times1.npy')
day2=np.load('times2.npy')
metadata=np.loadtxt('metadata_primaryschool.txt',delimiter='\t',dtype='str')

U=np.sum(A+B, axis=2) #Aggregate over all time-slots
P1=(U +U.T)
P1=P1.astype(float)
g=np.sum(P1,axis=1)
for i in np.nonzero(g)[0]:
    P1[:,i]=P1[:,i]* (1./g[i])
D=np.ones((242,242) ,dtype=np.float)- np.log(P1)
for g in range(5):
    print len(np.argwhere(D==np.inf))
   # np.save('D.2.npy', D)
    print np.max(D[D!=np.inf])
    for tp in np.argwhere(D!=np.NaN):       
        a=np.array([[D[tp[0], tp[1]]][0]])        
        for j in np.argwhere(D[:,tp[1]]!=np.inf):          
            if j!=tp[1]:
                b=D[j,tp[1]] + D[tp[0],j]
                a=np.append(a,b)
            for k in np.argwhere(D[:,j]!=np.inf)[0]:
                if k!=j[0] and k!=tp[1]:
                    b=D[j,tp[1]] + D[k,j] + D[tp[0],k] 
                    if b!=np.inf:
                        a=np.append(a,b)
                    for m in np.argwhere(D[:,k]!=np.inf)[0]:
                        if m!=j[0] and m!=tp[1] and m!=k:
                            b=D[j,tp[1]] + D[k,j] + D[m,k] +D[tp[0],m] 
                            if b!=np.inf:
                                a=np.append(a,b)
        D[tp[0],tp[1]]=np.min(a)
np.save('Deff.npy', D)
