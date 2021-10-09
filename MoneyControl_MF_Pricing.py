# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 17:42:59 2021

@author: aitsa
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

def load_in_db(df_mfs,stock_nm):
    conn, cur = dbConnect('postgres','postgres','localhost','admin')
    output = StringIO()                          # For Python3 use StringIO
    df_mfs.to_csv(output, sep='\t', header=True, index=False)
    output.seek(0) # Required for rewinding the String object    
        
    copy_query = "COPY PRICEDETAILS FROM STDOUT csv DELIMITER '\t' NULL ''  ESCAPE '\\' HEADER "  # Replace your table name in place of mem_info
    cur.copy_expert(copy_query, output)
    #deleting dupes for same pricedate and different inserted_dt
    print('Deleting dupes entries based on same pricedate and different inserted_dt ...')
    del_stmnt= "delete from PRICEDETAILS p1 using PRICEDETAILS p2 where p1.STOCK_NAME ='"+ stock_nm +"' and p1.inserted_dt < p2.inserted_dt and p1.pricedate=p2.pricedate and p1.STOCK_NAME=p2.STOCK_NAME"
    cur.execute(del_stmnt)
    conn.commit()
    conn.close()
    print('\n Data loaded successfully for '+stock_nm +'!!!\n')

def find_price_stocks(stock_nm,browser,table_selector):
    html=browser.page_source
    soup = BeautifulSoup(html, 'lxml')

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
                temp_lst.append(stock_nm)                                     #stock name
                temp_lst.append(cell_value)                                   #price date
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
                continue                                                     #quantity
            elif (seq==7):       
                temp_lst.append('MoneyControl')                              #source name
                temp_lst.append(pd.to_datetime('now'))                       #inserted time
                main_lst.append(temp_lst)  
        row_seq=row_seq+1
    #print(main_lst)
    df_mfs = pd.DataFrame(main_lst, columns=['STOCK_NAME','PRICEDATE','OPENPRICE','HIGHPRICE','LOWPRICE','CLOSEPRICE','VOLUME','SOURCE_NM','INSERTED_DT'])
    print(df_mfs)                                                   
    # Load into Database - PostGreSQL
    load_in_db(df_mfs,stock_nm) 

# Main program starts here
prog_start=datetime.now()
conn, cur = dbConnect('postgres','postgres','localhost','admin')
cur.execute("select count(1) from PRICEPROCESSINGSTATUS where ANALYSIS_IND='Y' and STOCK_SYMBOL is not null")
pending_cnt=[int(x[0]) for x in cur.fetchall()]
pending_cnt_val=pending_cnt[0]
if (pending_cnt_val==0):
    cur.execute("Insert into PRICEPROCESSINGSTATUS select * from REFFUND where ANALYSIS_IND='Y' and STOCK_SYMBOL is not null")
else:
    print('\n Re-running from last failure ...')

conn, cur = dbConnect('postgres','postgres','localhost','admin')
cur.execute("select distinct STOCK_SYMBOL from PRICEPROCESSINGSTATUS where ANALYSIS_IND='Y' and STOCK_SYMBOL is not null")
results = cur.fetchall()
conn.close()

