# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 18:17:13 2020

@author: Sandeep Bisht
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://newtrade.sharekhan.com/skweb/trading/report/dashboard')
elem=browser.find_element_by_css_selector('body > div > div.row > div.col-md-5.col-xs-12 > div > loginpage > div > div > div > div > div > div > div.slide.ng-scope > div:nth-child(1) > form > md-input > span > input')
elem.send_keys('pranitanegi23')
elem.submit()
time.sleep(5)
passw=browser.find_element_by_css_selector('body > div > div.row > div.col-md-5.col-xs-12 > div > loginpage > div > div > div > div > div > div > div.slide.ng-scope > div > div:nth-child(1) > div:nth-child(1) > form > md-input > span > input')
passw.send_keys('Sandy@87')
passw.submit()
time.sleep(5)
mf=browser.find_element_by_css_selector('#segmentActive > label:nth-child(2)')
mf.click()
time.sleep(5)
pf=browser.find_element_by_css_selector('body > div:nth-child(3) > div.hidden-sm.hidden-xs > div > nav > ul > li:nth-child(7) > a')
pf.click()
time.sleep(5)

html=browser.page_source
soup = BeautifulSoup(html, 'lxml')
mf_names = soup.select('div', {"class": "col-xs-10 truncate ng-binding"})
mf_name_lst=[]
for mf_name in mf_names:
    str_mf_nm=mf_name.attrs.get('title')
    if str_mf_nm != None:
        mf_name_lst.append(str_mf_nm)
print('\n Mutual Funds list - Total# ',len(mf_name_lst),'\n')    
print(mf_name_lst)  

def find_top_funds(cnt,browser):
    html=browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    mf_nm = soup.select('h4.ng-binding')
    top_fnd = soup.select('td.ng-binding')
    main_lst=[]
    for i in range(30):
        if (i%3)==0:
            temp_lst=[]
            sno=(''.join(top_fnd[i].findAll(text=True)))
            temp_lst.append(mf_nm[0].text)
            temp_lst.append(sno)
        elif (i%3)==1:
            fname=(''.join(top_fnd[i].findAll(text=True)))  
            temp_lst.append(fname)
        else:
            alloc=(''.join(top_fnd[i].findAll(text=True)))
            temp_lst.append(alloc)
            main_lst.append(temp_lst)
                
    df_mfs='df_top_10_fnd'+str(cnt)
    print('\n',mf_seq,'  - \n')
    df_mfs = pd.DataFrame(main_lst, columns=['MUTUAL FUND','SNO','UNDERLYING FUND','%-ALLOCATION'])
    print(df_mfs)
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    time.sleep(5)
    return browser    

cnt=0
#mf_name_lst=['Axis Bluechip Fund - Growth']
for mf_seq in mf_name_lst:
    cnt=cnt+1
    f1_link='body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child(3) > tr > td:nth-child(4) > div'
    
    
    
    
    if (mf_seq=='Aditya Birla Sun Life Corporate Bond Fund - Growth'):
        f1=browser.find_element_by_css_selector('body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child(3) > tr > td:nth-child(4) > div')
        f1.click()
        time.sleep(5)
        f1_fd=browser.find_element_by_css_selector('body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child(3) > tr > td:nth-child(4) > div.popover.ng-scope.ng-isolate-scope.right.popToolTip.fade.in > div.popover-inner > div > div > ul > li:nth-child(7) > a')
        f1_fd.click()
        time.sleep(5)
        f1_fh=browser.find_element_by_css_selector('body > div.modal.fade.ng-scope.ng-isolate-scope.active-modal.in > div > div > fund-detail > div > div.md-padding.green-tab > ul > li:nth-child(3) > a')
        f1_fh.click()
        browser = find_top_funds(cnt,browser)
    elif (mf_seq=='Axis Bluechip Fund - Growth'):
        f1=browser.find_element_by_css_selector('body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child(4) > tr > td:nth-child(4) > div')
        f1.click()
        time.sleep(5)
        f1_fd=browser.find_element_by_css_selector('body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child(4) > tr > td:nth-child(4) > div.popover.ng-scope.ng-isolate-scope.right.popToolTip.fade.in > div.popover-inner > div > div > ul > li:nth-child(7) > a')
        f1_fd.click()
        time.sleep(5)
        f1_fh=browser.find_element_by_css_selector('body > div.modal.fade.ng-scope.ng-isolate-scope.active-modal.in > div > div > fund-detail > div > div.md-padding.green-tab > ul > li:nth-child(3) > a')
        f1_fh.click()
        browser = find_top_funds(cnt,browser)
    elif (mf_seq=='Canara Robeco Emerging Equities - Growth'):
        f1=browser.find_element_by_css_selector('body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child(5) > tr > td:nth-child(4) > div')
        f1.click()
        time.sleep(5)
        f1_fd=browser.find_element_by_css_selector('body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child(5) > tr > td:nth-child(4) > div.popover.ng-scope.ng-isolate-scope.right.popToolTip.fade.in > div.popover-inner > div > div > ul > li:nth-child(7) > a')
        f1_fd.click()
        time.sleep(5)
        f1_fh=browser.find_element_by_css_selector('body > div.modal.fade.ng-scope.ng-isolate-scope.active-modal.in > div > div > fund-detail > div > div.md-padding.green-tab > ul > li:nth-child(3) > a')
        f1_fh.click()
        browser = find_top_funds(cnt,browser)
    elif (mf_seq=='DSP Small Cap Fund - Growth'):
        f1=browser.find_element_by_css_selector('body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child(6) > tr > td:nth-child(4) > div')
        f1.click()
        time.sleep(5)
        f1_fd=browser.find_element_by_css_selector('body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child(6) > tr > td:nth-child(4) > div.popover.ng-scope.ng-isolate-scope.right.popToolTip.fade.in > div.popover-inner > div > div > ul > li:nth-child(7) > a')
        f1_fd.click()
        time.sleep(5)
        f1_fh=browser.find_element_by_css_selector('body > div.modal.fade.ng-scope.ng-isolate-scope.active-modal.in > div > div > fund-detail > div > div.md-padding.green-tab > ul > li:nth-child(3) > a')
        f1_fh.click()
        browser = find_top_funds(cnt,browser)
    elif (mf_seq=='Franklin India Prima Fund - Growth'):
        f1=browser.find_element_by_css_selector('body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child(7) > tr > td:nth-child(4) > div')
        f1.click()
        time.sleep(5)
        f1_fd=browser.find_element_by_css_selector('body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child(7) > tr > td:nth-child(4) > div.popover.ng-scope.ng-isolate-scope.right.popToolTip.fade.in > div.popover-inner > div > div > ul > li:nth-child(7) > a')
        f1_fd.click()
        time.sleep(5)
        f1_fh=browser.find_element_by_css_selector('body > div.modal.fade.ng-scope.ng-isolate-scope.active-modal.in > div > div > fund-detail > div > div.md-padding.green-tab > ul > li:nth-child(3) > a')
        f1_fh.click()
        browser = find_top_funds(cnt,browser)        
    else:
        break





