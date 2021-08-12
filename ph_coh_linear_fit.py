# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 10:16:56 2021

@author: nicag
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import math

plt.rcParams.update({'font.size': 16})

name_folder='Phase_coherence_fit/'
path='C:/Users/nicag/Desktop/TNBC/Single_cell_data_Anna/' 
path2=str(path)+str(name_folder)
path3='C:/Users/nicag/Desktop/William_traces/Phase_coherence/'

colors_list=['red','orange','lime','purple']

df=pd.read_excel(path3+'Phase_coherence_inhibitor.xlsx') #Importing the file containing the phase coherence for all conditions
file_list=df.columns[df.columns != 'Unnamed: 0']
fig=plt.figure() 
print(file_list)

for i in range(4): #For densities: 0-3, for inhibitor concentration 3-6
    
    #Starting point of fitting
    if i==0:
        delta=50
        delta2=35
    elif i==1:
        delta=50
        delta2=35
    elif i==2:
        delta=45
        delta2=100
    elif i==3:
        delta=15
        delta2=140
            
    #Defining the linear function with two parameters
    def linear(m,x):
        data=pd.read_excel(path3+'Phase_coherence_inhibitor.xlsx')
        a=data.iloc[delta][i+1] #Initial point of the phase coherence
        return a+m*x

    name=file_list[i]
    time=df.index.values*0.5
    phases=df.iloc[:,[i+1]]
    time_vect=[]
    ph_coh=[]
    #Choosing only the necessary values of the phase coherence (starting from the maximum point)
    for j in range(len(time)-delta-delta2):
        time_vect.append(time[j])
        ph_coh.append(df.iloc[j+delta][i+1])

    time_vect=np.reshape(time_vect,len(time_vect))
    ph_coh=np.reshape(ph_coh,len(ph_coh))
    a=df.iloc[delta][i+1]

    popt,pcov=curve_fit(linear,time_vect,ph_coh)
    
    print(name, popt, np.sqrt(pcov))
    
    dist = int(math.log10(abs(np.sqrt(pcov))))
    dist=int(np.abs(dist)+1)
    slope=np.round(popt[0],dist)
    error=np.round(np.sqrt(pcov[0]),dist)
    print(slope,error[0])
    
    if i!=1:
        plt.plot(time,phases, color=colors_list[i])
        plt.plot(time_vect+delta/2,ph_coh,label=str(name)+'100%'+' slope:'+str(slope)+'$\pm$' +str(error[0]),color=colors_list[i])
    #    plt.plot(time_vect+delta/2,a*np.exp(-(time_vect)*popt[0]),'--',color=colors_list[col-1])
    #    plt.plot(time_vect+delta/2,exp(popt[0],time_vect),'--',color=colors_list[col-1])
        plt.plot(time_vect+delta/2,linear(popt,time_vect),'--',color=colors_list[i])


plt.xlabel('Time(h)')
plt.ylabel('Phase coherence')
#plt.ylim([0,0.6])
fig.set_figheight(10)
fig.set_figwidth(12)
plt.legend(loc='best')
plt.show()