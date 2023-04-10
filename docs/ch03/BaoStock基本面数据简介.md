## BaoStock 基本面数据简介

BaoStock 除了可以获取技术面数据，还可以获取基本面数据。BaoStock 可以获取的基本面数据主要有季频盈利能力、季频营运能力、季频成长能力、季频偿债能力等。

和技术面类似，BaoStock 通过 API 获取基本面数据。指定入参后，不同的 `BaoStock API` 会根据入参返回相应的数据。返回的数据类型是 `pandas` 的 `DataFrame` 。

**基本面数据入参说明如下：**

- code：股票代码，**sz.+6位数字代码**（0.8.8版本仅支持这一种格式），如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
- year：统计年份，为空时默认当前年；
- quarter：统计季度，可为空，为空时默认取当前季度。不为空时只有4个取值：1，2，3，4。

**基本面数据出参汇总说明如下：**

 **参数分类**   | **参数名称**    | **参数描述**                                 | **算法说明**                                              
----------------|------------------|------------------------------------------|-------------------------------------------------------
 公共参数       | code             | 证券代码                                     |                                                       
 公共参数       | pubDate          | 公司发布财报的日期                                |                                                       
 公共参数       | statDate         | "财报统计的季度的最后一天, 比如2017-03-31, 2017-06-30" |                                                       
 季频盈利能力   | roeAvg           | 净资产收益率(平均)(%)                            | 归属母公司股东净利润/[(期初归属母公司股东的权益+期末归属母公司股东的权益)/2]*100%       
 季频盈利能力   | npMargin         | 销售净利率(%)                                 | 净利润/营业收入*100%                                         
 季频盈利能力   | gpMargin         | 销售毛利率(%)                                 | 毛利/营业收入\*100%=(营业收入-营业成本)/营业收入*100%                    
 季频盈利能力   | netProfit        | 净利润(元)                                   |                                                       
 季频盈利能力   | epsTTM           | 每股收益                                     | 归属母公司股东的净利润TTM/最新总股本                                  
 季频盈利能力   | MBRevenue        | 主营营业收入(元)                                |                                                       
 季频盈利能力   | totalShare       | 总股本                                      |                                                       
 季频盈利能力   | liqaShare        | 流通股本                                     |                                                       
 季频营运能力   | NRTurnRatio      | 应收账款周转率(次)                               | 营业收入/[(期初应收票据及应收账款净额+期末应收票据及应收账款净额)/2]                
 季频营运能力   | NRTurnDays       | 应收账款周转天数(天)                              | 季报天数/应收账款周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)        
 季频营运能力   | INVTurnRatio     | 存货周转率(次)                                 | 营业成本/[(期初存货净额+期末存货净额)/2]                              
 季频营运能力   | INVTurnDays      | 存货周转天数(天)                                | 季报天数/存货周转率(一季报：90天，中报：180天，三季报：270天，年报：360天)          
 季频营运能力   | CATurnRatio      | 流动资产周转率(次)                               | 营业总收入/[(期初流动资产+期末流动资产)/2]                             
 季频营运能力   | AssetTurnRatio   | 总资产周转率                                   | 营业总收入/[(期初资产总额+期末资产总额)/2]                             
 季频成长能力   | YOYEquity        | 净资产同比增长率                                 | (本期净资产-上年同期净资产)/上年同期净资产的绝对值*100%                      
 季频成长能力   | YOYAsset         | 总资产同比增长率                                 | (本期总资产-上年同期总资产)/上年同期总资产的绝对值*100%                      
 季频成长能力   | YOYNI            | 净利润同比增长率                                 | (本期净利润-上年同期净利润)/上年同期净利润的绝对值*100%                      
 季频成长能力   | YOYEPSBasic      | 基本每股收益同比增长率                              | (本期基本每股收益-上年同期基本每股收益)/上年同期基本每股收益的绝对值*100%             
 季频成长能力   | YOYPNI           | 归属母公司股东净利润同比增长率                          | (本期归属母公司股东净利润-上年同期归属母公司股东净利润)/上年同期归属母公司股东净利润的绝对值*100% 
 季频偿债能力   | currentRatio     | 流动比率                                     | 流动资产/流动负债                                             
 季频偿债能力   | quickRatio       | 速动比率                                     | (流动资产-存货净额)/流动负债                                      
 季频偿债能力   | cashRatio        | 现金比率                                     | (货币资金+交易性金融资产)/流动负债                                   
 季频偿债能力   | YOYLiability     | 总负债同比增长率                                 | (本期总负债-上年同期总负债)/上年同期中负债的绝对值*100%                      
 季频偿债能力   | liabilityToAsset | 资产负债率                                    | 负债总额/资产总额                                             
 季频偿债能力   | assetToEquity    | 权益乘数                                     | 资产总额/股东权益总额=1/(1-资产负债率)                               

季频盈利能力是指公司在每个季度内所实现的盈利水平和能力。这通常涉及到一些财务指标和比率，例如每股收益（EPS）、净利润率、毛利润率等等。这些指标可以用来评估公司的经营状况和盈利能力，对投资者来说是非常重要的参考数据之一。通过了解公司的季度盈利能力，投资者可以更好地了解公司的财务状况，从而做出更明智的投资决策。

代码示例如下：

