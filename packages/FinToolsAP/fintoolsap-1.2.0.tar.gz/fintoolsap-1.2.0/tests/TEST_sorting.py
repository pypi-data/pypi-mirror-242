import os
import sys
import time
import shutil
import pathlib
import datetime
import functools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas.tseries.offsets

# add source directory to path
sys.path.insert(0, '../src/FinToolsAP/')

import LocalDatabase
import FamaFrench as FF
import _util_funcs


# set printing options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', shutil.get_terminal_size()[0])
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# directory for loacl wrds database
LOCAL_WRDS_DB = pathlib.Path('/home/andrewperry/Documents')

def main():

    DB = LocalDatabase.LocalDatabase(LOCAL_WRDS_DB, 
                                     database_name = 'WRDS')
    df = DB.query_DB(DB.DBP.CCM)

    sorts_df = FF.sort_portfolios(dfin = df, 
                               sorting_funcs = {'me': FF.sort_quintile, 'ffbm': FF.sort_quintile},
                               char_bkpts = {'me': [0.2, 0.4, 0.6, 0.8], 'ffbm': [0.2, 0.4, 0.6, 0.8]} 
                            )
    sorts_df = sorts_df.set_index('date')
    print(sorts_df.head())

    
    ffcsv = pd.read_csv('25_sorts.csv')
    ffcsv.date = pd.to_datetime(ffcsv.date, format = '%Y%m')
    ffcsv.date += pandas.tseries.offsets.MonthEnd(0)
    ffcsv = ffcsv.set_index('date').sort_index()
    ffcsv /= 100

    merged_df = ffcsv.merge(sorts_df, left_index = True, right_index = True)

    fig_ctr = 1
    for i in range(1, 6):
        for j in range(1, 6):
            col_ff = f'me{i}_bm{j}'
            col_me = f'me{i}_ffbm{j}'
            plt.figure(fig_ctr)
            merged_df[[col_ff, col_me]].plot(legend = True)
            print(merged_df[col_ff].corr(merged_df[col_me]))
            plt.legend()
    plt.show()


if __name__ == '__main__':
    main()