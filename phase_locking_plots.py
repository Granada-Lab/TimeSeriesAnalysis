# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 13:07:24 2021

@author: nicag
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from mpl_toolkits.axes_grid1 import make_axes_locatable


plt.rcParams.update({'font.size': 18})

def shannon_entropy(p):
    p_norm=p/float(np.sum(p))
    p_norm=p_norm[np.nonzero(p_norm)]
    H = -sum(p_norm* np.log2(p_norm))  
    return H

def mutual_info(X,Y,bins):
   p_XY=np.histogram2d(X,Y,bins,density=True)[0]
   p_X=np.histogram(X,bins,density=True)[0]
   p_Y=np.histogram(Y,bins,density=True)[0]
   
   H_X=shannon_entropy(p_X)
   H_Y=shannon_entropy(p_Y)
   H_XY=shannon_entropy(p_XY)

   MI=H_X+H_Y-H_XY
   
#   plt.hist2d(X,Y,bins=bins,density=True)
#   plt.show()
#   plt.hist(X,bins=bins,density=True)
#   plt.title('Cell cycle')
#   plt.show()
#   plt.hist(Y,bins=bins,density=True)
#   plt.title('Circadian rhythm')
#   plt.show()
     
   return MI

def moransI_square(data):
    sum_w   = 0
    total_sum = 0
    len_x = len(data[0])
    len_y = len(data[1])
    NaNFilteredData = data.flatten()[np.argwhere(~np.isnan(data).flatten())].flatten() #Clear data from NaNs
    total_mean = np.mean(data) #Mean value of the data
    for i in range(0, len_x):
        for j in range(0, len_y):
            if np.isnan(data[i][j]) != True: #Check if NaN
                for n in range(0, len_x):
                    for m in range(0, len_y):
                        if np.isnan(data[n][m]) != True: 
                            dist = np.sqrt((i-n)**2+(j-m)**2) #Computing distance between neighbours
                            if dist == 1: #Defining the spatial weight matrix on a grid lattice
                                w = 1.
                            else:
                                w = 0.
                            sum_w += w
                            total_sum += w * ( data[i][j] - total_mean ) * ( data[n][m] - total_mean ) #Local coherence
    val = sum(~np.isnan(data).flatten()) * total_sum / sum_w / sum( (NaNFilteredData - total_mean)**2 ) #Local coherence divided by global coherence
    return val


name_folder='ridge_result/'
name_folder2='powerseries/'
name_folder3='Divisions/'
path='C:/Users/nicag/Desktop/William_traces/'
path2=str(path)+str(name_folder)
path3=str(path)+str(name_folder2)
path4=str(path)+str(name_folder3)

file_list1=['untreated','0uM','5uM','10uM']
file_list2=['low','medium','high']

colors_list=['blue','green','red','orange','lime','purple']

channel1='circadian'
channel2='cell_cycle'
magn1='frequent_dividers_'
magn2='sporadic_dividers_'
magn=magn2

mi_matrix=np.zeros((len(file_list2),len(file_list1)))
for k in range(3):
    for i in range(4):
        nom=file_list1[i]
        nom2=file_list2[k]
        
        file1=str(nom2)+'_density_'+str(nom)+'_'+str(channel1)
        file11=magn+'ro_'+str(nom2)+'_'+str(channel1)
        file2=str(nom2)+'_density_'+str(nom)+'_'+str(channel2)
        file22=magn+'ro_'+str(nom2)+'_'+str(channel2)
    
        data1 = pd.read_csv(path2+file1+r'.csv')
        data2 = pd.read_csv(path2+file2+r'.csv')
            
    #    data1 = pd.read_excel(path4+file1+r'.xlsx')
    #    data2 = pd.read_excel(path4+file2+r'.xlsx')
        
        data1.dropna(inplace=True)
        data2.dropna(inplace=True)
        
        thresh=int((max(data1['frame'])+1)/2)
        
        power_series=pd.read_csv(path3+file1+r'_powerseries.csv')
        select_index=power_series.loc[power_series['0']>10]['index']
        cell_cycle=data1.loc[data1['traceId'].isin(select_index)]
        circadian=data2.loc[data2['traceId'].isin(select_index)]
        
        if k==0:
            nn=67
        elif k==1:
            nn=137
        elif k==2:
            nn=820
        
        #Randomly select some traces
        random_num=random.sample(set(cell_cycle['traceId']),nn)
        cell_cycle=cell_cycle.loc[cell_cycle['traceId'].isin(random_num)]
        circadian=circadian.loc[circadian['traceId'].isin(random_num)]
        select_index=random_num
#        
    #    #Split the experiment in two parts and choose the first/second part of the data
    #    select_index_2=cell_cycle.loc[cell_cycle['frame']>thresh]['frame']
    #    cell_cycle=cell_cycle.loc[cell_cycle['frame'].isin(select_index_2)]
    #    circadian=circadian.loc[circadian['frame'].isin(select_index_2)]
    
        ph_cell=cell_cycle['phase']/(2*np.pi)
        ph_circ=circadian['phase']/(2*np.pi)
        ph_cell=ph_cell.to_numpy()
        ph_circ=ph_circ.to_numpy()
        
        fig=plt.figure()
        hist2D=plt.hist2d(ph_circ,ph_cell,bins=np.arange(0,1.01,0.05),cmap=plt.cm.jet,density=True, vmin=0.5, vmax=1.5)
        plt.colorbar()
        plt.xlabel(r'Circadian phase ($\theta$/2$\pi$)')
        plt.ylabel(r'Cell cycle phase ($\theta$/2$\pi$)')
    
        num_cells=len(set(cell_cycle['traceId']))    
        moran_I=moransI_square(hist2D[0])
#        if num_cells<200:
#            num_bins=5
#        else:
#            num_bins=20
        mi=mutual_info(ph_cell,ph_circ,20)
        mi_matrix[k,i]=mi
        
        plt.title(str(nom)+" "+str(nom2)+", Moran's I: {:.3f}, MI: {:.3f} (n={})".format(moran_I,mi,num_cells))
        fig.set_figheight(10)
        fig.set_figwidth(12)
    #    plt.savefig('Phase_locking_high_density_'+str(magn)+'_'+str(nom)+'.png')
        plt.show()
        
    #    print(moransI_square(hist2D[0]))
        print(mutual_info(ph_cell,ph_circ,20))
        
  
print(mi_matrix)      
fig=plt.figure()
plt.figure(figsize=(10, 10))
positions=(0,1,2,3)
plt.xticks(positions,file_list1)
color_map=plt.imshow(mi_matrix)
color_map.set_cmap("viridis")
plt.xlabel(r'TGF-$\beta$ inhibitor dose')
positions2=(0,1,2)
plt.yticks(positions2,file_list2)
plt.ylabel('Density')
#plt.ylabel('Cell number')
ax=plt.gca()
divider=make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cb=plt.colorbar(cax=cax)
#plt.title(str(ii)+' '+str(nom2)+' density',loc='right')
plt.show()
        
        
