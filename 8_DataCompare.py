# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 13:08:25 2020

@author: Sandeep Bisht
"""


import pandas as pd
import numpy as np

key=['k1','k2']
allcols=['k1','k2','col1','col2','col3']
attrcols=[i for i in allcols if i not in key]
srccols=[i + '_src'  for i in allcols]
tgtcols=[i + '_tgt'  for i in allcols]
srcattrcols=[i + '_src'  for i in attrcols]
tgtattrcols=[i + '_tgt'  for i in attrcols]
srckeycols=[i + '_src'  for i in key]
tgtkeycols=[i + '_tgt'  for i in key]

#df_srcattrcols=['df_common['+"'"+i+"'"+']' for i in srcattrcols]
#df_tgtattrcols=['df_common['+"'"+i+"'"+']' for i in tgtattrcols]

df_src=pd.DataFrame(
    [['a',1,'X1','Y1','Z1'],
     ['b',2,'X2','Y2','Z2'],
     ['c',3,'X3','Y3','Z3'],
     ['d',4,'X4','Y4','Z4']],
    columns=['k1','k2','col1','col2','col3']
    )
df_src.columns +='_src'
print(' \n Data set 1 is :\n')
print(df_src)

df_tgt=pd.DataFrame(
    [['a',1,'X1','Y1','Z1'],
     ['b',2,'X2','Y','Z2'],
     ['c',3,'X3','Y3','Z'],
     ['e',5,'X5','Y5','Z5']],
    columns=['k1','k2','col1','col2','col3']
    )
df_tgt.columns +='_tgt'
print(' \n Data set 2 is :\n')
print(df_tgt)

df_fjoin=pd.merge(df_src,df_tgt, left_on=srckeycols, right_on=tgtkeycols, how ='outer')
print(df_fjoin)

#Case 1: Left only records
equi_tgt_key=[]
notequi_tgt_key=[]
for tgt_key in tgtkeycols:
    notequi_tgt_key.append(tgt_key+'!='+tgt_key)
    equi_tgt_key.append(tgt_key+'=='+tgt_key)
    
print(notequi_tgt_key)

str_tgt_keynull=' and '.join(notequi_tgt_key)
print(str_tgt_keynull)
#df_lonly=df_fjoin[df_fjoin['k1_tgt'].isnull() & df_fjoin['k2_tgt'].isnull()].drop(tgtcols, axis=1)
df_lonly=df_fjoin.query(str_tgt_keynull).drop(tgtcols, axis=1)
df_lonly.columns=allcols
print(' \n Left only records are as :\n')
print(df_lonly)

#Case 2: Right only records
equi_src_key=[]
notequi_src_key=[]
for src_key in srckeycols:
    notequi_src_key.append(src_key+'!='+src_key)
    equi_src_key.append(src_key+'=='+src_key)

str_src_keynull=' and '.join(notequi_src_key)
#df_ronly=df_fjoin[df_fjoin['k1_src'].isnull() & df_fjoin['k2_src'].isnull()].drop(srccols, axis=1)
df_ronly=df_fjoin.query(str_src_keynull).drop(srccols, axis=1)
df_ronly.columns=allcols
print(' \n Right only records are as :\n')
print(df_ronly)

#Case 3: Match records
str_all_keynotnull=' and '.join(equi_tgt_key + equi_src_key)
#df_common=df_fjoin[df_fjoin['k1_src'].notnull() & df_fjoin['k2_src'].notnull() & df_fjoin['k1_tgt'].notnull() & df_fjoin['k2_tgt'].notnull()]
df_common=df_fjoin.query(str_all_keynotnull)

lst_match_cndn=[]
for s,t in zip(srcattrcols,tgtattrcols):
    lst_match_cndn.append(s+'=='+t)
str_match_cndn=' and '.join(lst_match_cndn)

df_match=df_common.query(str_match_cndn).copy()
df_match.drop(tgtattrcols+tgtkeycols, axis=1, inplace=True)
df_match.columns=allcols
print(' \n Exact match records are as :\n')
print(df_match)

#Case 4: Mismatch records
str_mismatch_cndn='~('+str_match_cndn+')'
df_mismatch=df_common.query(str_mismatch_cndn).copy()

for s,t in zip(srcattrcols,tgtattrcols):
    newcol=s[:4]
    df_mismatch[newcol]=np.where(
        (df_mismatch[s]!=df_mismatch[t]),
        (df_mismatch[s].astype(str)+'-->'+df_mismatch[t]),
        df_mismatch[s]
        )

df_mismatch.drop(srcattrcols+tgtattrcols+tgtkeycols, axis=1, inplace=True)
df_mismatch.columns=allcols
print(' \n Mismatch records are as :\n')
print(df_mismatch)

html = df_mismatch.to_html()
#print(html)

#write html to file
text_file = open('C:\\Users\\Python\\Data\\Mismatch.html', "w")
text_file.write(html)
text_file.close()