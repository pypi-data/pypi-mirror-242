import pandas as pd
from pandasql import sqldf
from tabulate import tabulate

# from functools import partial
# pip install tabulate
# pip install pandas
# pip install pandasql

gbl = globals()

pysqldf = lambda q: sqldf(q, gbl)

csv_to_df = lambda filepath_or_buffer: pd.read_csv(filepath_or_buffer=filepath_or_buffer,header=0)
print_tab_with_grid = lambda df: print(tabulate(df, headers='keys', tablefmt='grid'))
print_tab = lambda df: print(tabulate(df, headers='keys'))

base_dir='/Users/zhongyou/softwares/idea/workbook/scretch/py/p15_distribute_pkg/examples/data'

df1 = csv_to_df(base_dir+'/1.csv')
df2 = csv_to_df(base_dir+'/2.csv')

print_tab(df1)
print_tab(df2)

sql='''
select 
    t1.name
    ,t1.score
    ,t2.score
from df1 as t1 
join df2 as t2
on t1.name=t2.name
'''

comp_df = pysqldf(sql)
print_tab_with_grid(comp_df)