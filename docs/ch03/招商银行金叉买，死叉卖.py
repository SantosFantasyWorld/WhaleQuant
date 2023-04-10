import baostock as bs
import pandas as pd
import numpy as np
import datetime

# 设定起始时间和结束时间
start_date = '2019-01-01'
end_date = '2022-01-01'

# 登录baostock
lg = bs.login()

# 获取招商银行的历史K线数据
rs = bs.query_history_k_data_plus('sh.600036', 'date,close', start_date=start_date, end_date=end_date,
                                  frequency='d', adjustflag='3')
# print(rs)
data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
# print(data_list)
stock_data = pd.DataFrame(data_list, columns=rs.fields)
stock_data['date'] = pd.to_datetime(stock_data['date'])
stock_data = stock_data.set_index('date')
stock_data['close'] = stock_data['close'].astype(float)
# print(stock_data)

# 计算招商银行的30日均线和60日均线
stock_data['ma30'] = stock_data['close'].rolling(window=30).mean()
stock_data['ma60'] = stock_data['close'].rolling(window=60).mean()
# print(stock_data)

# 计算招商银行的金叉和死叉信号
stock_data['signal'] = np.where(stock_data['ma30'] > stock_data['ma60'], 1, 0)
cond = stock_data.loc[:, 'signal'] == 1
# print('2',stock_data.loc[cond])
stock_data['position'] = stock_data['signal'].diff()
# print(stock_data)

# 打印出stock_data的position列中不为的值
# print(stock_data[stock_data['position'] != 0])

# 计算招商银行的收益率
stock_data['returns'] = stock_data['close'].pct_change()

# 计算招商银行的回测收益率
# 将stock_data中的index大于等于2019-04-02的数据赋值给backtest_data
backtest_data = stock_data[stock_data.index >= datetime.datetime(2019, 4, 2)]
backtest_data.loc[:,'strategy_returns'] = backtest_data.loc[:,'signal'].shift(1) * backtest_data['returns']
# print('1',backtest_data.loc[:,'signal'].shift(1))
backtest_returns = backtest_data.loc[:,'strategy_returns'].dropna()
# print(backtest_data)
# print(backtest_returns)

# 打印回测结果
print("回测收益率为：%.2f%%" % (backtest_returns.sum() * 100))