# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:40:42 2020

@author: Sandeep Bisht
"""


import numpy as np
import pandas as pd

df_emp=pd.DataFrame(
    [[101,'X1',500,100,1000,250],
     [102,'Y1',700,150,1500,300],
     [103,'Z1',800,np.nan,2500,350]
     ],
    columns=['EmpId','Name','HRA','LTA','BASIC','PF']
     )

print('\n Employee Data is as: \n')        
print(df_emp)

key_col=['EmpId','Name']
comp_col=[col for col in df_emp.columns if col not in key_col]

df_final=pd.DataFrame(columns=['EmpId','Name','Component','Amount'])
for k,v in df_emp.iterrows():
    for i in comp_col:
        df_final=df_final.append({'EmpId':v['EmpId'],'Name':v['Name'],'Component':i,'Amount':v[i]},ignore_index=True)
       
print('\n Final Data is as: \n')        
print(df_final)        
        