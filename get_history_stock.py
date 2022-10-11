#!/usr/bin/env python3

import datetime
import akshare as ak
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import backtrader as bt

symbol_a = '601869'
symbol_h = '06869'
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2022, 10, 10)
df_exchange = ak.stock_sgt_settlement_exchange_rate_szse()
df_e = df_exchange.loc[(df_exchange['适用日期'] > start_date) & (df_exchange['适用日期'] < end_date)].iloc[:,:2]

df_h = ak.stock_hk_hist(symbol=symbol_h, period="daily", start_date=start_date.strftime("%Y-%m-%d"), end_date=end_date.strftime("%Y-%m-%d"), adjust="qfq").iloc[:, :6]
df_a = ak.stock_zh_a_hist(symbol=symbol_a, period="daily", start_date=start_date.strftime("%Y%m%d"), end_date=end_date.strftime("%Y%m%d"), adjust="qfq").iloc[:, :6]
# 处理字段命名，以符合 Backtrader 的要求
df_a.columns = [
    'date',
    'open',
    'close',
    'high',
    'low',
    'volume',
]

df_e.columns = [
   'date',
   'exchange rate',
]

df_h.columns = df_a.columns
df_a.date = pd.to_datetime(df_a.date, infer_datetime_format=True)
df_h.date = pd.to_datetime(df_h.date, infer_datetime_format=True)
df_e.date = pd.to_datetime(df_e.date, infer_datetime_format=True)

merged = pd.merge(df_a, df_h, on='date')
results = pd.merge(merged, df_e, on='date')
results['premium rate'] = (results['close_y'] * results['exchange rate'] - results['close_x']) / results['close_x'] 
results['premium rate(bare)'] = (results['close_y'] - results['close_x']) / results['close_x'] 
results.index = results['date']
lines = results.loc[:, ['premium rate', 'premium rate(bare)']].plot.line()
plt.show()

#class MyStrategy(bt.Strategy):
#    """
#    主策略程序
#    """
#    params = (("maperiod", 20),)  # 全局设定交易策略的参数
#
#    def __init__(self):
#        """
#        初始化函数
#        """
#        self.data_close = self.datas[0].close  # 指定价格序列
#        # 初始化交易指令、买卖价格和手续费
#        self.order = None
#        self.buy_price = None
#        self.buy_comm = None
#        # 添加移动均线指标
#        self.sma = bt.indicators.SimpleMovingAverage(
#            self.datas[0], period=self.params.maperiod
#        )
#
#    def next(self):
#        """
#        执行逻辑
#        """
#        if self.order:  # 检查是否有指令等待执行,
#            return
#        # 检查是否持仓
#        if not self.position:  # 没有持仓
#            if self.data_close[0] > self.sma[0]:  # 执行买入条件判断：收盘价格上涨突破20日均线
#                self.order = self.buy(size=100)  # 执行买入
#        else:
#            if self.data_close[0] < self.sma[0]:  # 执行卖出条件判断：收盘价格跌破20日均线
#                self.order = self.sell(size=100)  # 执行卖出
#
#
#cerebro = bt.Cerebro()  # 初始化回测系统
#start_date = datetime(1991, 4, 3)  # 回测开始时间
#end_date = datetime(2020, 6, 16)  # 回测结束时间
#data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 加载数据
#cerebro.adddata(data)  # 将数据传入回测系统
#cerebro.addstrategy(MyStrategy)  # 将交易策略加载到回测系统中
#start_cash = 1000000
#cerebro.broker.setcash(start_cash)  # 设置初始资本为 100000
#cerebro.broker.setcommission(commission=0.002)  # 设置交易手续费为 0.2%
#cerebro.run()  # 运行回测系统
#
#port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
#pnl = port_value - start_cash  # 盈亏统计
#
#print(f"初始资金: {start_cash}\n回测期间：{start_date.strftime('%Y%m%d')}:{end_date.strftime('%Y%m%d')}")
#print(f"总资金: {round(port_value, 2)}")
#print(f"净收益: {round(pnl, 2)}")
#
#cerebro.plot(style='candlestick')  # 画图

