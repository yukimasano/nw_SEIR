# -*- coding: utf-8 -*-
"""
This code simulates an outbreak based on the 20min aggregated data
given by CreateNetworks.py
Data is stored in time-series and split by grades.
Various outputs possible 
(exposure date vs effective distance, SEIR classes vs time, etc.)

@author: Yuki Asano
"""


import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

D=np.load('D.npy')
Deff1=D[0:242,0:242]
Deff2=np.load('Deff.npy')
no=np.load('numbers.npy')
day1=np.load('times1.npy')
day2=np.load('times2.npy')
metadata=np.loadtxt('metadata_primaryschool.txt',delimiter='\t',dtype='str')
A=np.load('day1.npy')
B=np.load('day2.npy')

def transmit(A_at_t,s,ias,isy,home):
    for ij in np.argwhere(A_at_t!=0):
        i=ij[0]
        j=ij[1]
        infectious1= (ias[i]!=0 or isy[i]!=0)and home[i]<=0 and homecl[i]<=0 
        sus1= (s[i]==1 and homecl[i]<=0 )
        infectious2=(ias[j]!=0 or isy[j]!=0)and home[j]<=0 and homecl[j]<=0 
        sus2= (s[j]==1 and homecl[j]<=0)
        if (infectious1 and sus2):                
            rtemp=np.random.random()
            if isy[i]!=0:
                bina=rtemp > (1-beta)**A_at_t[i,j]
            else:
                bina=rtemp > (1-beta/2.)**A_at_t[i,j]
            if bina==1:
               # print 'pupil w/ ID', j, 'got exposed'
                ex[j]=1*(np.random.normal()*mu*0.1 + mu)
                arrival[j]=tt
                s[j]=0   #now at exposed 
        if (infectious2 and sus1):
            rtemp=np.random.random()
            if isy[j]!=0:
                bina=rtemp > (1-beta)**A_at_t[i,j]
            else:
                bina=rtemp > (1-beta/2.)**A_at_t[i,j]
            if bina==1:
               # print 'pupil w/ ID', j, 'got exposed'
                ex[i]=1*(np.random.normal()*mu*0.1 + mu)
                arrival[i]=tt
                print tt/72.
                s[i]=0   #now at exposed
    
def eod(grades,tt,isy,home,rec):            
    new=np.setdiff1d(np.nonzero(isy)[0],np.nonzero(home)[0])
    home[new]=isy[new]
    
def timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s):
    #spontaneous infection of susceptibles
    spontexpo(s,ex)
    
    #those infected: time passes
    ias[np.nonzero(ias)[0]]-=1.00000001
    isy[np.nonzero(isy)[0]]-=1.00000001
    #those at home: time passes
    home[np.nonzero(home)[0]]-= 1.00000001
    homecl[np.nonzero(homecl)[0]]-= 1.00000001
    
    # after recovery period they recover:
    rec[ias<0]=1
    rec[isy<0]=1
    # save this recovery to the prevalence time-series
    if any(isy<0):
        for i in np.where(isy<0)[0]:
            try:
                grade=metadata[i, 1].astype('S1').astype('i1')  -1  
            except:
                grade=5 #teacher
            gradesPrev[grade,tt:slots,batchno]=gradesPrev[grade,tt,batchno]-1        
    if any(ias<0): 
        for i in np.where(ias<0)[0]:
            try:
                grade=metadata[i, 1].astype('S1').astype('i1')  -1
            except:
                grade=5  #teacher
            gradesPrev[grade,tt:slots,batchno]=gradesPrev[grade,tt,batchno]-1
    ias[ias<0]=0
    isy[isy<0]=0    
    #those exposed: pass time
    ex[np.nonzero(ex)[0]]-=1.00000001
    # after exposure: disease develops: either with or without symptoms
    for i in np.argwhere(ex<0):
        ran=np.random.random()
        ias[i]=(ran<pa)* (np.random.normal()*gamma*0.1 + gamma)
        isy[i]=(ran>pa)*(np.random.normal()*gamma*0.1 + gamma)
        ex[i]=0
        #note: matrix A and ias, isy are already sorted
        # again, save this to prevalence time-series:
        try:
            grade=metadata[i, 1].astype('S1').astype('i1')[0]  -1
            grades[grade,tt:slots]=grades[grade,tt]+1
            gradesPrev[grade,tt:slots,batchno]=gradesPrev[grade,tt,batchno]+1
        except:
            # teacher
            gradesPrev[5,tt:slots,batchno]=gradesPrev[5,tt,batchno]+1   
    
