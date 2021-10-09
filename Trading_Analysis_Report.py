# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 23:06:07 2020

@author: Sandeep Bisht
"""

import pandas as pd
import psycopg2
from string import ascii_uppercase
from datetime import datetime

undrly_fnd_query="""
select curr.UNDERLYING_FUND, curr.Common_Ratio as Curr_Common_Ratio, curr.AVG_ALLOCATION as Curr_AVG_ALLOCATION,
prev.Common_Ratio as PREV_Common_Ratio, prev.AVG_ALLOCATION as PREV_AVG_ALLOCATION,
to_char(((curr.AVG_ALLOCATION::float) - (prev.AVG_ALLOCATION::float))::float,'FM999999990.00')as CHANGE_ALLOCATION from
(select UNDERLYING_FUND, cnt||'/'||total Common_Ratio, to_char(AVG_ALLOCATION::float, 'FM999999990.00') AVG_ALLOCATION
from 
  (select UNDERLYING_FUND, count(1) cnt, '1' as joincol, avg(PCNTGE_ALLOCATION) as AVG_ALLOCATION
   from MFUNDERLYINGFUND 
   where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER'))
   and HISTORY_ID = (select max(HISTORY_ID) from MFUNDERLYINGFUND where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER')))
   group by UNDERLYING_FUND) a,
  (select '1' as joincol, count(1) total from REFMUTUALFUND 
   where SUB_CATEGORY in ('FUND_IDENTIFIER') 
   and MF_NAME in (select distinct MF_NAME from MFUNDERLYINGFUND )) tot
 where a.joincol=tot.joincol
 order by cnt desc, AVG_ALLOCATION desc) curr
left join 
(select UNDERLYING_FUND, cnt||' / '||total Common_Ratio, to_char(AVG_ALLOCATION::float, 'FM999999990.00') AVG_ALLOCATION
 from 
  (select UNDERLYING_FUND, count(1) cnt, '1' as joincol, avg(PCNTGE_ALLOCATION) as AVG_ALLOCATION
   from MFUNDERLYINGFUND 
   where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER'))
   and HISTORY_ID = (select max(HISTORY_ID)-1 from MFUNDERLYINGFUND where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER')))
   group by UNDERLYING_FUND) a,
  (select '1' as joincol, count(1) total from REFMUTUALFUND 
   where SUB_CATEGORY in ('FUND_IDENTIFIER') 
   and MF_NAME in (select distinct MF_NAME from MFUNDERLYINGFUND )) tot
 where a.joincol=tot.joincol
order by cnt desc, AVG_ALLOCATION desc) prev
on curr.UNDERLYING_FUND=prev.UNDERLYING_FUND
limit 10
"""

#Query to extract top common underlying funds for each Category
q_small_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Small Cap')
q_mid_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Mid Cap')
q_lar_mid_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Large & Mid Cap')
q_large_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Large Cap')

#Export query result into Dataframes
df1 = pd.read_sql(q_small_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df2 = pd.read_sql(q_mid_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df3 = pd.read_sql(q_lar_mid_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df4 = pd.read_sql(q_large_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))


def write_in_excel(writer,df,sheets,file_name,row,df_title):    
    #skip 2 rows
    print('Preparing report for '+df_title)
    df.to_excel(writer, sheet_name='TopUnderlyingFunds', startrow=row, header=False, index=False)
    
    workbook  = writer.book
    worksheet = writer.sheets['TopUnderlyingFunds']
    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'fg_color': '#87D7AF', #'#ffcccc'
        'border': 1})
    
    #create dictionary for map length of columns 
    #d = dict(zip(range(25), list(ascii_uppercase)))
    #max_len = d[len(df.columns) - 1]
    #dynamically set merged columns in first row
    #title_start=str(row-1)
    #worksheet.merge_range('A'+ title_start +':' + max_len + title_start, df_title)
    worksheet.write(row-2, 0, df_title, header_format)
    
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(row-1, col_num, value, header_format)
        
        column_len = df[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 3
        worksheet.set_column(col_num, col_num, column_len)

    return writer
    
def multiple_dfs(df_list, sheets, file_name, spaces):
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter')  
    row = 2
    dict_df_title={0:'Small Cap',1:'Mid Cap',2:'Large & Mid Cap',3:'Large Cap'}
    for idx,df in enumerate(df_list):
        df_title=dict_df_title[idx]
        #df.to_excel(writer,sheet_name=sheets,startrow=row , startcol=0) 
        writer=write_in_excel(writer,df,sheets,file_name,row,df_title)
        row = row + len(df.index) + spaces + 1
    writer.save()

# list of dataframes
dfs = [df1,df2,df3,df4]
Report_name='Report_MF-Analysis_'+datetime.today().strftime('%Y%m%d')+'.xlsx'
multiple_dfs(dfs, 'TopUnderlyingFunds', Report_name, 2)