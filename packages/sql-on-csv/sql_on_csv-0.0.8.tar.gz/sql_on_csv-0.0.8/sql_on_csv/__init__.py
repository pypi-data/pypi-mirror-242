import pandas as pd
from pandasql import sqldf
from tabulate import tabulate

# from functools import partial
# pip install tabulate
# pip install pandas
# pip install pandasql

# env: locals() or globals()
# variable environment; locals() or globals() in your function
# allows sqldf to access the variables in your python environment
pysqldf = lambda q,env=globals(): sqldf(q, env)

csv_to_df = lambda filepath_or_buffer: pd.read_csv(filepath_or_buffer=filepath_or_buffer,header=0)
print_tab_with_grid = lambda df: print(tabulate(df, headers='keys', tablefmt='grid'))
print_tab = lambda df: print(tabulate(df, headers='keys'))