def targetedClosure(tt,gradesPrev,ias,isy,home,homecl,s,dates):       
    grademax=np.argmax(gradesPrev[:,tt,batchno]) 
    cond1=(grademax!=5) and previousgrade[grademax]==0
    if gradesPrev[grademax,tt,batchno] > threshhold and cond1:
        dates.append(tt/72.0)
        previousgrade[grademax]=1
        for i in range(243):
            try:
                grade=metadata[i, 1].astype('S1').astype('i1') -1
            except:
                pass  ## teachers still go to school
            if grade==grademax:
                #s[i]=0; ias[i]=0; isy[i]=0; ex[i]=0
                homecl[i]=clPeriod  

def svinfo(t,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex):
	## svinfo saves the current states 
    s_time[t]=(sum(s!=0))
    ias_time[t]=(sum(ias!=0))
    isy_time[t]=(sum(isy!=0))
    rec_time[t]=(sum(rec!=0))
    ex_time[t]=(sum(ex!=0))
     
def spontexpo(s,ex):
	#spontinfec accounts for the spontaenous exposure
    new= np.random.rand(len(np.argwhere(s==1))) < beta_spon
    ex[np.argwhere(s==1)[new]]=1*(np.random.normal()*gamma*0.1 + gamma)    
    s[np.argwhere(s==1)[new]]=0
    
