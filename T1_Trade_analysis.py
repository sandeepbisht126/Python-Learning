# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 18:10:12 2020

@author: Sandeep Bisht
"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import psycopg2
import csv
from io import StringIO
from string import ascii_uppercase
from datetime import datetime
import re

df = pd.DataFrame({'text': ['fooooooo', 'bar'],
                 'number': [1, 2]})

df.style.set_properties(**{'text-align': 'left'})
print(df)

main_lst=[['Aditya Birla Sun Life Corporate Bond Fund - Growth', '1', 'Net Receivables / (Payables)', '2.86'], 
          ['Aditya Birla Sun Life Corporate Bond Fund - Growth', '2', '7.25% Larsen & Toubro Limited (24/04/2023)', '2.68'], 
          ['Aditya Birla Sun Life Corporate Bond Fund - Growth', '3', '7.17% Reliance Industries Limited (08/11/2022)', '2.55'], 
          ['Aditya Birla Sun Life Corporate Bond Fund - Growth', '4', '6.70% National Bank For Agriculture and Rural Development (11/11/2022)', '2.44'],
          ['Aditya Birla Sun Life Corporate Bond Fund - Growth', '5', '8.65% Mahindra & Mahindra Financial Services Limited (19/03/2021)', '2.27'],
          ['Aditya Birla Sun Life Corporate Bond Fund - Growth', '6', '7.35% Power Finance Corporation Limited (15/10/2022)', '2.10'], 
          ['Aditya Birla Sun Life Corporate Bond Fund - Growth', '7', '6.95% Reliance Industries Limited (15/03/2023)', '2.06'], 
          ['Aditya Birla Sun Life Corporate Bond Fund - Growth', '8', '7.24% REC Limited (31/12/2022)', '2.06'], 
          ['Aditya Birla Sun Life Corporate Bond Fund - Growth', '9', '7.00% Housing Development Finance Corporation Limited (19/05/2022)', '2.05'], 
          ['Aditya Birla Sun Life Corporate Bond Fund - Growth', '10', 'Government of India (15/02/2027)', '1.97']] 

#print(main_lst)

df_mfs = pd.DataFrame(main_lst, columns=['MUTUAL_FUND','SNO','UNDERLYING_FUND','PCNTGE_ALLOCATION'])
print(df_mfs)

html='''
<div class="col-xs-10 truncate ng-binding" popover-class="popToolTip" popover-placement="right" uib-popover-template="'popover.html'" popover-trigger="'click outsideClick'" popover-is-open="popoverMenu.open" ng-click="popoverMenuItem.data=h" style="cursor:pointer;padding-left: 0;" title="Aditya Birla Sun Life Corporate Bond Fund - Growth">Aditya Birla Sun Life Corporate Bond Fund - Growth</div>
<div class="col-xs-10 truncate ng-binding" popover-class="popToolTip" popover-placement="right" uib-popover-template="'popover.html'" popover-trigger="'click outsideClick'" popover-is-open="popoverMenu.open" ng-click="popoverMenuItem.data=h" style="cursor:pointer;padding-left: 0;" title="Axis Bluechip Fund - Growth">Axis Bluechip Fund - Growth</div>
<h4 style="color:#f60" class="ng-binding">Aditya Birla Sun Life Corporate Bond Fund - Growth<span class="pull-right" ng-click="cancel()"><i class="fa fa-times"></i></span></h4>
'''

soup = BeautifulSoup(html, 'lxml')
#print(soup)
mf_names = soup.select('div', {"class": "col-xs-10 truncate ng-binding"})

mf_name_lst=[]
for mf_name in mf_names:
    mf_name_lst.append(mf_name.attrs.get('title'))
print('\n Mutual Funds list - \n')    
print(mf_name_lst) 

for i in mf_name_lst:
    print(i)

print('\n --------- \n')
nm = soup.select('h4',{"class":"ng-binding"})
print(nm[0].text)

def print_msg(cnt):
    print('hello',cnt)


for i in range(5):
    df_temp='df_temp'+str(i)
    df_temp=pd.DataFrame(columns= ['c1','c2','c3'])
    print(df_temp)
    cnt=1
    print_msg(cnt)

for mf_seq in range(len(mf_name_lst)):
    f1_link='body > div:nth-child(3) > div.view-animate-container > div > form > div > div > table > tbody:nth-child('+ str(mf_seq+3) +') > tr > td:nth-child(4) > div'
    f1_fd_link=f1_link + '.popover.ng-scope.ng-isolate-scope.right.popToolTip.fade.in > div.popover-inner > div > div > ul > li:nth-child(7) > a'
    f1_fh_link='body > div.modal.fade.ng-scope.ng-isolate-scope.active-modal.in > div > div > fund-detail > div > div.md-padding.green-tab > ul > li:nth-child(3) > a'
    print(f1_link)
    
for attempt in range(10):
    try:
        print('hello')
    except:
        print('Excepttion')
    else:
        break
    
print('\n Database activity test ...\n')    
MF_NM='Aditya Birla Sun Life Corporate Bond Fund - Growth'
conn = psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost', port='5432')
cur=conn.cursor()
cur.execute("select distinct MF_NAME, MF_URL from REFMUTUALFUND where MF_URL is not null;")
#del_stmnt= "delete from df_testTable where MUTUAL_FUND='"+ MF_NM +"'"
#print(del_stmnt)
#cur.execute(del_stmnt)
#conn.commit()
results = cur.fetchall()
#lst=[int(x[0]) for x in cur.fetchall()]
#hst_id=lst[0]
#print(hst_id)
print(results)
conn.close()

