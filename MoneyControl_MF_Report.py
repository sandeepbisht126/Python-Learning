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
select  top.UNDERLYING_FUND,
        top.Common_Ratio,
        top.avg_allocation as curr_allocation, 
        coalesce(to_char((((top.avg_allocation-prev.avg_allocation)*100/case when (coalesce(prev.avg_allocation,0))=(0::float) then top.avg_allocation else prev.avg_allocation end)::float)::float, 'FM999999990.00')::float,0) as percntge_change,
        top.reduced_mf,
        top.increased_mf,
        top.newaddedcnt,
        top.newdropcnt,
        prev.avg_allocation as prev_allocation
from
(
 select a.UNDERLYING_FUND, cnt, (cnt||' / '||total) as Common_Ratio, avg_allocation,avg_change,reduced_mf,increased_mf,coalesce(newaddedcnt,0) newaddedcnt,coalesce(newdropedcnt,0) newdropcnt
 from 
  (select UNDERLYING_FUND,count(distinct MF_NAME) cnt,coalesce(to_char(avg(replace(pcntge_allocation,'%','')::float)::float, 'FM999999990.00')::float,0) as avg_allocation,
   to_char(avg(replace(change_1m,'%','')::float)::float, 'FM999999990.00')::float as avg_change, 
   coalesce(sum(case when ((replace(change_1m,'%','')::float) < 0) then 1 end),0) as reduced_mf, coalesce(sum(case when ((replace(change_1m,'%','')::float) > 0) then 1 end),0) as increased_mf,
   '1' as joincol
   from MFFUNDDETAILS 
   where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER'))
   and RECORD_TYPE in ('Existing') and HISTORY_ID = (select max(HISTORY_ID) from MFFUNDDETAILS where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER')))
   group by UNDERLYING_FUND) a
   inner join
  (select '1' as joincol, count(1) total from REFMUTUALFUND 
   where SUB_CATEGORY in ('FUND_IDENTIFIER') and ANALYSIS_IND='Y'
   and MF_NAME in (select distinct MF_NAME from MFFUNDDETAILS )) tot
   on a.joincol=tot.joincol
   left join
   (select UNDERLYING_FUND, count(1) newaddedcnt from MFFUNDDETAILS where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER'))
    and RECORD_TYPE in ('New Added') and HISTORY_ID = (select max(HISTORY_ID) from MFFUNDDETAILS where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER')))
    group by UNDERLYING_FUND) newadd
	on a.UNDERLYING_FUND=newadd.UNDERLYING_FUND
   left join
   (select UNDERLYING_FUND, count(1) newdropedcnt from MFFUNDDETAILS where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER'))
    and RECORD_TYPE in ('Dropped') and HISTORY_ID = (select max(HISTORY_ID) from MFFUNDDETAILS where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER')))
    group by UNDERLYING_FUND) dropd	
   on a.UNDERLYING_FUND=dropd.UNDERLYING_FUND
  where avg_allocation!=0
 order by cnt desc,avg_allocation desc
 limit LIMIT_VAL
) top
left join
(
select a.UNDERLYING_FUND, cnt, cnt||' / '||total Common_Ratio, avg_allocation,avg_change,reduced_mf,increased_mf,coalesce(newaddedcnt,0) newaddedcnt,coalesce(newdropedcnt,0) newdropcnt
from 
  (select UNDERLYING_FUND,count(distinct MF_NAME) cnt,coalesce(to_char(avg(replace(pcntge_allocation,'%','')::float)::float, 'FM999999990.00')::float,0) as avg_allocation,
   to_char(avg(replace(change_1m,'%','')::float)::float, 'FM999999990.00')::float as avg_change, 
   coalesce(sum(case when ((replace(change_1m,'%','')::float) < 0) then 1 end),0) as reduced_mf, coalesce(sum(case when ((replace(change_1m,'%','')::float) > 0) then 1 end),0) as increased_mf,
   '1' as joincol
   from MFFUNDDETAILS 
   where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER'))
   and RECORD_TYPE in ('Existing') and HISTORY_ID = (select max(HISTORY_ID)-1 from MFFUNDDETAILS where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER')))
   group by UNDERLYING_FUND) a
   inner join
  (select '1' as joincol, count(1) total from REFMUTUALFUND 
   where SUB_CATEGORY in ('FUND_IDENTIFIER') and ANALYSIS_IND='Y'
   and MF_NAME in (select distinct MF_NAME from MFFUNDDETAILS )) tot
   on a.joincol=tot.joincol
   left join
   (select UNDERLYING_FUND, count(1) newaddedcnt from MFFUNDDETAILS where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER'))
    and RECORD_TYPE in ('New Added') and HISTORY_ID = (select max(HISTORY_ID)-1 from MFFUNDDETAILS where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER')))
    group by UNDERLYING_FUND) newadd
	on a.UNDERLYING_FUND=newadd.UNDERLYING_FUND
   left join
   (select UNDERLYING_FUND, count(1) newdropedcnt from MFFUNDDETAILS where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER'))
    and RECORD_TYPE in ('Dropped') and HISTORY_ID = (select max(HISTORY_ID)-1 from MFFUNDDETAILS where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND where SUB_CATEGORY in ('FUND_IDENTIFIER')))
    group by UNDERLYING_FUND) dropd	
   on a.UNDERLYING_FUND=dropd.UNDERLYING_FUND
order by cnt desc,avg_allocation desc
) prev
on top.UNDERLYING_FUND=prev.UNDERLYING_FUND
order by top.cnt desc,((top.avg_allocation-prev.avg_allocation)*100/(case when (coalesce(prev.avg_allocation,0))=(0::float) then top.avg_allocation else prev.avg_allocation end));
"""

recentchg_fnd_query="""
select 	MF_NAME,UNDERLYING_FUND,SECTOR,QTY_CHANGE_1M,QUANTITY,CHANGE_1M,PCNTGE_ALLOCATION,VALUEMN,LOW_HOLDING_1Y,HIGH_HOLDING_1Y 
from MFFUNDDETAILS where RECORD_TYPE='RECORD_INDENTIFIER' and HISTORY_ID = (select max(HISTORY_ID) from MFFUNDDETAILS where MF_NAME in (select distinct MF_NAME from REFMUTUALFUND))
ORDER BY UNDERLYING_FUND,MF_NAME,QTY_CHANGE_1M desc
"""

#Query to extract top common underlying funds for each Category
q_small_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Small Cap').replace('LIMIT_VAL','20')
q_mid_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Mid Cap').replace('LIMIT_VAL','20')
q_lar_mid_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Large & Mid Cap').replace('LIMIT_VAL','20')
q_large_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Large Cap').replace('LIMIT_VAL','20')
q_new_added=recentchg_fnd_query.replace('RECORD_INDENTIFIER','New Added').replace('LIMIT_VAL','20')
q_new_dropped=recentchg_fnd_query.replace('RECORD_INDENTIFIER','Dropped').replace('LIMIT_VAL','20')
q_multi_cap=undrly_fnd_query.replace('FUND_IDENTIFIER','Multi Cap').replace('LIMIT_VAL','20')
q_all_cap=undrly_fnd_query.replace('FUND_IDENTIFIER',"Small Cap','Mid Cap','Large & Mid Cap','Large Cap','Multi Cap").replace('LIMIT_VAL','200')

#Export query result into Dataframes
df1 = pd.read_sql(q_small_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df2 = pd.read_sql(q_mid_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df3 = pd.read_sql(q_lar_mid_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df4 = pd.read_sql(q_large_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df5 = pd.read_sql(q_new_added, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df6 = pd.read_sql(q_new_dropped, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df7 = pd.read_sql(q_multi_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))
df8 = pd.read_sql(q_all_cap, con=psycopg2.connect(dbname='postgres', user='postgres', password='admin', host='localhost'))

def color_negative_red(value):
  """
  Colors elements in a dateframe
  green if positive and red if
  negative. Does not color NaN
  values.
  """

  if value < 0:
    color = 'red'
  elif value > 0:
    color = 'green'
  else:
    color = 'black'

  return 'color: %s' % color

'''
def highlight_cols(x):
    for i, v in enumerate(x):
        if ((i==4 and (v*100/(v+x.iloc[5])>40) and x.iloc[3]<0) or (i==3 and x.iloc[3]<0)) :
            color = 'red'
        elif ((i==3 and x.iloc[3]>0)):
            color = 'green'
    return x
'''

def write_in_excel(writer,df,sheets,file_name,row,df_title):    
    #skip 2 rows
    print('Preparing report for '+df_title)    
    if (sheets=='TopUnderlyingFunds'):
        #df.style.applymap(color_negative_red,subset=['avg_change']).to_excel(writer, sheets, startrow=row, header=False, index=False)
        #formatted_df=formatted_df1.style.apply(highlight_cols, axis=None)
        #formatted_df.to_excel(writer, sheets, startrow=row, header=False, index=False)

        df1=df.style.apply(lambda x: ["background-color: red" 
                          if ((i==4 and x.iloc[3]<=0 and ((v+x.iloc[5])>0) and (v*100/(v+x.iloc[5])>50)) 
                              or (i==3 and x.iloc[3]<=0 and ((x.iloc[4]+x.iloc[5])>0) and (x.iloc[4]*100/(x.iloc[4]+x.iloc[5])>50))
                              or (i==5 and x.iloc[3]<=0 and ((v+x.iloc[4])>0) and (x.iloc[4]*100/(v+x.iloc[4])>50))
                              ) 
                          else ("color: red" 
                                if (i==3 and 1>2 and x.iloc[3]<0)
                                else ("background-color: green" 
                                      if ((i==5 and ((v+x.iloc[4])>0) and (v*100/(v+x.iloc[4])>60) and x.iloc[3]>=0) 
                                          or (i==3 and x.iloc[3]>=0 and ((x.iloc[4]+x.iloc[5])>0) and (x.iloc[5]*100/(x.iloc[4]+x.iloc[5])>60))
                                          or (i==4 and x.iloc[3]>=0 and ((v+x.iloc[5])>0) and (x.iloc[5]*100/(v+x.iloc[5])>60))
                                          ) 
                                      else ("background-color: green" 
                                            if (i==3 and v>=0 and (x.iloc[5]==(x.iloc[4]+x.iloc[5]))) 
                                            else ("background-color: orange" 
                                                  if ((i==4 and x.iloc[3]>=0 and ((v+x.iloc[5])>0) and (v*100/(v+x.iloc[5])>50)) 
                                                      or (i==3 and x.iloc[3]>=0 and ((x.iloc[4]+x.iloc[5])>0) and (x.iloc[4]*100/(x.iloc[4]+x.iloc[5])>50))
                                                      or (i==5 and x.iloc[3]>=0 and ((v+x.iloc[4])>0) and (x.iloc[4]*100/(v+x.iloc[4])>50))
                                                      ) 
                                                  else ("background-color: blue" 
                                                      if ((i==5 and x.iloc[3]<0 and ((v+x.iloc[4])>0) and (v*100/(v+x.iloc[4])>60)) 
                                                          or (i==3 and x.iloc[3]<0 and ((x.iloc[4]+x.iloc[5])>0) and (x.iloc[5]*100/(x.iloc[4]+x.iloc[5])>60))
                                                          or (i==4 and x.iloc[3]<0 and ((v+x.iloc[5])>0) and (x.iloc[5]*100/(v+x.iloc[5])>60))
                                                          )
                                                      else ""
                                                      )
                                                  ) 
                                            )
                                      )
                                  )
                              for i, v in enumerate(x)], axis = 1
                           )
                                   
        
        df1.to_excel(writer, sheets, startrow=row, header=False, index=False)
    else:
        df.to_excel(writer, sheets, startrow=row, header=False, index=False)        
    
    workbook  = writer.book
    worksheet = writer.sheets[sheets]
    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'fg_color': '#87D7AF', #'#ffcccc'
        'border': 1})
    
    worksheet.write(row-2, 0, df_title, header_format)
    
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(row-1, col_num, value, header_format)
        
        column_len = df[value].astype(str).str.len().max()
        column_len = max(column_len, len(value)) + 3
        worksheet.set_column(col_num, col_num, column_len)
    return writer
    
def multiple_dfs(writer, df_list, sheets, file_name, dict_df_title, spaces):
    row = 2
    for idx,df in enumerate(df_list):
        df_title=dict_df_title[idx]
        writer=write_in_excel(writer,df,sheets,file_name,row,df_title)
        row = row + len(df.index) + spaces + 1    

# list of dataframes
dfs_fnd = [df1,df2,df3,df4,df7,df8]
df_chng = [df5,df6]
Report_name='Report_MoneyControl_MF-Analysis_'+datetime.today().strftime('%Y%m%d')+'.xlsx'
dict_df_title_fnd={0:'Small Cap',1:'Mid Cap',2:'Large & Mid Cap',3:'Large Cap',4:'Multi Cap',5:'All Cap'}
dict_df_title_chg={0:'New Added Funds',1:'Dropped Funds'}
writer = pd.ExcelWriter(Report_name,engine='xlsxwriter')  
multiple_dfs(writer, dfs_fnd, 'TopUnderlyingFunds', Report_name, dict_df_title_fnd, 2)
multiple_dfs(writer,df_chng, 'RecentChanges', Report_name, dict_df_title_chg, 2)
writer.save()
