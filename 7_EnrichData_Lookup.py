# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 16:14:59 2020

@author: Sandeep Bisht
"""

import pandas as pd
import numpy as np

df_src=pd.DataFrame(
    [['a',1,'X1','Y1','Z1'],
     ['b',2,'X2','Y2','Z2'],
     ['c',3,'X3','Y3','Z3'],
     ['d',4,'X4','Y4','Z4']],
    columns=['k1','k2','col1','col2','col3']
    )

df_lkp1=pd.DataFrame(
    [['a',2,'X2_L1'],
     ['b',2,'X2_L1'],
     ['c',3,'X3_L1'],
     ['e',5,'X5_L1']],
    columns=['k1','k2','val1']
      )

df_lkp2=pd.DataFrame(
    [['a',1,'X1_L2'],
     ['b',2,'X2_L2'],
     ['d',4,'X4_L2']],
    columns=['k1','k2','val2']
      )

print('\n Source File is as :\n')
print(df_src)

print('\n Lookup File1 is as :\n')
print(df_lkp1)

print('\n Lookup File2 is as :\n')
print(df_lkp2)

# Case 1 : Enriching Lookup 1 only
df_enrch=pd.merge(df_src,df_lkp1,how='left', on=['k1','k2'])
df_enrch['col1']=np.where(
    (df_enrch['val1'].notnull() & (df_enrch['col1']!=df_enrch['val1'])),
    df_enrch['val1'],
    df_enrch['col1']                         
                          )
df_enrch1=df_enrch.drop(['val1'], axis=1)
print('\n Enriched data using Lookup File1 is as :\n')
print(df_enrch1)

# Case 2 : Enriching Lookup 1 & 2 both
df_enrch2=pd.merge(pd.merge(df_src,df_lkp1,how='left', on=['k1','k2']),df_lkp2,how='left')
print('\n Data after joining Lookup file 1 & 2 is as :\n')
print(df_enrch2)

df_enrch2['col1']=np.where(
    (df_enrch2['val1'].notnull() & (df_enrch2['col1']!=df_enrch2['val1'])),
    df_enrch2['val1'],
    np.where(
        df_enrch2['val1'].isnull(),
        np.where(
            (df_enrch2['val2'].notnull() & (df_enrch2['col1']!=df_enrch2['val2'])),
            df_enrch2['val2'],
            df_enrch2['col1']
            ),
        df_enrch2['col1']    
        )   
    )

df_enrch2.drop(['val1','val2'],axis =1, inplace=True)
print('\n Enriched data using Lookup File1 & 2 is as :\n')
print(df_enrch2)