for i in range(len(results)):
    stock_nm=''.join(results[i][0])
    price_url='https://www.moneycontrol.com/stocks/histstock.php?classic=true'
    print('\n Collecting data for '+stock_nm +'...')
    
    #Launch mutual fund detail holding page
    options = Options()
    options.headless = True
    #browser = webdriver.Chrome(executable_path=r'C:\Users\aitsa\Downloads\chromedriver_win32\chromedriver.exe',chrome_options=options)
    browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
    browser.get(price_url)  
    
    search_stock='#mycomp'
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,search_stock)))
    elem=browser.find_element_by_css_selector(search_stock)
    elem.send_keys(stock_nm)
    first_searched='#suggest > ul > li:nth-child(1) > a'
    for attempt in range(2):
        try:            
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,first_searched)))
            elem=browser.find_element_by_css_selector(first_searched)
            elem.click()
        except:
            time.sleep(2)
            first_searched='#suggest > ul > li > a'
            continue
        else:
            break
    conn, cur = dbConnect('postgres','postgres','localhost','admin')
    cur.execute("select case when min(PriceDate) is null then 0 else 1 end as MinPriceDt from PRICEDETAILS where STOCK_NAME='"+ stock_nm +"'")
    min_id_lst=[int(x[0]) for x in cur.fetchall()]
    min_price_id=min_id_lst[0] 
    if (min_price_id==0):
        from_date_val='01'
        from_mnth_val='Jan'
        from_year_val='2021'   # need to check how to automate this
    else:
        print('Pick max date from table for Stock to start loading from --> ',stock_nm)
        cur.execute("select extract(day from max(PriceDate))+1 as Day,to_char(max(PriceDate),'Mon') as Month, extract(year from max(PriceDate)) as year from PRICEDETAILS where STOCK_NAME='"+ stock_nm +"'")
        MaxDate = cur.fetchall()
        from_date_val=str(str(int(MaxDate[0][0])).zfill(2))
        from_mnth_val=MaxDate[0][1]
        from_year_val=str(int(MaxDate[0][2]))
    
    print('Extracting prices for stock - ',stock_nm,' from -- ',from_date_val,'-',from_mnth_val,'-',from_year_val)    
    #Select From date range for price listing
    from_date='#mc_mainWrapper > div.PA10 > div.FL > div.PT15 > div.PT10 > div.brdb > table > tbody > tr > td:nth-child(1) > form > div:nth-child(2) > select:nth-child(1)'
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,from_date)))
    elem=browser.find_element_by_css_selector(from_date)
    elem.send_keys(from_date_val)
    elem.click()  
    from_mnth='#mc_mainWrapper > div.PA10 > div.FL > div.PT15 > div.PT10 > div.brdb > table > tbody > tr > td:nth-child(1) > form > div:nth-child(2) > select:nth-child(2)'
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,from_mnth)))
    elem=browser.find_element_by_css_selector(from_mnth)
    elem.send_keys(from_mnth_val)
    elem.click()  
    from_year='#mc_mainWrapper > div.PA10 > div.FL > div.PT15 > div.PT10 > div.brdb > table > tbody > tr > td:nth-child(1) > form > div:nth-child(2) > select:nth-child(3)'
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,from_year)))
    elem=browser.find_element_by_css_selector(from_year)
    elem.send_keys(from_year_val)
    elem.click() 
    #Select To date range for price listing
    to_date='#mc_mainWrapper > div.PA10 > div.FL > div.PT15 > div.PT10 > div.brdb > table > tbody > tr > td:nth-child(1) > form > div:nth-child(4) > select:nth-child(1)'
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,to_date)))
    elem=browser.find_element_by_css_selector(to_date)
    elem.send_keys('31')
    elem.click()     
    to_mnth='#mc_mainWrapper > div.PA10 > div.FL > div.PT15 > div.PT10 > div.brdb > table > tbody > tr > td:nth-child(1) > form > div:nth-child(4) > select:nth-child(2)'
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,to_mnth)))
    elem=browser.find_element_by_css_selector(to_mnth)
    elem.send_keys('Dec')
    elem.click()    
    submit='#mc_mainWrapper > div.PA10 > div.FL > div.PT15 > div.PT10 > div.brdb > table > tbody > tr > td:nth-child(1) > form > div:nth-child(4) > input[type=image]:nth-child(4)'
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,submit)))
    elem=browser.find_element_by_css_selector(submit)
    elem.click()  
    
    #Find Prices of Stock and load in database      
    table_selector='#mc_mainWrapper > div.PA10 > div.FL > div.PT15 > div.MT12 > table'
    find_price_stocks(stock_nm,browser,table_selector)
    #All processing completed for a given Stock, so deleting entry from processing table
    conn, cur = dbConnect('postgres','postgres','localhost','admin')
    cur.execute("delete from PRICEPROCESSINGSTATUS where STOCK_SYMBOL='"+ stock_nm +"' and ANALYSIS_IND='Y' and STOCK_SYMBOL is not null")
    conn.close() 
    browser.close()
    
prog_complete=datetime.now()
print('Program started at - ',prog_start)
print('Program completed at - ',prog_complete)
print('Total execution time - ',(prog_complete - prog_start))