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


import csv
from io import StringIO
from keyboard import press

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://newtrade.sharekhan.com/skweb/trading/report/dashboard')
login='body > div > div.row > div.col-md-5.col-xs-12 > div > loginpage > div > div > div > div > div > div > div.slide.ng-scope > div:nth-child(1) > form > md-input > span > input'
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,login)))
elem=browser.find_element_by_css_selector(login)
elem.send_keys('pranitanegi23')
elem.submit()
passwd='body > div > div.row > div.col-md-5.col-xs-12 > div > loginpage > div > div > div > div > div > div > div.slide.ng-scope > div > div:nth-child(1) > div:nth-child(1) > form > md-input > span > input'
WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,passwd)))
elem=browser.find_element_by_css_selector(passwd)
elem.send_keys('Sandy@87')
elem.submit()


def dbConnect (db_parm, username_parm, host_parm, pw_parm):
    # Parse in connection information
    credentials = {'host': host_parm, 'database': db_parm, 'user': username_parm, 'password': pw_parm}
    conn = psycopg2.connect(**credentials)
    conn.autocommit = True  # auto-commit each entry to the database
    #conn.cursor_factory = RealDictCursor
    cur = conn.cursor()
    print ("Connected Successfully to DB: " + str(db_parm) + "@" + str(host_parm))
    return conn, cur


def load_in_db(df_mfs,mf_nm,max_hist_id):
    conn, cur = dbConnect('postgres','postgres','localhost','admin')
    output = StringIO() # For Python3 use StringIO
    df_mfs.to_csv(output, sep='\t', header=True, index=False)
    output.seek(0) # Required for rewinding the String object
    del_stmnt= "delete from MFUNDERLYINGFUND where MF_NAME='"+ mf_nm +"' and HISTORY_ID < "+str(max_hist_id)
        
    cur.execute(del_stmnt)
    copy_query = "COPY MFUNDERLYINGFUND FROM STDOUT csv DELIMITER '\t' NULL ''  ESCAPE '\\' HEADER "  # Replace your table name in place of mem_info
    cur.copy_expert(copy_query, output)
    conn.commit()
    conn.close()
    print('\n Data loaded successfully for '+mf_nm +'!!!\n')

def find_top_funds(mf_nm):
    time.sleep(5)
    conn, cur = dbConnect('postgres','postgres','localhost','admin')
    cur.execute("select coalesce(max(HISTORY_ID),0) from MFUNDERLYINGFUND where MF_NAME='"+ mf_nm +"'")
    max_id_lst=[int(x[0]) for x in cur.fetchall()]
    max_hist_id=max_id_lst[0]
    html=browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    #mf_nm = soup.select('h4.ng-binding')[0].text
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
            temp_lst.append('REFMUTUALFUND')
            temp_lst.append(pd.to_datetime('now'))
            temp_lst.append(max_hist_id+1)
            main_lst.append(temp_lst)
                
    df_mfs = pd.DataFrame(main_lst, columns=['MF_NAME','SNO','UNDERLYING_FUND','PCNTGE_ALLOCATION','SOURCE_NM','INSERTED_DT','HISTORY_ID'])
    
    print(df_mfs)     
    # Load into Database - PostGreSQL
    load_in_db(df_mfs,mf_nm,max_hist_id) 
    
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    time.sleep(5)
    

conn, cur = dbConnect('postgres','postgres','localhost','admin')
cur.execute("select distinct MF_NAME from REFMUTUALFUND where ANALYSIS_IND='Y'")
results = cur.fetchall()
conn.close()

for i in range(len(results)):
    mf_to_search=(''.join(results[i]))
    print('\n Collecting data for '+mf_to_search +'...')
    exit_cd=1
    #step 1 - clear & search the desired MF
    for attempt in range(2):
        try:
            search='#site-search'
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,search)))
            elem=browser.find_element_by_css_selector(search)
            elem.clear()
            elem.send_keys(mf_to_search)
            press('enter')
            exit_cd=0
        except:
            time.sleep(5)
            continue
        else:
            break
    
    if exit_cd==1:
        print('\n Failed in step 1 \n')

        exit(1)
    else:
        exit_cd=1
                
    # step 2 - click on searched MF to get its details
    for attempt in range(2):
        try:
            press('enter')
            click_on_search='#smart-search-list- > div > span.col-md-4 > span.companyName.col-md-10.ng-binding'
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,click_on_search)))
            elem=browser.find_element_by_css_selector(click_on_search)
            elem.click()
            exit_cd=0
        except:
            time.sleep(5)
            continue
        else:
            break
        
    if exit_cd==1:
        print('\n Failed in step 2 \n')
        exit(1)
    else:
        exit_cd=1

    # step 3 - click on Fund Detail tab to fetch underlying detail
    for attempt in range(2):
        try:
            fh_link='body > div.modal.fade.ng-scope.ng-isolate-scope.active-modal.in > div > div > fund-detail > div > div.md-padding.green-tab > ul > li:nth-child(3) > a'
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,fh_link)))
            elem=browser.find_element_by_css_selector(fh_link)
            elem.click()
            exit_cd=0
        except:
            time.sleep(5)
            
            continue
        else:
            break
        
    if exit_cd==1:
        print('\n Failed in step 3 \n')
        exit(1)
    else:
        exit_cd=1

    #Find Top underlying funds and load in database   
    find_top_funds(mf_to_search)
