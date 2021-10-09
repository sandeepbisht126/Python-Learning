# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 13:07:15 2020

@author: Sandeep Bisht
"""

import pandas as pd

df_ff=pd.DataFrame(
    [['a',1,'X1','Y1','Z1'],
     ['b',2,'X2','Y2','Z2'],
     ['c',3,'X3','Y3','Z3'],
     ['d',4,'X4','Y4','Z4']],
    columns=['k1','k2','col1','col2','col3']
    )

df_sod=pd.DataFrame(
    [['a',1,'X1','Y1','Z'],
     ['b',2,'X2','Y','Z'],
     ['c',3,'X3','Y3','Z3'],
     ['e',5,'X5','Y5','Z5']],
    columns=['k1','k2','col1','col2','col3']
    )

df_ff['Active']='Y'
df_sod['Active']='N'
print('Full file DataFrame : \n')
print(df_ff)
print('\nDelta file DataFrame : \n')
print(df_sod)

df_scd2=df_ff.append(df_sod,ignore_index=True).drop_duplicates(subset=['k1','k2','col1','col2','col3'])
print('\nSCD2 file DataFrame : \n')
print(df_scd2)