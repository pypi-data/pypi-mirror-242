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
