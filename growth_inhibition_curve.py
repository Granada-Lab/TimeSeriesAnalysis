# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 13:12:56 2021

@author: nicag
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 20})

name_folder='Cell_growth/'
path='C:/Users/nicag/Desktop/William_traces/'
path2=str(path)+str(name_folder)

conditions_list=['untreated','0uM','1.25uM','2.5uM','5uM','10uM']
color_list=['tab:red','tab:orange','tab:green','tab:purple','tab:blue','tab:brown']
dens=['High','Medium','Low']
density_cond=dens[2]
file=str(density_cond)+'_density_cell_growth_norm'
data=pd.read_excel(path2+file+r'.xlsx')
print(data)
time=data['Unnamed: 0']*0.5

fig=plt.figure()
count=0
for col in conditions_list:
    plt.plot(time,data[col],label=conditions_list[count],color=color_list[count],linewidth=3.5)
    count+=1
plt.legend(loc='best')
plt.xlabel('Time(h)')
plt.ylabel('Normalized number of cells')
fig.set_figheight(10)
fig.set_figwidth(13)
plt.show()

fig=plt.figure()
untreated=data['untreated'][int(len(time)-20):len(time)]
count=0
rel_values=[]
for col in conditions_list:
    signal=data[col]
    vect=signal[int(len(time)-20):len(time)]
    last=np.mean(vect)
    rel=last/np.mean(untreated)
    count+=1
    rel_values.append(rel)
plt.plot(conditions_list,rel_values,linestyle='-',marker='o',markersize=8)
plt.ylabel('Relative growth of cells to the untreated')
plt.title(str(density_cond)+' density')
fig.set_figheight(10)
fig.set_figwidth(13)
plt.show()





    

