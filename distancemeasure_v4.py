# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 21:36:19 2015

@author: yuki

here: gamma=4, mu=2, beta=2
recalc=1 um neu die distanzmatrizen zu berechnen
sim=1 for simulating an outbreak
spars=1 for getting picture of distance matrices


"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
A=np.load('day1.npy')
B=np.load('day2.npy')
no=np.load('numbers.npy')
day1=np.load('times1.npy')
day2=np.load('times2.npy')
metadata=np.loadtxt('metadata_primaryschool.txt',delimiter='\t',dtype='str')

U=np.sum(A+B, axis=2)
P1=(U +U.T)
P1=P1.astype(float)
g=np.sum(P1,axis=1)
for i in np.nonzero(g)[0]:
    P1[:,i]=P1[:,i]* (1./g[i])
recalc=0
if recalc==1:
    D=np.ones((243,243) ,dtype=np.float)*1./(P1)
    D[D==np.inf]=0.0
    mx= np.max(D)
    X=np.zeros((243,243) ,dtype=np.float)
    np.save('D.2.npy', D)
    for tp in np.argwhere(D==0):
        a=[]
        for j in np.nonzero(D[:,tp[1]])[0]:
            if D[tp[0],j]!=0:
                b=D[tp[0],j] + D[j,tp[1]]
                a.append(b)
        if len(a)!=0:
            X[tp[0],tp[1]]=np.min(a)
    np.save('D2.2.npy', D+X)
    
    D=np.ones((243,243) ,dtype=np.float)-np.log(P1)
    D[D==np.inf]=0.0
    mx= np.max(D)
    recalc=1    
    np.save('D.npy', D)
    X=np.zeros((243,243) ,dtype=np.float)
    for tp in np.argwhere(D==0):
        a=[]
        for j in np.nonzero(D[:,tp[1]])[0]:
            if D[tp[0],j]!=0:
                b=D[tp[0],j] + D[j,tp[1]]
                a.append(b)
        if len(a)!=0:
            X[tp[0],tp[1]]=np.min(a)
    np.save('D2.npy', D+X)

spars=1
D=np.load('D.2.npy')
D2=np.load('D2.2.npy')
D0=np.load('D.npy')
D02=np.load('D2.npy')
     
if spars==1:    
    
    x    = range(242)
    y    = range(242)
    x, y = np.meshgrid(x, y)
    
    x    = range(242,-1,-1)
    y    = range(243)
    x, y = np.meshgrid(x, y)
    
    fig=plt.figure(figsize=(7, 7))
    plt.rcParams.update({'font.size': 9})
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.subplot(2,2,2)
    z=D0
    plt.spy(z,origin='lower')
    frame1=plt.gca()
    frame1.axes.get_xaxis().set_ticks([])
    frame1.axes.get_yaxis().set_ticks([])
    plt.title('Sparsity pattern of first order contacts')
    plt.subplot(2,2,1)
    z[z==0]=1.1*np.max(z)
    plt.pcolormesh(x, y, np.rot90(z),clim=(243,243))
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.title('First order distances (inf dist=%s)'%np.round(np.max(z),1))
    plt.xlim(xmax=243) #or xl
    plt.ylim(ymax=243) #or yl
    
    plt.subplot(2,2,4)
    z=D02
    plt.spy(z,origin='lower')
    frame1=plt.gca()
    frame1.axes.get_xaxis().set_ticks([])
    frame1.axes.get_yaxis().set_ticks([])
    plt.title('Sparsity pattern of second order contacts')
    plt.subplot(2,2,3)
    z[z==0]=1.1*np.max(z)
    plt.pcolormesh(x,y,np.rot90(z), clim=(243,243))
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.title('Second order distances (inf dist=%s)'%np.round(np.max(z),1))
    plt.xlim(xmax=243) #or xl
    plt.ylim(ymax=243) #or yl
    plt.show()  
    plt.subplots_adjust(hspace=0.6)
    plt.suptitle('Effective distances (1-log(P_{mn}))',fontsize=14)     
    fig.savefig('effDistMatricesD0.png', dpi=500) 


