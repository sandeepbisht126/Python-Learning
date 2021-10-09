# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 13:18:35 2020

@author: Sandeep Bisht
"""

Monthly_Principal=15000
tenor=5
interest_rate=[5.45,5.3,5.4,5.5,5.5]
interest=0

for tenr in range(0,tenor):
    print('----Year', (tenr+1), '-----')
    year_interest=0
    factor= 1 + (tenr*4)
    for qtr in range(1,5):
        print('Quarter - ',qtr)
        Cust_deposit=(Monthly_Principal*(factor*3 + (3*(qtr-1))))
        Principal = Cust_deposit + interest
        interest=(Principal*interest_rate[tenr])/(4*100)        
        print(interest)
        year_interest = year_interest + interest
    print('Year', tenr+1,'interest = ',year_interest)        
    print('------------------')    
    