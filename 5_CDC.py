# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 13:42:11 2020

@author: Sandeep Bisht
"""
import pandas as pd

df_master=pd.DataFrame(
    [['a',1,'X1','Y1','Z1'],
     ['b',2,'X2','Y2','Z2'],
     ['c',3,'X3','Y3','Z3'],
     ['d',4,'X4','Y4','Z4']],
    columns=['k1','k2','col1','col2','col3']
    )

df_delta=pd.DataFrame(
    [['a',1,'X1','Y1','Z'],
     ['b',2,'X2','Y','Z'],
     ['c',3,'X3','Y3','Z3'],
     ['e',5,'X5','Y5','Z5']],
    columns=['k1','k2','col1','col2','col3']
    )

df_cdc=pd.concat([df_master,df_delta],ignore_index=True).drop_duplicates(subset=['k1','k2'], keep='last',ignore_index=True).sort_values(by=['k1','k2'])
print('\n CDC data is as - \n')
print(df_cdc)

