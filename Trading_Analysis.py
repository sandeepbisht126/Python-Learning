# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 18:17:13 2020

@author: Sandeep Bisht
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
from io import StringIO

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://newtrade.sharekhan.com/skweb/trading/report/dashboard')
login='body > div > div.row > div.col-md-5.col-xs-12 > div > loginpage > div > div > div > div > div > div > div.slide.ng-scope > div:nth-child(1) > form > md-input > span > input'
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,login)))
elem=browser.find_element_by_css_selector(login)
elem.send_keys('pranitanegi23')
elem.submit()
#time.sleep(5)
passwd='body > div > div.row > div.col-md-5.col-xs-12 > div > loginpage > div > div > div > div > div > div > div.slide.ng-scope > div > div:nth-child(1) > div:nth-child(1) > form > md-input > span > input'
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,passwd)))
passw=browser.find_element_by_css_selector(passwd)
passw.send_keys('Sandy@87')
passw.submit()
#time.sleep(5)
mfbutton='#segmentActive > label:nth-child(2)'
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,mfbutton)))
mf=browser.find_element_by_css_selector(mfbutton)
mf.click()
#time.sleep(5)
pfbutton='body > div:nth-child(3) > div.hidden-sm.hidden-xs > div > nav > ul > li:nth-child(7) > a'
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,pfbutton)))
pf=browser.find_element_by_css_selector(pfbutton)
pf.click()
time.sleep(3)

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

def dbConnect (db_parm, username_parm, host_parm, pw_parm):
    # Parse in connection information
    credentials = {'host': host_parm, 'database': db_parm, 'user': username_parm, 'password': pw_parm}
    conn = psycopg2.connect(**credentials)
    conn.autocommit = True  # auto-commit each entry to the database
    #conn.cursor_factory = RealDictCursor
    cur = conn.cursor()
    print ("Connected Successfully to DB: " + str(db_parm) + "@" + str(host_parm))
    return conn, cur

def load_in_db(df_mfs,mf_nm):
    conn, cur = dbConnect('postgres','postgres','localhost','admin')
    output = StringIO() # For Python3 use StringIO
    df_mfs.to_csv(output, sep='\t', header=True, index=False)
    output.seek(0) # Required for rewinding the String object
    del_stmnt= "delete from MFUNDERLYINGFUND where MF_NAME='"+ mf_nm +"'"
    cur.execute(del_stmnt)
    copy_query = "COPY MFUNDERLYINGFUND FROM STDOUT csv DELIMITER '\t' NULL ''  ESCAPE '\\' HEADER "  # Replace your table name in place of mem_info
    cur.copy_expert(copy_query, output)
    conn.commit()
    conn.close()
    print('\n Data loaded successfully for '+mf_nm +'!!!\n')

def find_top_funds(cnt,browser):
    html=browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    mf_nm = soup.select('h4.ng-binding')[0].text
    top_fnd = soup.select('td.ng-binding')
    main_lst=[]
    for i in range(30):
        if (i%3)==0:
            temp_lst=[]
            sno=(''.join(top_fnd[i].findAll(text=True)))
            temp_lst.append(mf_nm)
            temp_lst.append(sno)
        elif (i%3)==1:
            fname=(''.join(top_fnd[i].findAll(text=True)))  
            temp_lst.append(fname)
        else:
            alloc=(''.join(top_fnd[i].findAll(text=True)))
            temp_lst.append(alloc)
            temp_lst.append('MY PORTFOLIO')
            temp_lst.append(pd.to_datetime('now'))
            main_lst.append(temp_lst)
                
    df_mfs='df_top_10_fnd'+str(cnt)
    df_mfs = pd.DataFrame(main_lst, columns=['MF_NAME','SNO','UNDERLYING_FUND','PCNTGE_ALLOCATION','SOURCE_NM','INSERTED_DT'])
    
    print(df_mfs)     
    # Load into Database - PostGreSQL
    load_in_db(df_mfs,mf_nm)       
    
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    time.sleep(5)
    return browser    

for mf_seq in range(len(mf_name_lst)):
    f1_link='body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child('+ str(mf_seq+3) +') > tr > td:nth-child(4) > div'
    f1_fd_link=f1_link + '.popover.ng-scope.ng-isolate-scope.right.popToolTip.fade.in > div.popover-inner > div > div > ul > li:nth-child(7) > a'
    f1_fh_link='body > div.modal.fade.ng-scope.ng-isolate-scope.active-modal.in > div > div > fund-detail > div > div.md-padding.green-tab > ul > li:nth-child(3) > a'
    for attempt in range(2):
        try:
            WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR,f1_link)))
            f1=browser.find_element_by_css_selector(f1_link)
            f1.click() 
        except:
            time.sleep(5)
            continue
        else:
            break
    for attempt in range(2):
        try:
            WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR,f1_fd_link)))
            f1_fd=browser.find_element_by_css_selector(f1_fd_link)
            f1_fd.click() 
        except:
            time.sleep(5)
            continue
        else:
            break
    for attempt in range(2):
        try:
            WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR,f1_fh_link)))
            f1_fh=browser.find_element_by_css_selector(f1_fh_link)
            f1_fh.click()
            browser = find_top_funds(mf_seq,browser)
        except:
            time.sleep(5)
            continue
        else:
            break 
        