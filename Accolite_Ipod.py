# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 15:20:34 2021

@author: aitsa
"""

dict1 = {'Brazil':[100,100],'Arg':[50,100]}
lst=['Brazil','Arg']

c='Brazil'
n=50
shipping=400

for i in lst:
    if i!=c:
        rmt_cntry=i

local_amt=dict1[c][0]*n
#print(local_amt)
rmt_amt=dict1[rmt_cntry][0]*n + (shipping*n/10)
#print(rmt_amt)

if local_amt < rmt_amt:
    amt=local_amt
    flag=1
else:
    amt=rmt_amt
    flag=0
    
print(amt)

if flag==1:
    dict1[c][1]=dict1[c][1]-50
else:
    dict1[rmt_cntry][1]=dict1[c][1]-50
    
print(dict1)
    
        
    
    




