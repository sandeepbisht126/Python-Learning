# -*- coding: utf-8 -*-
"""
Created on Sat May  1 18:49:32 2021

@author: aitsa
"""


lst= [3,14,6,1,4,5,7]
target=8
dict1={}
for i in lst:
    dict1[i]='false'
for i in lst:
    for j in lst:
        if (i!=j and i+j==target and dict1[i]!='true' and dict1[j]!='true'):
            dict1[i]='true'
            dict1[j]='true'
            print(i,'--',j)
            
        