# -*- coding: utf-8 -*-
"""
Created on Sat May  9 12:19:20 2020

@author: Sandeep Bisht
"""

import numpy as np
import matplotlib.pyplot as plt

#1 - meshgrid function
arr1=np.arange(1,11,1).reshape((2,5))
arr2=np.arange(1,13,1).reshape((3,4))
print('array1 is - ', arr1)
print('array2 is - ', arr2)

x,y=np.meshgrid(arr1,arr2)
print('Meshgrid array shape is ', x.shape)
print('x-array is ', x)
print(y.shape)
print('y-array is ', y)
#  resulting both array will be of same shape
# x will always decide the nos of cols in each of the array
# y will always decide the nos of rows in each of the array
z=np.sqrt(x**2+y**2)
print(z)
print(plt.imshow(z,cmap=plt.cm.gray));plt.colorbar()

#2 - randn, arange, empty
print('Random numpy - ')
print(np.random.randn(2,4))
print('empty numpy - ')
print(np.empty((2,4)))
print('Arange numpy - ')
print(np.arange(1,10,1))


#3 - filtering
arr3=np.random.randn(4,5)
print(arr3)
arr3[arr3>0]=2
arr3[arr3<0]=-2
print(arr3)
arr3=np.random.randn(4,5)
print(arr3)
arr_filt=np.where(arr3>0,2,np.where(arr3==0,0,-2))
print(arr_filt)


#4 - functions
print(arr3.shape)
print(np.in1d(arr3,[2,3,4]).reshape(arr3.shape))

## File reading into Numpy array
#arr_file=np.loadtxt('C:\\Users\\Python\\Practise\\sample_file.txt', delimiter=',')
print(arr_file)
      


















