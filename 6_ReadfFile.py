# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 13:53:52 2020

@author: Sandeep Bisht
"""

import pandas as pd

#1 : read delimited file
df=pd.read_csv('C:\\Users\\Python\\Data\\delimitedfile.txt', sep='|', engine='python')
print('\n Delimited file is as :\n')
print(df)

#2 : read fixed width file

colspec=[(0,1),(1,4),(4,9)]
df=pd.read_fwf('C:\\Users\\Python\\Data\\fixedwidthfile.txt',colspecs=colspec,names=['AcctFirm','AcctOffice','Account'])
print('\n Fixed width file is as :\n')
print(df)

#3 : Split string as per specification

str1='SandeepKumarBisht'
split=[0,7,12,17]
print('\n Split string is as :\n')
[print(str1[split[i]:split[i+1]]) for i in range(len(split)-1)]
