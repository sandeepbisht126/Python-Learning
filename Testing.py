# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:00:29 2020

@author: Sandeep Bisht
"""


import pandas as pd
import numpy as np

key=['k1','k2']
allcols=['k1','k2','col1','col2','col3']
#attrcols=list(set(allcols) - set(key))
attrcols=[ i for i in allcols if i not in key]
srccols=[i + '_src'  for i in allcols]
tgtcols=[i + '_tgt'  for i in allcols]
srcattrcols=[i + '_src'  for i in attrcols]
tgtattrcols=[i + '_tgt'  for i in attrcols]
df_srcattrcols=['df_common['+"'"+i+"'"+']' for i in srcattrcols]
df_tgtattrcols=['df_common['+"'"+i+"'"+']' for i in tgtattrcols]
print(attrcols)
print(srcattrcols)
print(tgtattrcols)

str1='Sandeep'
new_str='-'.join(str1)
print(new_str)

df = pd.DataFrame(np.random.randn(30, 3), columns=['a','b','c'])
df_filtered = df.query('a > 0').query('0 < b < 2')
print(df_filtered)

df = pd.DataFrame({'value': [3, 4, 9, 10, 11, np.nan, 12]})
#df.query('value!=value',inplace=True)
print(df)

lst=[1,2,3] + [4,5]
print(lst)

df.query('~(value==3)', inplace=True)
df.index.name='Index'
df.reset_index(inplace=True)
print(df)

html = df.to_html()
#print(html)

#write html to file
text_file = open('C:\\Users\\Python\\Data\\index.html', "w")
text_file.write(html)
text_file.close()

for s,t in zip(srcattrcols,tgtattrcols):
    print(srcattrcols)

df_final=pd.DataFrame(columns=['EmpId','Name','Component','Amount'])
df_final['EmpId']=101
df_final['Name']='X1'
df_final['Component']='HRA'
df_final['Amount']=1500

print(df_final)