for i in range(len(results)):
    print('loop ---')
    #print(results[i][0])
    #print(results[i][1])
    mf_to_search=''.join(results[i][0])
    mf_url=''.join(results[i][1])
    print('MF name is - ',mf_to_search)
    print('MF url is - ',mf_url)

mf_nm='- SJVN Ltd.'
print(re.sub(r"[- #]", '', mf_nm, 1))
mf_nm='# SJVN Ltd.'
print(re.sub(r"[- #]", '', mf_nm, 1))

import pandas as pd
writer = pd.ExcelWriter('TT.xlsx',engine='xlsxwriter')  
df = pd.DataFrame([[2,3,1], [3,2,2], [2,4,4]], columns=list("ABC"))

df.style.apply(lambda x: ["background: red" if v > x.iloc[0] else "" for v in x], axis = 1).to_excel(writer, 'testss', startrow=1, header=False, index=False)
print(df)



'''
print('\n imported data from database -')
for i in range(len(results)):
    print(''.join(results[i]))

date=pd.to_datetime('now')
print(date)

df_mfs['INSERTED_DT']=date


def dbConnect (db_parm, username_parm, host_parm, pw_parm):
    # Parse in connection information
    credentials = {'host': host_parm, 'database': db_parm, 'user': username_parm, 'password': pw_parm}
    conn = psycopg2.connect(**credentials)
    conn.autocommit = True  # auto-commit each entry to the database
    #conn.cursor_factory = RealDictCursor
    cur = conn.cursor()
    print ("Connected Successfully to DB: " + str(db_parm) + "@" + str(host_parm))
    return conn, cur

def load_in_db(df_mfs):
    MF_NM='Aditya Birla Sun Life Corporate Bond Fund - Growth'
    conn, cur = dbConnect('postgres','postgres','localhost','admin')
    output = StringIO() # For Python3 use StringIO
    df_mfs.to_csv(output, sep='\t', header=True, index=False)
    output.seek(0) # Required for rewinding the String object
    del_stmnt= "delete from df_testTable where MUTUAL_FUND='"+ MF_NM +"'"
    cur.execute(del_stmnt)
    copy_query = "COPY df_testTable FROM STDOUT csv DELIMITER '\t' NULL ''  ESCAPE '\\' HEADER "  # Replace your table name in place of mem_info
    cur.copy_expert(copy_query, output)
    conn.commit()
    conn.close()
    print('\n Data loaded successfully for '+MF_NM +'!!!\n')

load_in_db(df_mfs)

print('\n Imported data from table is \n')
undrly_fnd_query="""
select UNDERLYING_FUND, cnt||' / '||total CommonRatio 
from 
  (select UNDERLYING_FUND, count(1) cnt, '1' as joincol from MFUNDERLYINGFUND 
   where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER'))
   group by UNDERLYING_FUND) a,
  (select '1' as joincol, count(1) total from REFMUTUALFUND 
   where SUB_CATEGORY in ('FUND_IDENTIFIER') 
   and MF_NAME in (select distinct MF_NAME from MFUNDERLYINGFUND )) tot
 where a.joincol=tot.joincol
order by cnt desc
limit 5
"""

q_small_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Small Cap')
q_mid_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Mid Cap')
q_lar_mid_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Large & Mid Cap')
q_large_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Large Cap')
print(q_large_cap)

df1 = pd.read_sql(q_small_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df2 = pd.read_sql(q_mid_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df3 = pd.read_sql(q_lar_mid_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df4 = pd.read_sql(q_large_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))


def write_in_excel(writer,df,sheets,file_name,row,df_title):    
    #skip 2 rows
    print(df_title)
    df.to_excel(writer, sheet_name='TopUnderlyingFunds', startrow=row, header=False, index=False)
    
    workbook  = writer.book
    worksheet = writer.sheets['TopUnderlyingFunds']
    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'fg_color': '#ffcccc',
        'border': 1})
    
    #create dictionary for map length of columns 
    d = dict(zip(range(25), list(ascii_uppercase)))
    max_len = d[len(df.columns) - 1]
    print (max_len)
    #dynamically set merged columns in first row
    #title_start=str(row-1)
    #worksheet.merge_range('A'+ title_start +':' + max_len + title_start, df_title)
    worksheet.write(row-2, 0, df_title, header_format)
    
    for col_num, value in enumerate(df.columns.values):
        #write to second row
        print(col_num, value)
        worksheet.write(row-1, col_num, value, header_format)
        
        column_len = df[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 3
        worksheet.set_column(col_num, col_num, column_len)

    # Close the Pandas Excel writer and output the Excel file.
    #writer.save()
    return writer
    
def multiple_dfs(df_list, sheets, file_name, spaces):
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter')  
    row = 2
    dict_df_title={0:'Small Cap',1:'Mid Cap',2:'Large & Mid Cap',3:'Large Cap'}
    for idx,df in enumerate(df_list):
        df_title=dict_df_title[idx]
        #df.to_excel(writer,sheet_name=sheets,startrow=row , startcol=0) 
        #df.to_excel(writer, sheet_name='TopUnderlyingFunds', startrow=row, header=False, index=False)
        writer=write_in_excel(writer,df,sheets,file_name,row,df_title)
        row = row + len(df.index) + spaces + 1
    writer.save()

# list of dataframes
dfs = [df1,df2,df3,df4]
multiple_dfs(dfs, 'TopUnderlyingFunds', 'MF_Analysis.xlsx', 2)
    

Report_name='Report_MF-Analysis_'+datetime.today().strftime('%Y%m%d')+'.xlsx'
print(Report_name)
'''