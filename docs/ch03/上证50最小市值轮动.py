import baostock as bs
import pandas as pd
import datetime as dt
import numpy as np

# bs.login()

#定义一个函数，用于获取沪深300成分股的股票代码
def get_sz50_stocks():
    stock_list = []
    rs = bs.query_sz50_stocks()
    while (rs.error_code == '0') & rs.next():
        stock_list.append(rs.get_row_data())
    return pd.DataFrame(stock_list, columns=rs.fields)

# bs.login()
# print(get_sz50_stocks()['code'])
# print(type(get_sz50_stocks()['code'].values))
# for i in get_sz50_stocks()['code'].values:
#     print(i)
# bs.logout()

#定义一个函数，用于获取股票的市值
def get_stock_market_cap(stock_code, date):
    rs = bs.query_profit_data(code=stock_code,year=date[0:4])
    shares = rs.get_row_data()[-2]
    shares = float(shares)
    rs = bs.query_history_k_data_plus(stock_code, "date,close", date, date)
    row_data = rs.get_row_data()
    if not row_data:
        return None  # or a default market cap value
    close_price = float(row_data[1])
    return shares * close_price

# bs.login()
# print(get_stock_market_cap('sh.600010', '2022-01-04'))
# bs.logout()


#定义一个函数，选择市值最小的n只股票
def select_top_n_stocks(stock_list, date, n):
    stock_market_caps = []
    for stock in stock_list:
        print(stock)
        print(get_stock_market_cap(stock, date))
        stock_market_caps.append(get_stock_market_cap(stock, date))
    print(stock_market_caps)
    top_n_indices = np.argsort(stock_market_caps)[:n]
    return np.array(stock_list)[top_n_indices]

# bs.login()
# tickers = []
# for i in get_sz50_stocks()['code'].values:
#     tickers.append(i)
# print(select_top_n_stocks(tickers, '2022-02-07', 5))
# bs.logout()

def weekly_trade(start_date, end_date):
    # 每周轮动交易策略
    stock_list = get_sz50_stocks()['code'].values
    current_holdings = []
    weekly_portfolio = []
    date_range = pd.date_range(start_date, end_date, freq='W-FRI')
    for date in date_range:
        date_str = date.strftime("%Y-%m-%d")
        new_holdings = select_top_n_stocks(stock_list, date_str, 5)
        sell_holdings = list(set(current_holdings) - set(new_holdings))
        buy_holdings = list(set(new_holdings) - set(current_holdings))
        print('new_holdings',new_holdings)
        print('current_holdings',current_holdings)
        print('sell_holdings',sell_holdings)
        print('buy_holdings',buy_holdings)
        for stock in sell_holdings:
            # 卖出不在新持仓列表的股票
            weekly_portfolio.append((date_str, stock, 'sell'))
        if date == date_range[0]:
            for stock in new_holdings:
                # 买入新持仓列表的股票
                weekly_portfolio.append((date_str, stock, 'buy'))
        else:
            for stock in new_holdings:
                if stock in buy_holdings:
                    # 买入新持仓列表的股票
                    weekly_portfolio.append((date_str, stock, 'buy'))
                else:
                    # 持有原持仓列表的股票
                    weekly_portfolio.append((date_str, stock, 'hold'))
        print(weekly_portfolio)
        current_holdings = list(new_holdings)
    return pd.DataFrame(weekly_portfolio, columns=['date', 'stock', 'action'])

# bs.login()
# start_date = '2022-01-04'
# end_date = '2022-01-20'
# weekly_portfolio = weekly_trade(start_date, end_date)
# print(weekly_portfolio)
# bs.logout()
