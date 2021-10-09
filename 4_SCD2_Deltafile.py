# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 13:07:15 2020

@author: Sandeep Bisht
"""

import pandas as pd
import numpy as np

df_delta=pd.DataFrame(
    [['a',1,'X1','Y1','Z1'],
     ['b',2,'X2','Y2','Z2'],
     ['c',3,'X3','Y3','Z3'],
     ['d',4,'X4','Y4','Z4']],
    columns=['k1','k2','col1','col2','col3']
    )

df_sod=pd.DataFrame(
    [['a',1,'X1','Y1','Z'],
     ['b',2,'X2','Y','Z'],
     ['c',3,'X','Y3','Z3'],
     ['e',5,'X5','Y5','Z5']],
    columns=['k1','k2','col1','col2','col3']
    )

df_merge=pd.merge(df_delta,df_sod, on=['k1','k2'], how='outer')
print(df_merge)

#df_active=df_merge[['k1','k2','col1_x','col2_x','col3_x']][df_merge['col1_x'].notnull()]
df_delta['Active']='Y'
df_active1=df_delta
print(df_active1)

#Matching SOD records from Delta file, these should be inactivated
df_sod_match=df_merge[['k1','k2','col1_x','col1_y','col2_y','col3_y']]
df_inactive1=df_sod_match[['k1','k2','col1_y','col2_y','col3_y']][df_sod_match.col1_x.notnull() & df_sod_match.col1_y.notnull()]
df_inactive1.columns=['k1','k2','col1','col2','col3']
df_inactive1['Active']='N'
print(df_inactive1)

#Non matching SOD records from Delta file, these are SOD only records
df_sod_notmatch=df_merge[['k1','k2','col1_x','col1_y','col2_y','col3_y']]
df_active2=df_sod_notmatch[['k1','k2','col1_y','col2_y','col3_y']][df_sod_notmatch.col1_x.isnull() & df_sod_notmatch.col1_y.notnull()]
df_active2.columns=['k1','k2','col1','col2','col3']
df_active2['Active']='Y'
print(df_active2)

df_scd2=pd.concat([df_active1,df_active2,df_inactive1], ignore_index=True).drop_duplicates(subset=['k1','k2','col1','col2','col3'])
print('\nSCD2 dataframe is : \n')
print(df_scd2)

## Sceanrio -2 - Keep few SOD col value intact - non-SCD cols
df_noncheck=df_sod[['k1','k2','col1']]
df_noncheck.columns=['k1','k2','col_persist']
print(df_noncheck)

df_final=pd.merge(df_scd2,df_noncheck, on=['k1','k2'], how ='left')
print(df_final)

df_final['col1']=np.where(((df_final['col1']!=df_final['col_persist']) & (df_final['col_persist'].notnull())),
                          df_final['col_persist']
                          ,df_final['col1'])
df_final=df_final[['k1','k2','col1','col2','col3','Active']].drop_duplicates(subset=['k1','k2','col1','col2','col3'])
print(df_final)



