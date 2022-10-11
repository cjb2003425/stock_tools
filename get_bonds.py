#!/usr/bin/env python3

import requests
import akshare as ak
import numpy as np

def getBonds():
    df = ak.bond_cov_comparison()
    options = ['-']
    results = df.loc[(df['转股溢价率'] < -1) & ~(df['转债最新价']).isin(options), ['转债名称', '转债代码', '转股溢价率' , '转债涨跌幅', '正股涨跌幅']]
    if not results.empty:
        print(results)
getBonds()