```python
import baostock as bs
import pandas as pd

# 登录 BaoStock 系统
lg = bs.login()

# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 获取600036招商银行季频盈利能力数据
profit_list = []
rs_profit = bs.query_profit_data(code="sh.600036", year=2022, quarter=4)
while (rs_profit.error_code == '0') & rs_profit.next():
    profit_list.append(rs_profit.get_row_data())

# 转换为DataFrame格式
df_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)

# 打印结果
print(df_profit)

# 将结果集输出到csv文件
df_profit.to_csv("D:\\profit_data.csv", encoding="gbk", index=False)

# 退出 BaoStock 系统
bs.logout()
```

结果数据示例如下：

 code      | pubDate    | statDate   | roeAvg   | npMargin | gpMargin | netProfit           | epsTTM   | MBRevenue           | totalShare  | liqaShare   
-----------|------------|------------|----------|----------|----------|---------------------|----------|---------------------|-------------|-------------
 sh.600036 | 2023-03-25 | 2022-12-31 | 0.152986 | 0.404005 |          | 139294000000.000000 | 5.472357 | 344783000000.000000 | 25219845601 | 20628944429 

季频营运能力是指公司在每个季度内所实现的营运能力和效率。这通常涉及到一些财务指标和比率，例如存货周转率、应收账款周转率、总资产周转率等等。这些指标可以用来评估公司的经营状况和营运效率，对投资者来说也是非常重要的参考数据之一。通过了解公司的季度营运能力，投资者可以更好地了解公司的经营状况和盈利潜力，从而做出更明智的投资决策。

代码示例如下：

```python
import baostock as bs
import pandas as pd

# 登录 BaoStock 系统
lg = bs.login()

# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 获取600036招商银行季频营运能力数据
operation_list = []
rs_operation = bs.query_operation_data(code="sh.600036", year=2022, quarter=4)
while (rs_operation.error_code == '0') & rs_operation.next():
    operation_list.append(rs_operation.get_row_data())

# 转换为DataFrame格式
df_operation = pd.DataFrame(operation_list, columns=rs_operation.fields)

# 打印输出
print(df_operation)

# 将结果集输出到csv文件
df_operation.to_csv("D:\\operation_data.csv", encoding="gbk", index=False)

# 退出 BaoStock 系统
bs.logout()
```

结果数据示例如下：

 code      | pubDate    | statDate   | NRTurnRatio | NRTurnDays | INVTurnRatio | INVTurnDays | CATurnRatio | AssetTurnRatio 
-----------|------------|------------|-------------|------------|--------------|-------------|-------------|----------------
 sh.600036 | 2023-03-25 | 2022-12-31 |             |            |              |             |             | 0.035567       

季频成长能力是指公司在每个季度内所实现的成长水平和能力。这通常涉及到一些财务指标和比率，例如营收增长率、净利润增长率、每股收益增长率等等。这些指标可以用来评估公司的成长潜力和未来发展趋势，对投资者来说也是非常重要的参考数据之一。通过了解公司的季度成长能力，投资者可以更好地了解公司的未来发展潜力，从而做出更明智的投资决策。

代码示例如下：

```python
import baostock as bs
import pandas as pd

# 登录 BaoStock 系统
lg = bs.login()

# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 获取600036招商银行季频成长能力数据
growth_list = []
rs_growth = bs.query_growth_data(code="sh.600036", year=2022, quarter=4)
while (rs_growth.error_code == '0') & rs_growth.next():
    growth_list.append(rs_growth.get_row_data())

# 转换为DataFrame格式
df_growth = pd.DataFrame(growth_list, columns=rs_growth.fields)

# 打印输出
print(df_growth)

# 将结果集输出到csv文件
df_growth.to_csv("D:\\growth_data.csv", encoding="gbk", index=False)

# 退出 BaoStock 系统
bs.logout()
```

结果数据示例如下：

 code      | pubDate    | statDate   | YOYEquity | YOYAsset | YOYNI    | YOYEPSBasic | YOYPNI   
-----------|------------|------------|-----------|----------|----------|-------------|----------
 sh.600036 | 2023-03-25 | 2022-12-31 | 0.101029  | 0.096215 | 0.152772 | 0.140998    | 0.150848 

季频偿债能力是指公司在每个季度内所实现的偿债能力和风险。这通常涉及到一些财务指标和比率，例如资产负债比率、流动比率、速动比率、利息保障倍数等等。这些指标可以用来评估公司的偿债能力和财务风险，对投资者来说也是非常重要的参考数据之一。通过了解公司的季度偿债能力，投资者可以更好地了解公司的财务状况和风险情况，从而做出更明智的投资决策。

代码示例如下：

```python
import baostock as bs
import pandas as pd

# 登录 BaoStock 系统
lg = bs.login()

# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 获取600036招商银行季频偿债能力数据
balance_list = []
rs_balance = bs.query_balance_data(code="sh.600036", year=2022, quarter=4)
while (rs_balance.error_code == '0') & rs_balance.next():
    balance_list.append(rs_balance.get_row_data())

# 转换为DataFrame格式
df_balance = pd.DataFrame(balance_list, columns=rs_balance.fields)

# 打印输出
print(df_balance)

# 将结果集输出到csv文件
df_balance.to_csv("D:\\balance_data.csv", encoding="gbk", index=False)

# 退出 BaoStock 系统
bs.logout()
```

结果数据示例如下：

 code      | pubDate    | statDate   | currentRatio | quickRatio | cashRatio | YOYLiability | liabilityToAsset | assetToEquity 
-----------|------------|------------|--------------|------------|-----------|--------------|------------------|---------------
 sh.600036 | 2023-03-25 | 2022-12-31 |              |            |           | 0.095586     | 0.905884         | 10.62514      
