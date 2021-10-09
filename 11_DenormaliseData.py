# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:42:56 2020

@author: Sandeep Bisht
"""

import pandas as pd
import numpy as np

df_denorm=pd.DataFrame(
    [[101,'X1','HRA',500],
     [101,'X1','LTA',100],
     [101,'X1','BASIC',1000],
     [101,'X1','PF',250],
     [102 ,'Y1','HRA',700],
     [102 ,'Y1','LTA',150],
     [102,'Y1','BASIC',1500],
     [102,'Y1','PF',300],
     [103,'Z1','HRA',800],
     [103,'Z1','LTA',np.NaN],
     [103,'Z1','BASIC',2500],
     [103,'Z1','PF',350]
     ],
    columns=['EmpId','Name','Component','Amount'])

print('\n Normalised data is as: \n')
print(df_denorm)

key_col=['EmpId','Name']
comp_cols=list(df_denorm['Component'].unique())
all_cols=key_col + comp_cols

df_interm=pd.DataFrame(columns= all_cols)
for k,v in df_denorm.iterrows():
    print(k,v)
    dict1={}
    for comp_col in comp_cols:
        if (v['Component'] == comp_col):
            dict1['EmpId']=v['EmpId']
            dict1['Name']=v['Name']                             
            dict1[comp_col]=v['Amount']
        else:
            dict1['EmpId']=v['EmpId']
            dict1['Name']=v['Name']                             
            dict1[comp_col]=np.nan
    df_interm=df_interm.append(dict1,ignore_index=True)
#print(df_interm)

aggr_comp_col={i:max for i in comp_cols}
#{'HRA':max,'LTA':max,'BASIC':max,'PF':max}

df_final=df_interm.groupby(['EmpId','Name']).agg(aggr_comp_col).reset_index()
print('\n De-Normalised data is as: \n')
print(df_final)
