# -*- coding: utf-8 -*-
"""
Created on Mon May  3 19:02:05 2021

@author: aitsa
"""
import numpy as np

str1='yogi'
print(id(str1),'--',str1)
print(id(str1+'bin'),'--',str1+'bin')

print(list(str1))

#Tuple are Immutable, however if mutable element (like List, Dict etc) are there in it, they can be changed
tup = ([3, 4, 5], 'myname') 
print(tup)
tup[0][0]=1
print(tup)

#Tuple are Immutable, can't be changed
tup=(3,4,5, 'myname') 
tup[0]=1
print(tup)