sim=0
if sim==1:
            
    no=no+1
    def transmit(A_at_t,s,ias,isy,home,arrival):
        r=np.nonzero(A_at_t)[0]
        for i in r:
            if (ias[i]!=0 or isy[i]!=0)and home[i]<=0 and homecl[i]<=0:
                c=np.nonzero(A_at_t)[1]
                for j in c:
                    if ias[j]==0 and isy[j]==0 and (home[j]<=0 and rec[j]==0 and ex[j]==0 and homecl[j]<=0):
                        rtemp=np.random.random()
                        if ias[i]==0:
                            bina=rtemp > (1-beta)**( A_at_t[i,j]*(isy[i]!=0) )
                        else:
                            bina=rtemp > (1-beta)**( A_at_t[i,j]*(ias[i]!=0) )
                        if bina==1:
                           # print 'pupil w/ ID', j, 'got exposed'
                            ex[j]=1*(np.random.normal()*mu*0.1 + mu)
                            arrival[i,batchno]=tt
                            s[j]=0   #remove
                           
        
    def eod(grades,tt,isy,home,rec):            
        new=np.setdiff1d(np.nonzero(isy)[0],np.nonzero(home)[0])
        home[new]=isy[new]
        
    def timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s):
        #spontaneous infection of susceptibles
        spontexpo(s,ex)
        
        #those without symptoms
        ias[np.nonzero(ias)[0]]-=1.00000001
        isy[np.nonzero(isy)[0]]-=1.00000001
        #those at home
        home[np.nonzero(home)[0]]-= 1.00000001
        homecl[np.nonzero(homecl)[0]]-= 1.00000001
        
        rec[ias<0]=1
        rec[isy<0]=1
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
                    grade=5     #teacher
                gradesPrev[grade,tt:slots,batchno]=gradesPrev[grade,tt,batchno]-1
        ias[ias<0]=0
        isy[isy<0]=0    
        
        
    
        #those exposed
        ex[np.nonzero(ex)[0]]-=1.00000001
        for i in np.argwhere(ex<0):
            
            ran=np.random.random()
            ias[i]=(ran<pa)* (np.random.normal()*gamma*0.1 + gamma)
            isy[i]=(ran>pa)*(np.random.normal()*gamma*0.1 + gamma)
            ex[i]=0
            #note: my matrix A and ias, isy are already sorted 
            try:
                grade=metadata[i, 1].astype('S1').astype('i1')[0]  -1
                grades[grade,tt:slots]=grades[grade,tt]+1
                gradesPrev[grade,tt:slots,batchno]=gradesPrev[grade,tt,batchno]+1
            except:
                gradesPrev[5,tt:slots,batchno]=gradesPrev[5,tt,batchno]+1   
        
    def targetedClosure(tt,gradesPrev,ias,isy,home,homecl,s,dates):
        grademax=np.argmax(gradesPrev[:,tt,batchno]) 
        if gradesPrev[grademax,tt,batchno] > threshhold and previousgrade[grademax]==0:
            dates.append(tt/72.0)
            previousgrade[grademax]=1
            #gradesPrev[grademax,tt:slots]=05
            for i in range(243):
                try:
                    grade=metadata[i, 1].astype('S1').astype('i1') -1
                except:
                    pass  ## teachers still go to school
                if grade==grademax:
                    #s[i]=0; ias[i]=0; isy[i]=0; ex[i]=0
                    homecl[i]=clPeriod  
    
        
    def spontexpo(s,ex):
    	#spontinfec accounts for the spontaenous exposure
        new= np.random.rand(len(np.argwhere(s==1))) < beta_spon
      #  if max(new)!=0:
      #      print 'spont infection of', np.argwhere(s==1)[new]
        ex[np.argwhere(s==1)[new]]=1*(np.random.normal()*gamma*0.1 + gamma)    
        s[np.argwhere(s==1)[new]]=0
        
        
    if __name__ == "__main__":
        for batchno in range(1):
            home=np.zeros((no),dtype=np.float)
            homecl=np.zeros((no),dtype=np.float)
            s=np.ones((no),dtype=np.int)
            ias=np.zeros((no),dtype=np.float)
            isy=np.zeros((no),dtype=np.float)
            ex=np.zeros((no),dtype=np.float)
            rec=np.zeros((no),dtype=np.int)
            maxdays=30; tt=0; 
            threshhold=2; clPeriod=24*3*5;
            previousgrade= np.zeros(5,dtype=np.int)
            slots=24*3*maxdays +1
            s_time= np.zeros(slots,dtype=np.int)
            ias_time= np.zeros(slots,dtype=np.int)
            isy_time= np.zeros(slots,dtype=np.int)
            rec_time= np.zeros(slots,dtype=np.int)
            ex_time= np.zeros(slots,dtype=np.int)
            grades=np.zeros((6,slots),dtype=np.int)
            gradesPrev=np.zeros((6,slots,1),dtype=np.int)
            gamma=24*3*4
            mu=24*3*2
            beta=2*10**-3 ; beta_spon=6*10**-8
            pa=0.3 
            dates=[]
            arrival=np.zeros((243,1))
            tinder=np.random.randint(no, size=1)
            isy[tinder]=1*(np.random.normal()*gamma*0.1 + gamma)
            s[tinder]=0
            print tinder
            #initial
            try:
                grade=metadata[tinder, 1].astype('S1').astype('i1')  -1  
            except:
                grade=5 #teacher       
            grades[grade,tt:slots]=grades[grade,tt]+1
            gradesPrev[grade,tt:slots]=gradesPrev[grade,tt]+1   
            while tt<maxdays*24*3:
                if not any(gradesPrev[:,tt]) and all(ex==0):
                    break
                else:
                    if np.mod(tt+24*3*2,24*3*7)==0:    #weekend 
                        for t in range (72+72):
                            timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                       #     svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                            tt+=1 
                        eod(grades, tt,isy,home,rec)
                    for t in day1:
                        transmit(A[:,:,t],s, ias,isy,home,arrival)
                        timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                       # targetedClosure(tt,gradesPrev,ias,isy,home,homecl,s,dates)
                      #  svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                        tt+=1                     
                    for t in range (72-25):
                        timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                       # svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                        tt+=1
                    eod(grades,tt,isy,home,rec)
                    if np.mod(tt+24*3*2,24*3*7)==0:    #weekend 
                        for t in range (72+72):
                            timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                        #    svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                            tt+=1 
                        eod(grades,tt,isy,home,rec)
                    for t in day2:
                        transmit(B[:,:,t],s, ias,isy,home,arrival)
                        timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                        #targetedClosure(tt,gradesPrev,ias,isy,home,homecl,s,dates)
                       # svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                        tt+=1       
                    for t in range (72-25):
                        timepass(grades,gradesPrev,tt,ias,rec,ex,isy,home,s)
                       # svinfo(tt,s_time, ias_time, isy_time, rec_time,ex_time, s,ias,isy,rec,ex)
                        tt+=1
                    eod(grades,tt,isy,home,rec)
            #############################################################
            if np.max(np.sum(gradesPrev[:,:,batchno], axis=0))<20:
                gradesPrev[:,tt,batchno]=0
                arrival[:,batchno]=0

    '''
       # plt.plot(np.arange(slots)/72., np.sum(gradesPrev, axis=0) ,linewidth=0.5)  
        plt.plot(np.arange(slots)/72., np.median(infecs.T[a],axis=0) ,linewidth=1, color='k') 
        plt.plot(np.arange(slots)/72., infecs.T[a].T,linewidth=0.3,alpha=0.2)
        
        plt.title(r'$\mbox{Prevalence by grade; %s simulations, %s with AR\textgreater0.1}$'%(maxbatch, maxbatch-noplot))
        plt.xlabel('time (days)')
        plt.ylabel('Prevalence')
        plt.legend(['median'])
        
        fig.savefig('%sgc_median_Infecs.png'%maxbatch, bbox_inches='tight')
        plt.show()
    
        #print sum(home!=0) + sum(rec!=0) + sum(s!=0) +sum(isy!=0) +sum(ias!=0) +sum(ex!=0)
    ''' 
    plt.close()   
    fig=plt.figure()
    plt.rcParams.update({'font.size': 10})
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    y=arrival.T[0][arrival.T[0]!=0]/72.
    plt.suptitle('Comparison of effective distance measures for disease arrival time',fontsize=14)
    plt.subplot(2,2,1)  
    plt.title(r'$\mbox{First order distances (P^{-1}_{mn})}$')
    x=D[tinder][0][arrival.T[0]!=0]
    plt.scatter(x[x!=0], y[x!=0],marker='x',c='darkblue')    
    fit =np.polyfit(x[x!=0], y[x!=0],1)
    _, _, r_value, _, std_err = stats.linregress(x[x!=0], y[x!=0])
    z = np.poly1d(fit)
    plt.plot(x,z(x),'k-', linewidth=1)
    plt.legend(['Data',r'$\mbox{y=ax+b, } R^2 = %s$'%(np.round(r_value,2))],loc=2,fontsize=8)
    plt.ylabel('Exposure date')
    #plt.xlabel('Effective distance')
    
    
    plt.subplot(2,2,3) 
    plt.title(r'$\mbox{Second order distances (P^{-1}_{mn})}$')
    x=D2[tinder][0][arrival.T[0]!=0]
    plt.scatter(x, y,marker='x',c='darkblue')   
    fit=np.polyfit(x[x!=0], y[x!=0],1)
    _, _, r_value, _, std_err = stats.linregress(x, y)
    z = np.poly1d(fit)
    plt.plot(x,z(x),'k-', linewidth=1)  
    plt.legend(['Data',r'$\mbox{y=ax+b, } R^2 = %s$'%(np.round(r_value,2))],loc=2,fontsize=8)
    plt.ylabel('Exposure date')
    plt.xlabel('Effective distance')
    plt.subplots_adjust(hspace=0.6)
    
    plt.subplot(2,2,2)  
    plt.title(r'$\mbox{First order distances (1-log(P_{mn}))}$')
    x=D0[tinder][0][arrival.T[0]!=0]
    plt.scatter(x[x!=0], y[x!=0],marker='x',c='darkblue')    
    fit =np.polyfit(x[x!=0], y[x!=0],1)
    _, _, r_value, _, std_err = stats.linregress(x[x!=0], y[x!=0])
    z = np.poly1d(fit)
    plt.plot(x,z(x),'k-', linewidth=1)
    plt.legend(['Data',r'$\mbox{y=ax+b, } R^2 = %s$'%(np.round(r_value,2))],loc=2,fontsize=8)
    #plt.ylabel('Exposure date')
    #plt.xlabel('Effective distance')
    
    
    plt.subplot(2,2,4) 
    plt.title(r'$\mbox{Second order distances (1-log(P_{mn}))}$')
    x=D02[tinder][0][arrival.T[0]!=0]
    plt.scatter(x, y,marker='x',c='darkblue')   
    fit=np.polyfit(x[x!=0], y[x!=0],1)
    _, _, r_value, _, std_err = stats.linregress(x, y)
    z = np.poly1d(fit)
    plt.plot(x,z(x),'k-', linewidth=1)  
    plt.legend(['Data',r'$\mbox{y=ax+b, } R^2 = %s$'%(np.round(r_value,2))],loc=2,fontsize=8)
    #plt.ylabel('Exposure date')
    plt.xlabel('Effective distance')
    plt.subplots_adjust(hspace=0.6)
    
    fig.savefig('effDistCompare2_%s.png'%(tinder), dpi=500) 