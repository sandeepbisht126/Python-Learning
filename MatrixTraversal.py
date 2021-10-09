# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 10:44:38 2021

@author: aitsa
"""

r=5
c=5
matrix=[[0 for c in range(c)] for r in range(r)]
print('Original Matrix - \n', matrix)
for i in range(r):
    for j in range(c):
        if (i==0 or j==0):
            matrix[i][j]=1
        else:
            matrix[i][j]=matrix[i-1][j] + matrix[i][j-1]
print(matrix)      
print("Formatted Matrix -")      
for i in range(r):
    temp_lst=[]
    for j in range(c):
        temp_lst.append(matrix[i][j])
    print(temp_lst,"\n")
            