# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 16:10:31 2021

@author: nicag
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pyboat import WAnalyzer
from pyboat import ensemble_measures as em
from pyboat import plotting as pl 

plt.rcParams.update({'font.size': 18})

def powerthresh(wAn,signal):
    wAn.compute_spectrum(signal,do_plot=False)
    wAn.get_maxRidge(power_thresh=0,smoothing_wsize=4)
    rd=wAn.ridge_data
    max_power=rd['power'].max()
    pthresh=max_power*0.25
    return pthresh

name_folder='ridge_result/'
name_folder2='powerseries/'
name_folder3='Divisions/'
name_folder4='Phase_coherence/'
path='C:/Users/nicag/Desktop/William_traces/'
path2=str(path)+str(name_folder)
path3=str(path)+str(name_folder2)
path4=str(path)+str(name_folder3)
path5=str(path)+str(name_folder4)

channel1='cell_cycle'
channel2='circadian'

channel1='cell_cycle'
channel2='circadian'
file_list=['untreated','0uM','5uM','10uM']
file_list2=['low','medium','high']
magn1='frequent_dividers_'
magn2='sporadic_dividers_'
magn=magn2
channel=channel2
colors_list=['blue','green','red','orange','lime','purple']

ph_coh=pd.DataFrame(columns=file_list2)
for i in range(4):
    nom=file_list[i]
    nom2=file_list2[2]
    file=str(nom2)+'_density_'+str(nom)+'_'+str(channel)
    file11=magn+str(nom)+'_'+str(channel)
    
    data=pd.read_csv(path+file+r'.csv')
#    data = pd.read_excel(path4+file11+r'.xlsx')
#    data=data.fillna(-1)
   
##Only for the entire file    
#    data=pd.read_csv(path+file+r'.csv')
    
##    #If we want only the first part of the experiment
#    thresh=int((max(data['frame'])+1)/2)
#    select_index_2=data.loc[data['frame']<=thresh]['frame']
#    data=data.loc[data['frame'].isin(select_index_2)]
    
    power_series=pd.read_csv(path3+file+r'_powerseries.csv')
    select_index=power_series.loc[power_series['0']>10]['index']
    data=data.loc[:,data.columns.isin(select_index)]
        
    dt = 0.5 # the sampling interval, 0.5hours
    lowT=16
    highT=32
    periods = np.linspace(lowT, highT, 200)
    wAn = WAnalyzer(periods, dt, time_unit_label='hours')
    
    time=data.index.values*0.5
    num_signals=len(data.columns)-1
    print(num_signals)
        
    norm_signals=pd.DataFrame(columns=data.columns, index=data.index)
    
    count=0
    ridge_results={}
    ridge_table=pd.DataFrame()
    for column in data:
        if count>=0 and count<=num_signals: #equal to 0 if there is no frame column
            signal=data[column].dropna()
            
            #For circadian signal only
            trend=wAn.sinc_smooth(signal, T_c=52)
            detrended=signal-trend
            norm_signal = wAn.normalize_amplitude(detrended, window_size=50)
            norm_signals[column]=norm_signal
            
#            norm_signals[column]=signal
                
        count+=1

    for icol in norm_signals:
        norm_signal=norm_signals[icol].dropna()
        wAn.compute_spectrum(norm_signal, do_plot=False) #computes the detrended signal wavelet spectrum
#        power_th=powerthresh(wAn,signal)
        rd=wAn.get_maxRidge(power_thresh=0, smoothing_wsize=5) #gets the maximum ridge
        rd.set_index(norm_signal.index,inplace=True)
        ridge_results[icol]=rd
        rd['traceId']=icol
    
    powers_series = em.average_power_distribution(ridge_results.values(),signal_ids = ridge_results.keys())
    high_power_ids = powers_series[powers_series > 1].index
    high_power_ridge_results = [ridge_results[i] for i in high_power_ids]
    res = em.get_ensemble_dynamics(high_power_ridge_results)
    pl.ensemble_dynamics(*res)
    plt.show()
    plt.close()
    
    ph_coh[nom]=res[0]['median']  #0,1,2: median; 3: R
 
#ph_coh.to_excel(path5+'Phase_coherence_inhibitor.xlsx')

#ph_coh=pd.read_excel(path5+'Phase_coherence_inhibitor.xlsx')
time=ph_coh.index.values*0.5
fig=plt.figure()
for i in range(4):
    plt.plot(time,ph_coh[file_list[i]],color=colors_list[i],label=file_list[i]+' 100%')
plt.xlabel('Time(h)')
plt.ylabel('Period(h)')
fig.set_figheight(10)
fig.set_figwidth(12)
plt.legend(loc='best')
plt.title(str(channel)+' channel ')#+str(magn))
plt.show()

