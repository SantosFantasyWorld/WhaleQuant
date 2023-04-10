# 使用时间序列

## Python 和 Pandas 中的日期

我们希望具有类似excel的能力来处理 Pandas 中的日期。  到目前为止，我们已经看到许多在其索引中包含日期的Series和Data frame，例如以下示例：

~~~
import pandas as pd

dates = [
  '2020-01-02', 
  '2020-01-03',
  '2020-01-06',
  '2020-01-07',
  '2020-01-08',
  '2020-01-09',
  '2020-01-10',
  '2020-01-13',
  '2020-01-14',
  '2020-01-15',
  ]

# Close price
prices = [
  7.1600, 
  7.1900,
  7.0000,
  7.1000,
  6.8600,
  6.9500,
  7.0000,
  7.0200,
  7.1100,
  7.0400,
  ]

ser = pd.Series(data=prices, index=dates)
print(ser)

# Output:
#   2020-01-02    7.16
#   2020-01-03    7.19
#   2020-01-06    7.00
#   2020-01-07    7.10
#   2020-01-08    6.86
#   2020-01-09    6.95
#   2020-01-10    7.00
#   2020-01-13    7.02
#   2020-01-14    7.11
#   2020-01-15    7.04
#   dtype: float64
~~~

乍一看，这些索引似乎实际上包含日期。  然而，情况并非如此。  到目前为止，在本课程中，诸如上述的索引由日期的字符串表示组成。  但是，用字符串表示日期不允许我们执行日历类型的操作，例如计算两个日期之间的天数、获取日期部分（日、月或年），或将日期按特定时间段移动。  我们可以通过将日期更改为无效日期来证明这一点。  例如，将上面其中一个日期更改为第十三年的第十三个月的第十三天：'2013-13-13'。  这不是有效日期，但 Pandas 允许您将其用作索引。  就 Pandas 而言，索引标签是字符串，而不是日期。

### 日期时间模块

我们强调表示日期和时间的类，因为日期和时间戳在财务分析中通常都很重要。  这些类是：

- datetime 类，它实现结合了日期和时间功能的对象。

- timedelta 类，用于表示持续时间，或两个日期时间实例之间的差异。

~~~
import datetime as dt 
~~~

#### 日期时间类

将下面的代码复制并粘贴到 lec_pd_datetime.py 文件中：

~~~
import os
import datetime as dt
import pandas as pd
import toolkit_config as cfg

CSVLOC = os.path.join(cfg.DATADIR, 'tsla_prc.csv')
~~~

让我们从 datetime.datetime 类开始（将使用 dt.datetime 访问）。  此类的实例表示日期和时间。  此类有许多方法旨在生成表示特定日期的实例。  这些方法之一是 now，它返回 dt.datetime 的一个实例，该实例表示调用该方法时的日期/时间的快照。

 在lec_pd_datetime.py模块中写入如下语句并运行代码：

~~~
# Instance of `dt.datetime` with the current date/time
dt_now = dt.datetime.now()
# This will produce a string representing the date/time in `dt_now`
print(dt_now)
# This will confirm that `dt_now` is an instance of the `datetime` class
print(type(dt_now)) # --> <class 'datetime.datetime'>
~~~

当我们在 datetime.datetime 的实例上调用 print 函数时，该函数返回实例中包含的数据的表示形式。  例如，假设 dt_now 变量是在 2021 年 8 月 21 日 13:24:27:283311 创建的（即下午 1.24 后 27 秒和 283,311 微秒）。  print(dt_now) 的输出然后变为“2021-08-21 13:24:27.283311”。  从这个表示中，我们可以看到 datetime 的实例存储日期（年、月、日）和时间（小时、分钟、秒、微秒）。

~~~
dt_now.day            # --> 21
dt_now.month          # --> 8
dt_now.year           # --> 2021
dt_now.hour           # --> 13
dt_now.minute         # --> 24
dt_now.second         # --> 27
dt_now.microsecond    # --> 283311
~~~

请注意，这些属性不是函数调用（没有括号）。  我们可以直接从实例访问这些属性。  以下代码使用属性 dt_now.day、dt_now.month 和 dt_now.year。

