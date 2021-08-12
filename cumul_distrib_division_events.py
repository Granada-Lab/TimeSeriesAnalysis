# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 11:03:36 2021

@author: nicag
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pyboat import WAnalyzer
from pyboat import ensemble_measures as em
from pyboat import plotting as pl 
from mpl_toolkits.axes_grid1 import make_axes_locatable
import random

plt.rcParams.update({'font.size': 18})

#name_folder='Phase_coherence/'
name_folder='ridge_result/'
name_folder2='powerseries/'
name_folder3='Divisions/'
path='C:/Users/nicag/Desktop/William_traces/'
path2=str(path)+str(name_folder)
path3=str(path)+str(name_folder2)
path4=str(path)+str(name_folder3)

channel1='cell_cycle'
channel2='circadian'

channel1='cell_cycle'
channel2='circadian'
file_list=['untreated','0uM','5uM','10uM']
file_list2=['low','medium','high']
magn1='frequent_dividers_'
magn2='sporadic_dividers_'
colors_list=['blue','green','red','orange','lime','purple']
magn=magn2

fig=plt.figure()        

for i in range(4):
    nom=file_list[i]
    nom2=file_list2[0]
    file1='divisions_'+str(nom2)+'_'+str(nom)
    print(file1)
    
    divisions_matrix=pd.read_excel(path4+file1+r'.xlsx')
    time=np.arange(0,225*0.5,step=0.5)
    
    num_Ids=divisions_matrix.columns
    time_points=len(divisions_matrix.index.values)
    division_profile=np.zeros((len(num_Ids),time_points))
    
    for j in range(len(num_Ids)):
        vect=[]
        for k in range(time_points):
            vect.append(divisions_matrix.iloc[k,j])
        division_profile[j,:]=vect
    
    distr=[]
    for j in range(2,len(divisions_matrix)):
        distr.append(sum(division_profile[1:len(divisions_matrix),j]))
    
    plt.plot(time,np.cumsum(distr)/max(np.cumsum(distr)),label=str(nom)+' '+str(nom2),color=colors_list[i])

plt.xlabel('Time(h)')
plt.ylabel('Cumulative distribution of division events')
fig.set_figheight(10)
fig.set_figwidth(13)
plt.legend(loc='best')
plt.show()
    