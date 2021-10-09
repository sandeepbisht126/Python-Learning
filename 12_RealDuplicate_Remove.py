# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 17:02:57 2020

@author: Sandeep Bisht
"""


import pandas as pd
import numpy as np

df_src=pd.DataFrame(
    [['Mumbai','Pune',150],
     ['Delhi','Bhopal',550],
     ['Pune','Mumbai',150],
     ['Dehradoon','Delhi',200],
     ['Bhopal','Delhi',550]
     ],
    columns=['Source','Destination','Distance']
    )

print('\n Source data is as: \n')
print(df_src)

df_interm=pd.DataFrame(columns=['Source','Destination','Distance'])
for k,v in df_src.iterrows():
    if (v['Source'] > v['Destination']):
        df_interm=df_interm.append({'Source': v['Destination'],'Destination':v['Source'],'Distance':v['Distance']}, ignore_index=True)
    else:
        df_interm=df_interm.append({'Source': v['Source'],'Destination':v['Destination'],'Distance':v['Distance']}, ignore_index=True)
    
df_final=df_interm.drop_duplicates(ignore_index='True')    
print('\n Final data after removing real dups is as: \n')
print(df_final)