if __name__ == "__main__":
    fig=plt.figure()
    plt.rcParams.update({'font.size': 12})
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    maxbatch=30 # how many simulations should be carried out
    maxdays=50;  noplot=0
    threshhold=3; clPeriod=24*3*4;
    slots=24*3*maxdays +25*3*np.ceil(maxdays/7.)
    epd=[] # saves the simulations with AR>10%
    gradesPrev=np.zeros((6,slots,maxbatch),dtype=np.int)
    for batchno in range(maxbatch):
        s_time= np.zeros(slots,dtype=np.int)    #susceptible, time series
        ias_time= np.zeros(slots,dtype=np.int)  #asymtomatic, time series
        isy_time= np.zeros(slots,dtype=np.int)  #symptomatic, time series
        rec_time= np.zeros(slots,dtype=np.int)  #recovered, time series
        ex_time= np.zeros(slots,dtype=np.int)   #exposed, time series
        home=np.zeros((no),dtype=np.float)	#at home due to discovery
        homecl=np.zeros((no),dtype=np.float)	#at home due to closure
        s=np.ones((no),dtype=np.int)		#susceptible
        ias=np.zeros((no),dtype=np.float)	#asymtomatic
        isy=np.zeros((no),dtype=np.float)	#symtomatic
        ex=np.zeros((no),dtype=np.float)	#exposed
        rec=np.zeros((no),dtype=np.int)		#recovered
        previousgrade= np.zeros(5,dtype=np.int) #saves grades already closed
        arrival=np.zeros(242)			#saves exposure date for all
        tt=0;					#time
        grades=np.zeros((6,slots),dtype=np.int) #cum. Incidence by grade

        #SEIR parameters#####################################
        gamma=24*3*4.
        mu=24*3*2.
        beta=20*3.5* 10**-4 ; beta_spon=20*2.8* 10**-9
        pa=0.3 
	#####################################################
        dates=[] 				#dates of class closure   
        tinder=np.random.randint(no, size=1)    #initially infected
        isy[tinder]=1*(np.random.normal()*gamma*0.1 + gamma)
        s[tinder]=0
        # save this initially infected to gradesPrev time-series
        try:
            grade=metadata[tinder, 1].astype('S1').astype('i1')  -1  
        except:
            grade=5 #teacher       
        gradesPrev[grade,tt:slots,batchno]=gradesPrev[grade,tt,batchno]+1  
        
        while (tt<maxdays*24*3): #main time-loop
            if not any(gradesPrev[:,tt,batchno]) and all(ex==0):
                #no one sick and no one exposed
                break
            else:
                if np.mod(tt+24*3*2,24*3*7)==0:    #weekend 
                    for t in range (72+72):
                        timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                        svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                        tt+=1
                    eod(grades,tt,isy,home,rec)
                for t in day1:
                    transmit(A[:,:,t],s, ias,isy,home)
                    timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                  # targetedClosure(tt,gradesPrev,ias,isy,home,homecl,s,dates)
                    svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                    tt+=1                     
                for t in range (72-25): #A has 25 20min slots
                    timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                    svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                    tt+=1
                eod(grades,tt,isy,home,rec)
                if np.mod(tt+24*3*4,24*3*7)==0:    #wednesday
                    for t in range (72):
                        timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                        svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                        tt+=1
                    eod(grades,tt,isy,home,rec)
                if np.mod(tt+24*3*2,24*3*7)==0:    #weekend 
                    for t in range (72+72): 
                        timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                        svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                        tt+=1 
                    eod(grades,tt,isy,home,rec)
                for t in day2:
                    transmit(B[:,:,t],s, ias,isy,home)
                    timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                 #  targetedClosure(tt,gradesPrev,ias,isy,home,homecl,s,dates)
                    svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                    tt+=1       
                for t in range (72-25): #B has 25 20min slots
                    timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                    svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                    tt+=1
                eod(grades,tt,isy,home,rec)
                if np.mod(tt+24*3*4,24*3*7)==0:    #wednesday
                    for t in range (72):
                        timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                        svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                        tt+=1
                    eod(grades,tt,isy,home,rec)
        #graphics
        numInfec=np.sum(gradesPrev[:,:,batchno], axis=0)  #Aggregate over all classes  
        try: 
            plt.close('all')   
            fig=plt.figure(figsize=(10, 5))
            plt.rcParams.update({'font.size': 12})
            plt.rc('text', usetex=True)
            plt.rc('font', family='serif')           
            plt.suptitle('Disease arrival time as a function of effective distance',fontsize=15) 
            plt.subplot(1,2,1) 
            plt.title(r'$\mbox{First order distances$')
            Deff1[np.argwhere(Deff1==np.max(Deff1))]=0.
            x=Deff1[arrival!=0, tinder]
            y=arrival[arrival!=0]/72.
            plt.scatter(x[x!=0], y[x!=0],marker='x',c='darkblue')   
            fit=np.polyfit(x[x!=0], y[x!=0],1)
            sl, _, r_value, _, std_err = stats.linregress(x[x!=0], y[x!=0])
            z = np.poly1d(fit)
            plt.plot(x,z(x),'k-', linewidth=1)  
            plt.legend(['Data',r'$\mbox{linear fit: } R^2 = %s$'%(np.round(r_value,2))],loc=2,fontsize=12)
            plt.ylabel('Exposure date (day)')
            plt.xlabel('Effective distance')
            plt.xlim(xmin=0)
            plt.ylim(ymin=0)
            plt.subplots_adjust(hspace=0.6)
            
            plt.subplot(1,2,2)  
            plt.title(r'$\mbox{Up to third order distances}$')
            x=Deff2[arrival!=0,tinder]
            plt.scatter(x[x!=0], y[x!=0],marker='x',c='darkblue')    
            fit =np.polyfit(x[x!=0], y[x!=0],1)
            sl, _, r_value, _, std_err = stats.linregress(x[x!=0], y[x!=0])
            z = np.poly1d(fit)
            plt.plot(x,z(x),'k-', linewidth=1)
            plt.xlim(xmin=0)
            plt.ylim(ymin=0)
            plt.legend(['Data',r'$\mbox{linear fit: } R^2 = %s$'%(np.round(r_value,2))],loc=2,fontsize=12)
               # plt.ylabel('Exposure date')
            plt.xlabel('Effective distance')
            if r_value>0.6:
                fig.savefig('effDistCompareDeff_%s.png'%(tinder), dpi=200) 
                print tinder, 'good'
            else:
                print 'bad', tinder
        except:
            pass