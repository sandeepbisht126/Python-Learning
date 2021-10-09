# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 18:17:13 2020

@author: Sandeep Bisht
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import re

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://www.amazon.in/ap/signin?_encoding=UTF8&openid.assoc_handle=inflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%252Fhome%26ref_%3Dnav_AccountFlyout_signout%26signIn%3D1%26useRedirectOnSuccess%3D1')
elem=browser.find_element_by_css_selector('#ap_email')
elem.send_keys('aitsandeep87@gmail.com')
elem.submit()
passw=browser.find_element_by_css_selector('#ap_password')
passw.send_keys('Sandy@871')
passw.submit()

nav=browser.find_element_by_css_selector('#nav-subnav > a:nth-child(3) > span')
nav.click()
nav1=browser.find_element_by_css_selector('#desktop-ysh-remote-recs_CSInclMultiCategoryRepeatPurchaseStrategy_all_single > li > span > span > div.overlay')
nav1.click()
curr_url=browser.current_url
print('Current url is - ', curr_url)
print('------------------------------------------------------')

html=browser.page_source
'''
f=open('amazon_html.txt','w+',encoding='utf-8')
f.write(html)
f.close()
#print(html)
'''
soup = BeautifulSoup(html, 'lxml')
#print(soup)

all_tag=soup.findAll("a",{"class":"a-link-normal"})
print('Length of tag is :', len(all_tag))
product=[]
for tag in all_tag:
    lst=tag.select("div.title-container")
    if len(lst) !=0:
        for i in lst:
            product.append(''.join(i.findAll(text=True)))
print('All Products are -' , len(product))
print(product)            

#links = [i.attrs.get('href') for i in soup.select('a.a-link-normal')]
#browser.quit()
