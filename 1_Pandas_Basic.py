import pandas as pd
import numpy as np
from pandas import Series, DataFrame

frame = pd.DataFrame(
    [['2010', 'F', 2],
    ['2010', 'F', 1],
    ['2010', 'M', 3],
    ['2012', 'F', 2],
    ['2012', 'M', 4]],
    columns = ['year','sex','id']
    )
print(frame)

frame_group = frame.groupby(['sex','year'])
#frame_group.apply(print)

#frame_group['count']=frame.groupby(['sex','year'])
for i,j in frame.groupby(['sex','year']):
  print(i)
  print(j)

# List can contain heterogenous elements,but it will convert into same datatype 
lst = [1,2,'a',4,5]
print('List is ', lst)

# Array can contain heterogenous elements,but it will convert into same datatype  
arr1=np.array([1,2,'a',4,5])
print('Array is - ', arr1)

arr1=np.array([[1,2,3,4],
               [9,8,7,6]])
print('Array is - ', arr1)
print(arr1.dtype)
arr1=np.array([[1,2,3,4],
               [9,8,'a',6]])
print('Array is - ', arr1)
print(arr1.dtype)

# Dictionary can contain heterogenous elements as key/value
dict1={'1':101,'2':102}
print('Dict is - ', dict1)
dict1={'1':101,'2':102, 3:103,4:'104'}
print('Dict is - ', dict1)
print(dict1['1'])
print(dict1[3])
print(dict1[4])


#Series with list value
ser1=Series([1,2,[4,5,6]], index=[1,2,3])
print('Series is - ', ser1)

#Index
ind1=np.arange(5)
print(ind1)
print(pd.Index(np.arange(5)))

ser1=Series([1,2,[4,5,6]], index=np.arange(3))
print('Series is - ', ser1)