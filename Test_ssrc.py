# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 10:30:55 2021

@author: aitsa
"""

import numpy as np
import pandas as pd

'''
lst=[5,9,1,4,7,2,8]
ip=2
len1=len(lst)

temp_lst=[]
rest_lst=[]
for i,x in enumerate(lst):
    if (i<(len1-ip)):
        temp_lst.append(x)
    else:
        rest_lst.append(x)
print(temp_lst)
print(rest_lst)
'''

purchase_df=pd.DataFrame(
    [[1,2,'X1','Y1','Z1',''],
     [1,2,'X2','Y2','Z2',''],
     [3,3,'X3','Y3','Z3',''],
     [4,4,'X4','Y4','Z4','']],
    columns=['trans_id','purchase_Dt','cust_id','product_id','qty','amt']
    )

product_df=pd.DataFrame(
    [[1,2],
     [1,2],
     [3,3],
     [4,4]],
    columns=['product_id','product_name']
    )

print(purchase_df)
print(product_df)






    
    
    
    
