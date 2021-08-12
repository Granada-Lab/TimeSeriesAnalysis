# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 13:53:17 2021

@author: nicag
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

name_folder='Divisions/'
path='C:/Users/nicag/Desktop/William_traces/'
path2=str(path)+str(name_folder)
file_list=['untreated','0uM','5uM','10uM']
file_list2=['low','medium','high']

channel='cell_cycle'
channel2='circadian'
for i in range(4):
    nom=file_list[i]
    nom2=file_list2[0]
    
    file_name=str(nom2)+'_density_'+str(nom)+'_'+str(channel)
    file2=str(nom2)+'_density_'+str(nom)+'_'+str(channel2)
 
    df = pd.read_csv(path+file_name+r'.csv')
    circadian=pd.read_csv(path+file2+r'.csv')
    df=df.fillna(0)

    num_signals=len(df.columns)-1
    count=0
    
    frequent=[]
    sporadic=[]
    df_pos_new = pd.DataFrame(columns = df.columns)
    for column in df:
        division=[]
        c=0
        if count==0:
            frequent.append('frame')
            sporadic.append('frame')
        if count>0 and count<=num_signals:
            signal=df[column]
#            plt.plot(df['frame']*0.5,signal,linewidth=2.5)
            for i in range(len(signal)-5):
                if c==0 and (signal[i+1]-signal[i])<-1000 and (signal[i+2]-signal[i+1])<100 and (signal[i+3]-signal[i+2])<100 and (signal[i+4]-signal[i+3])<100 and (signal[i+5]-signal[i+4])<100:
                    division.append(1)
                    c=23
                    
#                    print(df['frame'][i]*0.5)
#                    plt.axvline(x=df['frame'][i]*0.5, color='black')
                    
                else:
                    division.append(0)
                    if c!=0:
                        c-=1
                        
#            plt.xlabel('Time(h)')
#            plt.ylabel('Signal intensity (a.u.)')
#            plt.title('Geminin')
#            plt.show()
                        
            df_pos_new[column]=division
            if sum(division)>2:
                frequent.append(df.columns[count])
            else:
                sporadic.append(df.columns[count])
                    

        count+=1
        
    df_pos_new['frame']=df['frame']
    df_pos_new.to_excel(path2+'divisions_'+str(nom2)+'_'+str(nom)+'.xlsx',index=False)
    
    print(len(frequent))
    print(len(sporadic))
    
    df_frequent=pd.DataFrame(columns=frequent)
    df_sporadic=pd.DataFrame(columns=sporadic)
    df_frequent_circ=pd.DataFrame(columns=frequent)
    df_sporadic_circ=pd.DataFrame(columns=sporadic)
    df_frequent['frame']=df['frame']
    df_frequent_circ['frame']=df['frame']
    df_sporadic['frame']=df['frame']
    df_sporadic_circ['frame']=df['frame']

    for col in df_frequent:
        df_frequent[col]=df[col]
        df_frequent_circ[col]=circadian[col]
    df_frequent.to_excel(path2+'frequent_dividers_'+str(nom2)+'_'+str(nom)+'_cell_cycle.xlsx',index=False)
    df_frequent_circ.to_excel(path2+'frequent_dividers_'+str(nom2)+'_'+str(nom)+'_circadian.xlsx',index=False)

    for cols in df_sporadic:
        df_sporadic[cols]=df[cols]
        df_sporadic_circ[cols]=circadian[cols]
    df_sporadic_circ.to_excel(path2+'sporadic_dividers_'+str(nom2)+'_'+str(nom)+'_cell_cycle.xlsx',index=False)    
    df_sporadic_circ.to_excel(path2+'sporadic_dividers_'+str(nom2)+'_'+str(nom)+'_circadian.xlsx',index=False)
    

                
            




    
    
    
    