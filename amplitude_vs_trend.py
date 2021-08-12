# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 11:41:04 2021

@author: nicag
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pyboat import WAnalyzer
from pyboat import ensemble_measures as em
from pyboat import plotting as pl 

plt.rcParams.update({'font.size': 18})

name_folder='Amplitude_vs_trend/'
path='C:/Users/nicag/Desktop/William_traces/'
path2=str(path)+str(name_folder)

dt = 0.5 # the sampling interval, 0.5hours
lowT=16
highT=32
periods = np.linspace(lowT, highT, 200)
wAn = WAnalyzer(periods, dt, time_unit_label='hours')

channel1='cell_cycle'
channel2='circadian'
file_list=['untreated','0uM','5uM','10uM']
file_list2=['low','medium','high']
for i in range(3):
    nom=file_list[i]
    file='high_density_'+str(nom)+'_'+str(channel2)
    file=str(file_list2[i])+'_density_'+str(file_list[0])+'_'+str(channel2)
    
    data = pd.read_csv(path+file+r'.csv')
    data=data.fillna(-1)
    
    num_signals=len(data.columns)-1
    print(num_signals)
    
    time=data[str(data.columns[0])]*0.5
    
    df_amplitude=pd.DataFrame(columns=data.columns)   
    df_trend=pd.DataFrame(columns=data.columns)    
    df_amplitude['frame']=time
    df_trend['frame']=time
    
    count=0
    ridge_results={}
    for column in data:
        if count>0 and count<=num_signals:
            signal=data[column]
            trend=wAn.sinc_smooth(signal, T_c=72)
            detrended=signal-trend
            wAn.compute_spectrum(detrended, do_plot=False) #computes the detrended signal wavelet spectrum
            wAn.get_maxRidge(power_thresh=0, smoothing_wsize=4) #gets the maximum ridge
            rd=wAn.ridge_data
            ridge_results[column]=rd
            df_amplitude[column]=rd['amplitude']
            df_trend[column]=trend
    #        plt.plot(time,rd['amplitude'])
    #        plt.plot(time,trend)
    #        plt.show()
        count+=1
    
    #df_amplitude.to_csv(path2+'Amplitude_'+str(file)+'.csv',index=False)
    #df_trend.to_csv(path2+'Trend_'+str(file)+'.csv',index=False)
    
    median_amp=[]
    median_trend=[]
    time_new=[]
    for j in range(len(time)):
        if j%1==0:
            median_amp.append(np.median(df_amplitude.iloc[j]))
            median_trend.append(np.median(df_trend.iloc[j]))
            time_new.append(time[j])
    fig=plt.figure()
    plt.scatter(median_amp,median_trend,c=time_new,cmap='viridis')
#    plt.title(str(nom)+'100%')
    plt.title(str(file_list2[i])+' density')
    plt.xlabel('Detrended amplitude')
    plt.ylabel('Trend')
    fig.set_figheight(10)
    fig.set_figwidth(12)
    plt.savefig(path2+'Trend_vs_amp_'+str(file)+'.png')
    plt.show()
    





