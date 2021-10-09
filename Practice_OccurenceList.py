# -*- coding: utf-8 -*-
"""
Created on Sun May  2 21:17:28 2021

@author: aitsa
"""
import pandas as pd
import numpy as np

lst1= [1,8,3,5]
lst2=[4,1,7,4,3,1,5]

for i in lst1:
    cnt=lst2.count(i)
    print(i,' occurs ',cnt,' times')
    
min1=sorted(lst1)
print('min element in list1 is -',min1[0])    
max1=list(reversed(sorted(lst1)))
print('max element in list1 is -',max1[0])   

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
    print('k is - ',k)
    print('v is - ',v)
