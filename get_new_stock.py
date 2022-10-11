#!/usr/bin/env python3

import requests
import akshare as ak
import numpy as np

def getBonds():
    df = ak.stock_zh_a_new_em()
    not_688 = ~df['代码'].str.startswith('68')
    not_300 = ~df['代码'].str.startswith('30')
    results = df.loc[((not_688 & not_300) & (df['涨跌幅'] > 8)), ['代码', '名称', '换手率', '最新价' , '涨跌幅' ]]
    results['下次涨停价'] = df['最新价'] * 1.1
    print(results)
getBonds()
