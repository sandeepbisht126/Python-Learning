# -*- coding: utf-8 -*-
"""
Created on Mon May  3 08:15:23 2021

@author: aitsa
"""

# find pair of odd and even number in sequence
lst1=[3,2,5,4,1,6]
lst_even=[]
lst_odd=[]
for i in lst1:
    if i%2==0:
        lst_even.append(i)
    else:
        lst_odd.append(i)
print(lst_even)        
print(lst_odd)

final_lst=[]
for o,e in zip(sorted(lst_odd),sorted(lst_even)):
    tmp_lst1=[]
    tmp_lst1.append(o)
    tmp_lst1.append(e)
    final_lst.append(tuple(tmp_lst1))
print(final_lst)
    
# single lonely number
lst1=[1,4,7,3,4,7,1]
dict1={}
for i in lst1:
    if i in dict1.keys():
        dict1[i]='false'
    else:
        dict1[i]='true'
print(dict1)  
for i in dict1:
    if dict1[i]=='true':
        print('Single Lonely number is: ',i)
        
# other approach:
for k,v in enumerate(lst1):
    flag=0
    for k1,v1 in enumerate(lst1):
        if (v == v1 and k!=k1):
            flag=1
    if flag==0:
        print('Single Lonely number is: ',i)
        
tup1=(1,2)
tup2=(3,4)
print(tup1+tup2)
        
        
        
        
        
        
        