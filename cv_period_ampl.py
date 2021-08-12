# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 15:53:48 2021

@author: nicag
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pyboat import WAnalyzer
from pyboat import ensemble_measures as em
from pyboat import plotting as pl 

plt.rcParams.update({'font.size': 20})

name_folder='Amplitude_vs_trend/'
name_folder2='powerseries/'
path='C:/Users/nicag/Desktop/William_traces/'
path2=str(path)+str(name_folder)
path3=str(path)+str(name_folder2)

dt = 0.5 # the sampling interval, 0.5hours
lowT=16
highT=32
periods = np.linspace(lowT, highT, 200)
wAn = WAnalyzer(periods, dt, time_unit_label='hours')

channel1='cell_cycle'
channel2='circadian'
file_list=['untreated','0uM','5uM','10uM']
file_list2=['low','medium','high']

#path='C:/Users/nicag/Desktop/TNBC/Single_cell_data_Anna/'
#file_list=['25','50','100','DMSO100','5uM100','10uM100']

for i in range(4):
    nom=file_list[i]
    file='high_density_'+str(nom)+'_'+str(channel2)
#    file=str(file_list2[i])+'_density_'+str(file_list[0])+'_'+str(channel2)
#    file='InterpolatedTraces_'+str(nom)

    data = pd.read_csv(path+file+r'.csv')
    data=data.fillna(-1)
        
    time=data[str(data.columns[0])]*0.5
    
    file1='high_density_'+str(nom)+'_'+str(channel2)
    
    power_series=pd.read_csv(path3+file1+r'_powerseries.csv')
    select_index=power_series.loc[power_series['0']>10]['index']
    data=data[select_index]
    
    num_signals=len(data.columns)-1
    print(num_signals)
    
    count=0
    ridge_results={}
    cv_per1=[]
    cv_per2=[]
    
    cv_amp1=[]
    cv_amp2=[]

    for column in data:
        if count>0 and count<=num_signals:
            signal=data[column]
            trend=wAn.sinc_smooth(signal, T_c=72)
            detrended=signal-trend
            wAn.compute_spectrum(detrended, do_plot=False) #computes the detrended signal wavelet spectrum
            wAn.get_maxRidge(power_thresh=0, smoothing_wsize=4) #gets the maximum ridge
            rd=wAn.ridge_data
            ridge_results[column]=rd
            interv1=int(len(time)/2)
            cv_per1.append(np.std(rd['periods'][0:interv1])/np.mean(rd['periods'][0:interv1]))
            cv_per2.append(np.std(rd['periods'][interv1:len(time)])/np.mean(rd['periods'][interv1:len(time)]))
            cv_amp1.append(np.std(rd['amplitude'][0:interv1])/np.mean(rd['periods'][0:interv1]))
            cv_amp2.append(np.std(rd['amplitude'][interv1:len(time)])/np.mean(rd['periods'][interv1:len(time)]))

        count+=1

    cv_periods={'1st interval':cv_per1,'2nd interval':cv_per2}        
    df=pd.DataFrame(cv_periods, columns=['1st interval','2nd interval'])
    fig=plt.figure()
    df.boxplot(column=['1st interval','2nd interval'])
    plt.ylabel('Coefficient of variation of periods')
    plt.title(str(nom)+'100%')
    fig.set_figheight(10)
    fig.set_figwidth(12)
    plt.savefig(path2+'CV_periods_'+str(nom)+'.png')
    plt.show()
    
    cv_amplitudes={'1st interval':cv_per1,'2nd interval':cv_per2}        
    df=pd.DataFrame(cv_amplitudes, columns=['1st interval','2nd interval'])
    fig=plt.figure()
    df.boxplot(column=['1st interval','2nd interval'])
    plt.ylabel('Coefficient of variation of amplitudes')
    plt.title(str(nom)+'100%')
    fig.set_figheight(10)
    fig.set_figwidth(12)
    plt.savefig(path2+'CV_amplitudes_'+str(nom)+'.png')
    plt.show()


#            
#            
#            
#            
#            
#            
            
            
            
            