~~~
s = 'Date in day/month/year format is: {}/{}/{} '.format(dt_now.day, dt_now.month, dt_now.year)
print(s) 

# Output (assuming the Aug 21, 2021 date above):
#   Date in day/month/year format is: 21/8/2021 
~~~

Python 有另一个内置函数 repr，它通常与 print 结合使用。  repr 函数返回实例创建方式的表示（尽管这种行为也可以由类自定义）。  如果没有自定义，此函数将返回一个字符串，其中包含用于生成实例的语句（如果可能）。  这意味着 repr 帮助我们学习如何重构实例。  对于基本类型和其他简单情况，repr 返回创建具有相同数据的实例的命令。

~~~
# String representing the data included in the object
print(dt_now)

# Output:
# 2021-08-21 13:24:27.283311

# This will give you a string representing how the instance could be
# constructed
print(repr(dt_now))

# Output:
#   datetime.datetime(2021, 8, 21, 13, 24, 27, 283311)
~~~

下面的语句创建一个日期/时间为“2021-08-21 13:24:27.283311”的日期时间实例：

~~~
a_little_ago = dt.datetime(
    year=2021, 
    month=8, 
    day=21, 
    hour=13, 
    minute=27, 
    second=1, microsecond=283311)
print(a_little_ago) 

# Output:
# 2021-08-21 13:24:27.283311
~~~

这表明构造函数 dt.datetime（datetime.datetime 的快捷方式）在给定日期和时间参数的情况下生成 datetime.datetime 的实例。我们不需要将所有参数传递给此构造函数，只需传递年、月和日：

~~~
dt_other = dt.datetime(
    year=2021, 
    month=8, 
    day=21, 
    )
print(dt_other) 

# Output:
# 2021-08-21 00:00:00
~~~



### timedelta类

dt.timedelta 的实例表示持续时间或经过的时间。  例如，让我们检查一下如果我们减去两个 datetime 实例会发生什么：

~~~
# Lets create two other datetime instances
dt0 = dt.datetime(year=2019, month=12, day=31) 
dt1 = dt.datetime(year=2020, month=1, day=1) 

# Operations between datetime objects will return timedelta objects
delta = dt1 - dt0

print(delta)
# Output:
# 1 day, 0:00:00

print(repr(delta))
# Output:
# datetime.timedelta(days=1)
~~~

另外一个例子：

~~~
t1 = dt.datetime(year=2020, month=12, day=31, hour=12)
t2 = dt.datetime(year=2020, month=12, day=31, hour=0)

new_delta = t1 - t2
  
print(new_delta) 
# Output:
# 12:00:00
~~~

由于 timedelta 对象表示持续时间，我们可以使用它们来移动 datetime 实例中表示的日期：

~~~
start = dt.datetime(year=2020, month=12, day=31, hour=0)
delta = dt.timedelta(hours=12) 

# This is the new date
end = start + delta 

print(start) 
# Output:
#   2020-12-31 00:00:00

print(end) 
# Output:
#   2020-12-31 12:00:00
~~~

### 格式化日期时间对象

Datetime 对象有一个非常方便的方法，称为 strftime，它允许我们以不同的格式表示日期时间。  在下表中，指令指示我们用来获得所需输出的符号。

~~~
| Directive | Meaning                                                        | Example                  |
|-----------|----------------------------------------------------------------|--------------------------|
| %a        | Weekday as locale's abbreviated name.                          | Sun, Mon, ...            |
| %A        | Weekday as locale's full name.                                 | Sunday, Monday, ...      |
| %w        | Weekday as a decimal number (Sunday=0,Saturday=6)              | 0, 1, .., 6              |
| %d        | Day of the month as a zero-padded decimal number.              | 01, 02, ..., 31          |
| %b        | Month as locale's abbreviated name.                            | Jan, Feb, .., Dec        |
| %B        | Month as locale's full name.                                   | January, February, ...   |
| %m        | Month as a zero-padded decimal number.                         | 01, 02, ..., 12          |
| %y        | Year without century as a zero-padded decimal number.          | 00, 01, ..., 99          |
| %Y        | Year with a century as a decimal number.                       | 0001, 1999, 2013, 2014   |
| %H        | Hour (24-hour clock) as a zero-padded decimal number.          | 00, 01, ..., 23          |
| %I        | Hour (12-hour clock) as a zero-padded decimal number.          | 01, 02, ..., 12          |
| %p        | Locale's equivalent of either am or pm.                        | AM, PM                   |
| %M        | Minute as a zero-padded decimal number.                        | 00, 01, ..., 59          |
| %S        | Second as a zero-padded decimal number.                        | 00, 01, ..., 59          |
| %j        | Day of the year as a zero-padded decimal number.               | 001, 002, ..., 366       |
| %U        | Week number of the year (Sunday as the first day of the week). | 00, 01, ..., 53          |
| %W        | Week number of the year (Monday as the first day of the week). | 00, 01, ..., 53          |
| %c        | Locale's appropriate date and time representation.             | Tue Aug 16 21:30:00 1988 |
~~~

