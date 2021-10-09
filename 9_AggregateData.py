# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 16:07:25 2020

@author: Sandeep Bisht
"""

import pandas as pd
import numpy as np


df_src=pd.DataFrame(
    [['a',1,50],
     ['b',2,100],
     ['a',2,125],
     ['b',2,50],
     ['a',1,175],
     ['c',3,200]],
    columns=['k1','k2','col1']
    )

df_src['type']=np.nan
print(' \n Source records is as: \n')
print(df_src)

df_agg=df_src.groupby(['k1','k2']).agg({'col1':['sum']}).reset_index(['k1','k2'])
df_agg.columns=df_agg.columns.droplevel(1)
df_agg['type']='9Z'
print(' \n 9Z records is as: \n')
print(df_agg.head())

df_final=df_src.append(df_agg).sort_values(by=['k1','k2'], ignore_index=True)
print(' \n Aggregated Data showing 9Z records is as: \n')
print(df_final)
