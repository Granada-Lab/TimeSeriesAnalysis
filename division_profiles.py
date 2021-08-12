# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 12:28:49 2021

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

for ii in file_list:
#    nom=file_list[ii]
    nom2=file_list2[2]
    file=magn+str(ii)+'_'+str(channel1)
    file=str(nom2)+'_density_'+str(ii)+'_'+str(channel1)
    file1='divisions_'+str(nom2)+'_'+str(ii)
    
#    data = pd.read_excel(path4+file+r'.xlsx')
    data = pd.read_csv(path+file+r'.csv')
    time=data.index.values*0.5
    divisions_matrix=pd.read_excel(path4+file1+r'.xlsx')
    
    power_series=pd.read_csv(path3+file+r'_powerseries.csv')
    select_index=power_series.loc[power_series['0']>10]['index']
    divisions_matrix=divisions_matrix.loc[:,divisions_matrix.columns.isin(select_index)]
    
#    #Randomly select some traces
#    random_num=random.sample(set(divisions_matrix.columns),600)
#    divisions_matrix=divisions_matrix.loc[:,divisions_matrix.columns.isin(random_num)]
    
    num_Ids=divisions_matrix.columns
    time_points=len(divisions_matrix.index.values)  #Can be changed in order to see a smaller part of the experiment
    print(len(num_Ids))
    
    division_profile=np.zeros((len(num_Ids),time_points))

    ID=[]
    num_divisions=[]
    time_1st=[]
    for col in num_Ids:
        num_divisions.append(sum(divisions_matrix[col]))
        ID.append(col)
        count=0
        for i in range(len(divisions_matrix[col])):
            if sum(divisions_matrix[col])==0 and count<1:
                count+=1
                time_1st.append(0)
            elif sum(divisions_matrix[col])!=0:
                if divisions_matrix[col][i]==1 and count<1:
                    time_1st.append(divisions_matrix.index.values[i])
                    count+=1
                
    num_divisions,time_1st,ID=zip(*sorted(zip(num_divisions,time_1st,ID)))
#    print(num_divisions)
#    print(time_1st)
#    print(ID)
    
    df_new=pd.DataFrame(columns=ID,index=divisions_matrix.index.values)
    
    for column in ID:
        df_new[column]=divisions_matrix[column]
    
    for j in range(len(num_Ids)):
        vect=[]
        for k in range(time_points):
            vect.append(df_new.iloc[k,j])
        division_profile[j,:]=vect
        
    for xx in range(len(num_Ids)):
        divisions=[]
        for yy in range(time_points):
            if division_profile[xx,yy]==1:
                divisions.append(yy)
        if len(divisions)>0:
            for n in range(len(divisions)-1):
                division_profile[xx,divisions[n]+1:divisions[n+1]]=division_profile[xx,divisions[n]+1:divisions[n+1]]+(n+1)   
            division_profile[xx,divisions[-1]+1:time_points]=division_profile[xx,divisions[-1]+1:time_points]+len(divisions)
    
     
    fig=plt.figure()
    plt.figure(figsize=(8, 14))
    positions=(0,50,100,150,200)
    label=(0,25,50,75,100)
    plt.xticks(positions,label)
    color_map=plt.imshow(division_profile)
    color_map.set_cmap("plasma")
    plt.xlabel('Time(h)')
    plt.ylabel('Cell number')
    ax=plt.gca()
    divider=make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cb=plt.colorbar(cax=cax)
    labels=np.arange(0,sum(divisions),1)
    loc=labels+0
    cb.set_ticks(loc)
    cb.set_ticklabels(labels)
    plt.title(str(ii)+' '+str(nom2)+' density',loc='right')
#    plt.savefig(path4+'Division_profile_'+str(ii)+'.png')
    plt.show()
    
    division_profile=pd.DataFrame(division_profile)
    division_profile.to_excel(path4+'Division_profile_'+str(ii)+'_'+str(nom2)+'.xlsx')

            