例如

~~~
# Create a datatime object
date = dt.datetime(year=2020, month=12, day=31, hour=0)

# Create a string with the representation we want:
s = date.strftime('%Y-%m-%d')
print(s)

# Output: 
#  '2020-12-31' 
~~~



## Pandas 中的时间序列功能

我们已经讨论了如何使用 Pandas read_csv 方法将 CSV 加载到data frame中。  在 lec_pd_datetime.py 文件的以下部分中，我们将此文件的内容加载到data frame中（不设置索引）：

~~~
prc = pd.read_csv(CSVLOC) 
print(prc) 

# Output:
#             Date        Open        High  ...       Close   Adj Close    Volume
# 0     2010-06-29    3.800000    5.000000  ...    4.778000    4.778000  93831500
# 1     2010-06-30    5.158000    6.084000  ...    4.766000    4.766000  85935500
# 2     2010-07-01    5.000000    5.184000  ...    4.392000    4.392000  41094000
# 3     2010-07-02    4.600000    4.620000  ...    3.840000    3.840000  25699000
# 4     2010-07-06    4.000000    4.000000  ...    3.222000    3.222000  34334500
# ...          ...         ...         ...  ...         ...         ...       ...
# 2640  2020-12-22  648.000000  649.880005  ...  640.340027  640.340027  51716000
# 2641  2020-12-23  632.200012  651.500000  ...  645.979980  645.979980  33173000
# 2642  2020-12-24  642.989990  666.090027  ...  661.770020  661.770020  22865600
# 2643  2020-12-28  674.510010  681.400024  ...  663.690002  663.690002  32278600
# 2644  2020-12-29  661.000000  669.900024  ...  665.989990  665.989990  22910800
# 
# [2645 rows x 7 columns]

prc.info() 

# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 2645 entries, 0 to 2644
# Data columns (total 7 columns):
#  #   Column     Non-Null Count  Dtype  
# ---  ------     --------------  -----  
#  0   Date       2645 non-null   object 
#  1   Open       2645 non-null   float64
#  2   High       2645 non-null   float64
#  3   Low        2645 non-null   float64
#  4   Close      2645 non-null   float64
#  5   Adj Close  2645 non-null   float64
#  6   Volume     2645 non-null   int64  
# dtypes: float64(5), int64(1), object(1)
~~~

检查数据显示，包含日期 (Date) 的列的数据类型是object，这是 Pandas 用于字符串的数据类型。

~~~
# 'Date' is a column of strings with dates.
print(prc.loc[:, 'Date'])

# Output:
# 0       2010-06-29
# 1       2010-06-30
# 2       2010-07-01
# 3       2010-07-02
# 4       2010-07-06
#            ...    
# 2640    2020-12-22
# 2641    2020-12-23
# 2642    2020-12-24
# 2643    2020-12-28
# 2644    2020-12-29
# Name: Date, Length: 2645, dtype: object

# The index is just a counter
print(prc.index) 

# Output:
# RangeIndex(start=0, stop=2645, step=1)
~~~

当我们使用 read_csv 方法时，Pandas 会自动创建一种特殊类型的索引，称为 RangeIndex。  出于我们的目的，它的行为与将位置作为行标签的普通索引完全一样。

