# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 15:30:41 2021

@author: nicag
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

name_folder2='ridge_result/'
name_folder3='powerseries/'
name_folder4='Divisions/'
path='C:/Users/nicag/Desktop/William_traces/'
path2=str(path)+str(name_folder2)
path3=str(path)+str(name_folder3)
path4=str(path)+str(name_folder4)

file_list=['untreated','0uM','5uM','10uM']
file_list2=['low','medium','high']

#fig=plt.figure() 
channel1='circadian'
channel2='cell_cycle'
magn1='frequent_dividers_'
magn2='sporadic_dividers_'
magn=magn2
for i in range(3):
    nom=file_list[0]
    nom2=file_list2[i]
    
    file1=str(magn)+str(nom2)+'_'+str(channel1) #nom or nom2
    file2=str(magn)+str(nom2)+'_'+str(channel2)
    data1 = pd.read_excel(path4+file1+r'.xlsx')
    data2 = pd.read_excel(path4+file2+r'.xlsx')
    
    ro1=str(nom2)+'_density_'+str(nom)+'_'+str(channel1)
    ro2=str(nom2)+'_density_'+str(nom)+'_'+str(channel2)
    ro_res1 = pd.read_csv(path2+ro1+r'.csv')
    ro_res2 = pd.read_csv(path2+ro2+r'.csv')
               
    list_freq=data1.columns
    
    ro_freq_circadian=pd.DataFrame(columns=ro_res1.columns,index=ro_res1.index)    
    ro_freq_cellcycle=pd.DataFrame(columns=ro_res2.columns,index=ro_res2.index)    
    
    for i in range(len(ro_res1.iloc[:,[0]])):
        if (ro_res1['traceId'][i]) in list_freq:
            ro_freq_circadian.iloc[i]=ro_res1.iloc[i]
            ro_freq_cellcycle.iloc[i]=ro_res2.iloc[i]
    
    ro_freq_circadian.dropna(inplace=True)
    ro_freq_circadian.to_csv(path2+str(magn)+'ro_'+str(nom2)+'_'+str(channel1)+'.csv')
    
    ro_freq_cellcycle.dropna(inplace=True)
    ro_freq_cellcycle.to_csv(path2+str(magn)+'ro_'+str(nom2)+'_'+str(channel2)+'.csv')

            
            
            
            
            
            
            