# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 21:09:02 2021

@author: aitsa
"""
import hashlib
  
from itertools import permutations
your_list=[1,2,3,4,5,6,7,8,9,0]
#your_list=[1,2,3,4]
lst=[]
cnt=0
for i in permutations(your_list, 8):
    cnt=cnt+1
    str1=''.join([str(elem) for elem in list(i)])
    result = hashlib.md5(str1.encode())
    #print(result.hexdigest(),' -- ',str1) 
    if (result.hexdigest()=="81f76e8f385ce3d87e2eecb55bf8f540"):
        print('81f76e8f385ce3d87e2eecb55bf8f540',' - plaintext value is - ', str1)
    elif (result.hexdigest()=="dd5474d1f304c82e4f188aa296392807"):
        print('dd5474d1f304c82e4f188aa296392807',' - plaintext value is - ', str1)
    elif (result.hexdigest()=="45c88b92c845d135b942d88d304d0264"):
        print('45c88b92c845d135b942d88d304d0264',' - plaintext value is - ', str1)
    elif (cnt%100000==0):
        print('processed count - ',cnt)
    else:
        continue
            
    