我们的下一步是为 prc 数据框设置一个新索引。  我们希望此索引包含“日期”列中的日期。  但是我们不希望这个索引中的标签是代表日期的字符串。  相反，我们想创建另一种更适合时间序列分析的索引：DatetimeIndex。

#### 将字符串转换为日期时间

我们使用 Pandas 方法 to_datetime，该方法用于将参数转换为日期时间值的系列或索引。  to_datetime 方法返回的对象取决于输入的类型：

- 列表或类似的返回 DatetimeIndex

- 系列返回具有日期时间数据类型的系列

- 标量返回时间戳

~~~
# prc['Date'] is a series
dser = pd.to_datetime(prc['Date'], format='%Y-%m-%d')
print(dser)

# Output:
# 0      2010-06-29
# 1      2010-06-30
# 2      2010-07-01
# 3      2010-07-02
# 4      2010-07-06
#           ...    
# 2640   2020-12-22
# 2641   2020-12-23
# 2642   2020-12-24
# 2643   2020-12-28
# 2644   2020-12-29
# Name: Date, Length: 2645, dtype: datetime64[ns]


# prc['Date'].array is a pandas array
didx = pd.to_datetime(prc['Date'].array, format='%Y-%m-%d')
print(didx)

# Output:
# DatetimeIndex(['2010-06-29', '2010-06-30', '2010-07-01', '2010-07-02',
#                '2010-07-06', '2010-07-07', '2010-07-08', '2010-07-09',
#                '2010-07-12', '2010-07-13',
#                ...
#                '2020-12-15', '2020-12-16', '2020-12-17', '2020-12-18',
#                '2020-12-21', '2020-12-22', '2020-12-23', '2020-12-24',
#                '2020-12-28', '2020-12-29'],
#               dtype='datetime64[ns]', length=2645, freq=None)
~~~

可以看出，to_datetime 方法接受一些可选参数。  format 参数允许我们指定日期格式。  如果您知道格式，声明它也无妨；  不然Pandas 会尝试从表示日期的字符串中推断日期。

我们使用 to_datetime 方法将 prc['Date'] 的元素从字符串表示形式转换为日期时间对象。

~~~
# Convert the elements in the Date column
prc.loc[:, 'Date'] = pd.to_datetime(prc['Date'], format='%Y-%m-%d')
prc.info()

# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 2645 entries, 0 to 2644
# Data columns (total 7 columns):
#  #   Column     Non-Null Count  Dtype         
# ---  ------     --------------  -----         
#  0   Date       2645 non-null   datetime64[ns]
#  1   Open       2645 non-null   float64       
#  2   High       2645 non-null   float64       
#  3   Low        2645 non-null   float64       
#  4   Close      2645 non-null   float64       
#  5   Adj Close  2645 non-null   float64       
#  6   Volume     2645 non-null   int64         
# dtypes: datetime64[ns](1), float64(5), int64(1)
~~~

现在，我们需要将默认的 RangeIndex 替换为包含 Date 列中日期的 DatetimeIndex。  Pandas 提供了一种将数据框列转换为索引的便捷方法。  此方法称为 set_index。

~~~
# Using the .set_index method 
prc.set_index('Date') 
prc.info() 

# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 2645 entries, 0 to 2644
# Data columns (total 7 columns):
#  #   Column     Non-Null Count  Dtype         
# ---  ------     --------------  -----         
#  0   Date       2645 non-null   datetime64[ns]
#  1   Open       2645 non-null   float64       
#  2   High       2645 non-null   float64       
#  3   Low        2645 non-null   float64       
#  4   Close      2645 non-null   float64       
#  5   Adj Close  2645 non-null   float64       
#  6   Volume     2645 non-null   int64         
# dtypes: datetime64[ns](1), float64(5), int64(1)
~~~

如您所见，没有发生任何事情，因为 set_index 方法返回一个数据框作为结果，而不是就地更改原始数据框。  要解决此问题，请将 set_index 方法调用的结果分配给一个新变量：

~~~
# Using the .set_index method 
another_df = prc.set_index('Date')
another_df.info()

