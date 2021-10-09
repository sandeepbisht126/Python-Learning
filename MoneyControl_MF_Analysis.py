# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 12:03:55 2020

@author: Sandeep Bisht
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
from io import StringIO
from keyboard import press
import re
from datetime import datetime


def dbConnect (db_parm, username_parm, host_parm, pw_parm):
    # Parse in connection information
    credentials = {'host': host_parm, 'database': db_parm, 'user': username_parm, 'password': pw_parm}
    conn = psycopg2.connect(**credentials)
    conn.autocommit = True  # auto-commit each entry to the database
    #conn.cursor_factory = RealDictCursor
    cur = conn.cursor()
    print ("Connected Successfully to DB: " + str(db_parm) + "@" + str(host_parm))
    return conn, cur


def load_in_db(df_mfs,mf_nm,max_hist_id,record_type):
    conn, cur = dbConnect('postgres','postgres','localhost','admin')
    output = StringIO()                          # For Python3 use StringIO
    df_mfs.to_csv(output, sep='\t', header=True, index=False)
    output.seek(0) # Required for rewinding the String object
    del_stmnt= "delete from MFFUNDDETAILS where MF_NAME='"+ mf_nm +"' and RECORD_TYPE='"+ record_type +"'  and HISTORY_ID < "+str(max_hist_id)
        
    cur.execute(del_stmnt)
    copy_query = "COPY MFFUNDDETAILS FROM STDOUT csv DELIMITER '\t' NULL ''  ESCAPE '\\' HEADER "  # Replace your table name in place of mem_info
    cur.copy_expert(copy_query, output)
    conn.commit()
    conn.close()
    print('\n Data loaded successfully for '+mf_nm +'!!!\n')


def find_top_funds(mf_nm,browser,table_selector,max_hist_id,record_type):
    html=browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    main_lst=[]
    mytable = browser.find_element_by_css_selector(table_selector)
    row_seq=0
    for row in mytable.find_elements_by_css_selector('tr'):
        temp_lst=[]     
        for seq,cell in enumerate(row.find_elements_by_tag_name('td')):
            cell_value=cell.text
            if (cell_value=='' or cell_value=='No new entrants in the portfolio in the last month'):
                continue
            elif (seq==0):           
                temp_lst.append(mf_nm)                                       #mf anme
                temp_lst.append(row_seq)                                     #sno
                formatted_undrlying_fnd=(re.sub(r"[- #]", '', cell.text, 1))
                temp_lst.append(formatted_undrlying_fnd)                     #underlying fund
            elif (seq==1):   
                temp_lst.append(cell_value)                                   #sector
            elif (seq==2):       
                temp_lst.append(cell_value)                                   #valueMn
            elif (seq==3):       
                temp_lst.append(cell_value)                                   #percentage allocation
            elif (seq==4):       
                temp_lst.append(cell_value)                                   #change in 1M  
            elif (seq==5):                       
                temp_lst.append(cell_value)                                   #high holding in 1Y
            elif (seq==6):       
                temp_lst.append(cell_value)                                   #low holding in 1Y
            elif (seq==7):       
                temp_lst.append(cell_value)                                   #quantity
            elif (seq==8):       
                temp_lst.append(cell_value)                                   #quantity change in 1M
                temp_lst.append('MoneyControl')                              #source name
                temp_lst.append(pd.to_datetime('now'))                       #inserted time
                temp_lst.append(max_hist_id+1)                               #history id 
                temp_lst.append(record_type)                                 #record type 
                main_lst.append(temp_lst)    
        row_seq=row_seq+1
    print(main_lst)
    df_mfs = pd.DataFrame(main_lst, columns=['MF_NAME','SNO','UNDERLYING_FUND','SECTOR','VALUEMN','PCNTGE_ALLOCATION','CHANGE_1M','HIGH_HOLDING_1Y','LOW_HOLDING_1Y','QUANTITY','QTY_CHANGE_1M','SOURCE_NM','INSERTED_DT','HISTORY_ID','RECORD_TYPE'])
    print(df_mfs)                                                   
    # Load into Database - PostGreSQL
    load_in_db(df_mfs,mf_nm,max_hist_id,record_type) 

# Main program starts here
prog_start=datetime.now()
conn, cur = dbConnect('postgres','postgres','localhost','admin')
cur.execute("select count(1) from PROCESSINGSTATUS")
pending_cnt=[int(x[0]) for x in cur.fetchall()]
pending_cnt_val=pending_cnt[0]
if (pending_cnt_val==0):
    cur.execute("insert into PROCESSINGSTATUS select * from REFMUTUALFUND where ANALYSIS_IND='Y' and MF_URL is not null")
else:
    print('\n Re-running from last failure ...')
    
conn, cur = dbConnect('postgres','postgres','localhost','admin')
cur.execute("select distinct MF_NAME, MF_URL from PROCESSINGSTATUS where ANALYSIS_IND='Y' and MF_URL is not null")
results = cur.fetchall()
conn.close()

for i in range(len(results)):
    mf_to_search=''.join(results[i][0])
    mf_url=''.join(results[i][1])
    print('\n Collecting data for '+mf_to_search +'...')
    
    #Launch mutual fund detail holding page
    #browser = webdriver.Chrome(ChromeDriverManager().install())
    options = Options()
    options.headless = True
    #browser = webdriver.Chrome(executable_path=r'C:\Users\aitsa\Downloads\chromedriver_win32\chromedriver.exe',chrome_options=options)
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
    browser.get(mf_url)  
    conn, cur = dbConnect('postgres','postgres','localhost','admin')
    cur.execute("select coalesce(max(HISTORY_ID),0) from MFFUNDDETAILS where MF_NAME='"+ mf_to_search +"'")
    max_id_lst=[int(x[0]) for x in cur.fetchall()]
    max_hist_id=max_id_lst[0]    

    #Find Top underlying funds and load in database      
    table_selector='#equityCompleteHoldingTable'
    find_top_funds(mf_to_search,browser,table_selector,max_hist_id,'Existing')
    
    #Find Recent changes in the underlying funds and load in database  
    print('\n Find the recent changes happened in the MF ... \n')
    print('\n Recently dropped funds \n')
    recent_chng='#port_tab1 > div.nsebsetab > ul > li:nth-child(3) > a'
    elem=browser.find_element_by_css_selector(recent_chng)
    elem.click()    
    table_selector='#equity_tab3 > div:nth-child(4) > table'
    find_top_funds(mf_to_search,browser,table_selector,max_hist_id,'Dropped')
    
    print('\n Recently added funds \n')
    table_selector='#equity_tab3 > div:nth-child(2) > table'
    find_top_funds(mf_to_search,browser,table_selector,max_hist_id,'New Added')
    
    #All processing completed for a given MFund, so deleting entry from processing table
    conn, cur = dbConnect('postgres','postgres','localhost','admin')
    cur.execute("delete from PROCESSINGSTATUS where MF_NAME='"+ mf_to_search +"' and ANALYSIS_IND='Y' and MF_URL is not null")
    conn.close()    
    browser.close()
    
prog_complete=datetime.now()
print('Program started at - ',prog_start)
print('Program completed at - ',prog_complete)
print('Total execution time - ',(prog_complete - prog_start))