# <class 'pandas.core.frame.DataFrame'>
# DatetimeIndex: 2645 entries, 2010-06-29 to 2020-12-29
# Data columns (total 6 columns):
#  #   Column     Non-Null Count  Dtype  
# ---  ------     --------------  -----  
#  0   Open       2645 non-null   float64
#  1   High       2645 non-null   float64
#  2   Low        2645 non-null   float64
#  3   Close      2645 non-null   float64
#  4   Adj Close  2645 non-null   float64
#  5   Volume     2645 non-null   int64  
~~~

您要么必须将结果分配给具有相同名称的变量（以覆盖它），要么最好使用 inplace 参数（如果可用）：

~~~
# prc = prc.set_index('Date') or use the `inplace` argument:
# (recommended)
prc.set_index('Date', inplace=True)
prc.info()

# <class 'pandas.core.frame.DataFrame'>
# DatetimeIndex: 2645 entries, 2010-06-29 to 2020-12-29
# Data columns (total 6 columns):
#  #   Column     Non-Null Count  Dtype  
# ---  ------     --------------  -----  
#  0   Open       2645 non-null   float64
#  1   High       2645 non-null   float64
#  2   Low        2645 non-null   float64
#  3   Close      2645 non-null   float64
#  4   Adj Close  2645 non-null   float64
#  5   Volume     2645 non-null   int64  
# dtypes: float64(5), int64(1)
# memory usage: 144.6 KB

# Check the new index
print(prc.index)
~~~

从包含日期作为索引的 CSV 文件中读取数据是一种常见的操作，因此 Pandas 允许您将上面的最后两个步骤组合到 read_csv 操作中。

~~~
# previously:
# prc = pd.read_csv(CSVLOC)

# New version
prc = pd.read_csv(CSVLOC, parse_dates=['Date'], index_col='Date') 
prc.info()

# <class 'pandas.core.frame.DataFrame'>
# DatetimeIndex: 2645 entries, 2010-06-29 to 2020-12-29
# Data columns (total 6 columns):
#  #   Column     Non-Null Count  Dtype  
# ---  ------     --------------  -----  
#  0   Open       2645 non-null   float64
#  1   High       2645 non-null   float64
#  2   Low        2645 non-null   float64
#  3   Close      2645 non-null   float64
#  4   Adj Close  2645 non-null   float64
#  5   Volume     2645 non-null   int64  
# dtypes: float64(5), int64(1)
# memory usage: 144.6 KB
~~~

#### 日期时间索引的优点

现在我们知道如何创建包含 DatetimeIndex 的 Pandas 数据框，让我们看看为什么要这样做。  使用 DatetimeIndex 有很多优点，包括：

- 选择日期范围的便捷方式

- 重采样、变频

- 缺少观测值的“完成”时间序列

- 选择超前、滞后的简单方法（例如计算回报时）

- 计算“滚动”统计数据

- 使用自定义日历、假期

- 轻松转换为期间指数（使用 PeriodIndex）

- 时区之间的转换

- 及时向后或向前移动数据（使用 .shift 方法）

- 处理重复项

我们会在继续使用 Pandas 的过程中说明这些好处。  现在，尝试 DatetimeIndex 为选择数据提供的一些不错、方便的方法：

~~~
# Select all data for a given year in one go
print(prc.loc['2020'])

# [251 rows x 6 columns]

# Select all data for a given month
print(prc.loc['2020-01'])


# Selecting date ranges using strings
print(prc.loc['2020-01-01':'2020-01-05'])
~~~

#### 计算回报

得益于数据框方法 pct_change，从股价数据计算特斯拉的回报非常简单。

~~~
# Make sure the dataframe is sorted
prc.sort_index(inplace=True)

# compute returns
rets = prc.loc[:, 'Close'].pct_change()
print(rets)


# Output:
# Date
# 2010-06-29         NaN
# 2010-06-30   -0.002512
# 2010-07-01   -0.078472
# 2010-07-02   -0.125683
# 2010-07-06   -0.160938
#                 ...   
# 2020-12-22   -0.014649
# 2020-12-23    0.008808
# 2020-12-24    0.024444
# 2020-12-28    0.002901
# 2020-12-29    0.003465
# Name: Close, Length: 2645, dtype: float64
~~~

