# 用 Pandas 做更多事情

## 组合 Pandas 对象：代数运算符

将下面的代码复制并粘贴到 lec_pd_joins.py 文件中：

~~~
import pandas as pd

# ---------------------------------------------------------------------------- 
#   The dates and prices lists
# ---------------------------------------------------------------------------- 
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

# Trading day counter
bday = [
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10]
~~~

我们会定义了一个Series(ser) 和一个dataframe (df)。  我们将使用两者作为如何组合不同 Pandas 对象的示例。

~~~
# Series with prices
ser = pd.Series(data=prices, index=dates)
# Data Frame with close and bday columns
df = pd.DataFrame({'close': ser, 'bday': bday}) 
~~~

Python 中的运算符取决于所使用的对象。  例如，+ 运算符的工作方式因操作数而异：

~~~
# Simple sums with integers 
print(1 + 1)              # --> 2 

# String concatenation 
print('1' + '1')          # --> '11' 

# List concatenation 
print([1] + [2, 3])       # --> [1, 2, 3] 
~~~

但是 + 运算符如何与系列一起使用？  我们将讨论以下情况：

     ser + 标量
    
     ser1 + ser2
    
     df1 + df2
    
     df1 + ser1
    
     df + 标量

 此讨论很容易推广到其他运算符，如 -、* 等...

将标量添加到系列或数据框会将标量值添加到数据结构中的所有元素，只要有可能。  例如，如果我们将 1 添加到我们的序列 ser 中，我们将得到一个新序列，其中每个元素都增加 1：

~~~
# Adding an integer to a series of floats
new_ser = ser + 1
print(new_ser)

# Output:
#  2020-01-02    8.16
#  2020-01-03    8.19
#  2020-01-06    8.00
#  2020-01-07    8.10
#  2020-01-08    7.86
#  2020-01-09    7.95
#  2020-01-10    8.00
#  2020-01-13    8.02
#  2020-01-14    8.11
#  2020-01-15    8.04
#  dtype: float64
~~~

但是，如果没有解析数据类型的逻辑方法会怎样？  Pandas 会抛出异常。

~~~
# Adding a string to a series of floats 
new_ser =  ser + '1'     # --> raises an exception
~~~

发生这种情况是因为 pandas 不知道如何将 ser 中的数值与字符串“1”相加。  但是，Pandas 能够将字符串 '1' 添加到值也是字符串的系列中：

~~~
s0 = pd.Series (['1', '2', '3']) 
s1 = s0 + '1' 
print(s1) 

# Output:
#  0    11 
#  1    21 
#  2    31 
#  dtype: object 
~~~

当我们将两个系列加在一起时会发生什么？  这将取决于这两个系列的指数如何相互比较。

考虑两个假设的Series，s1 和 s2。

因此，对于任何 s1 和 s2，存在三种可能性：

-  这两个Series具有相同的索引（即相同的标签）：

​			所以 s1.index.values 与 s2.index.values 相同。

​			当然，这意味着两个索引标签的并集与两个索引标签的交集相同。

- 这两个Series有不同的索引，但它们有一些共同的标签。

 			这意味着 s1.index.values 和 s2.index.values 的交集不为空。

- 这两个Series有不同的索引，没有共同的标签。

​		 	这意味着 s1.index.values 和 s2.index.values 的交集不为空。

为什么这很重要？  这是因为，直觉上，我们可以将 s1 + s2 之类的操作表示为一系列步骤：

1. 创建一个系列 s3，其索引包含 s1.index 和 s2.index 的并集，其中元素值均为 NaN。  这将包括 s1.index 或 s2.index 中的任何索引标签。
2. 选择 s1.index 和 s2.index 的交集。  这些是 s1.index 和 s2.index 中的索引标签。
3. 对于索引标签交叉点的选择：
   - 将所需操作应用于 s1 和 s2 中的相应元素
   - 用这个结果替换 s3 中的 NaN 元素

~~~
print(ser)
# Output:
#  2020-01-02    7.16
#  2020-01-03    7.19
#  2020-01-06    7.00
#  2020-01-07    7.10
#  2020-01-08    6.86
#  2020-01-09    6.95
#  2020-01-10    7.00
#  2020-01-13    7.02
#  2020-01-14    7.11
#  2020-01-15    7.04
#  dtype: float64


# Summing two series with the same index
# (obviously, adding a series to itself will do that...)
print(ser + ser)

# Output:
#  2020-01-02    14.32
#  2020-01-03    14.38
#  2020-01-06    14.00
#  2020-01-07    14.20
#  2020-01-08    13.72
#  2020-01-09    13.90
#  2020-01-10    14.00
#  2020-01-13    14.04
#  2020-01-14    14.22
#  2020-01-15    14.08
#  dtype: float64
~~~

下一种情况是两个系列没有相同的索引。  让我们将 ser 加到另一个不包含标签“2020-01-15”的系列：

~~~
print(ser + ser[:-1])

# Output:
#  2020-01-02    14.32
#  2020-01-03    14.38
#  2020-01-06    14.00
#  2020-01-07    14.20
#  2020-01-08    13.72
#  2020-01-09    13.90
#  2020-01-10    14.00
#  2020-01-13    14.04
#  2020-01-14    14.22
#  2020-01-15      NaN
#  dtype: float64
~~~

最后一种情况涉及没有共同索引标签的系列：

~~~
# Create another series
s2 = pd.Series([1,2], index=['2900-01-01', '2900-01-02'])

print(s2)
# Output:
#   2900-01-01    1
#   2900-01-02    2
#   dtype: int64

print(ser + s2)

# Output:
#  2020-01-02   NaN
#  2020-01-03   NaN
#  2020-01-06   NaN
#  2020-01-07   NaN
#  2020-01-08   NaN
#  2020-01-09   NaN
#  2020-01-10   NaN
#  2020-01-13   NaN
#  2020-01-14   NaN
#  2020-01-15   NaN
#  2900-01-01   NaN
#  2900-01-02   NaN
#  Length: 12, dtype: float64
~~~

### data frame之间的操作

让我们从两个数据帧之间的操作开始。  逻辑与我们之前看到的类似，只是现在我们需要处理两个索引，df.columns 和 df.index。  直观上 df1 + df2 是这样工作的：

- Pandas 将创建一个以 NaN 为元素的新数据框
- - 这个新数据框的行索引是 df1.index 和 df2.index 的并集.
  - 列索引将是 df1.columns 和 df2.columns 的联合(并集)。 

- Pandas 将选择列和索引的交集（在两个数据框中找到的索引和列标签）
- - 对于此选择，Pandas 将对 df1 和 df2 的相应元素求和。  这些将被插入到新的data frame中，用于适当的行和列索引。

~~~
print(df)
# Output:
#              close  bday
#  2020-01-02   7.16     1
#  2020-01-03   7.19     2
#  2020-01-06   7.00     3
#  2020-01-07   7.10     4
#  2020-01-08   6.86     5
#  2020-01-09   6.95     6
#  2020-01-10   7.00     7
#  2020-01-13   7.02     8
#  2020-01-14   7.11     9
#  2020-01-15   7.04    10

# This will be a dataframe with just one column 'bday'
# (Note the column argument is a list of one element)
df2 = df.iloc[1:3, [1]]
print(df2)

# Output:
#              bday
#  2020-01-03     2
#  2020-01-06     3

print(df + df2)

# Output:
#              bday  close
#  2020-01-02   NaN    NaN
#  2020-01-03   4.0    NaN
#  2020-01-06   6.0    NaN
#  2020-01-07   NaN    NaN
#  2020-01-08   NaN    NaN
#  2020-01-09   NaN    NaN
#  2020-01-10   NaN    NaN
#  2020-01-13   NaN    NaN
#  2020-01-14   NaN    NaN
#  2020-01-15   NaN    NaN
~~~

### dataframe 和 series 之间的操作

数据框和系列之间的操作可能会变得非常混乱。  这是因为默认行为是将 ser.index 与 df.columns 对齐，然后按行执行操作。

 考虑以下示例：

~~~
# This is a series of 1, indexed by dates
ones_by_dates = pd.Series(1, index=dates)

# In:
print(ones_by_dates)

# Output:
#  2020-01-02    1
#  2020-01-03    1
#  2020-01-06    1
#  2020-01-07    1
#  2020-01-08    1
#  2020-01-09    1
#  2020-01-10    1
#  2020-01-13    1
#  2020-01-14    1
#  2020-01-15    1
#  dtype: int64

# This is a series of 1, indexed by the columns of df
ones_by_cols = pd.Series(1, index=['bday', 'close'])

# In:
print(ones_by_cols)

# Output:
#  bday     1
#  close    1
#  dtype: int64
~~~

首先，让我们将 df 添加到Series-ones_by_dates 这一对象中：

~~~
# This will produce a dataframe of NaN
print(df + ones_by_dates)
# Output:？
~~~

同样，您可以看到 Pandas 所做的是：

- 使用原始 df.index 创建一个数据框，但将 df.columns 和 ones_by_dates.index 的并集作为列。

- 查找 ones_by_dates.index 和 df.columns 之间的交集。  由于没有公共元素，因此生成的数据框将为 NaN。

同时，我们再看一段代码：

~~~
# This will add one to each column
print(df + ones_by_cols)

# Output:
#              bday  close
#  2020-01-02     2   8.16
#  2020-01-03     3   8.19
#  2020-01-06     4   8.00
#  2020-01-07     5   8.10
#  2020-01-08     6   7.86
#  2020-01-09     7   7.95
#  2020-01-10     8   8.00
#  2020-01-13     9   8.02
#  2020-01-14    10   8.11
#  2020-01-15    11   8.04
~~~

### 合并 Pandas 对象：合并和连接

虽然上一节重点介绍了Series和data frame的数学运算（例如，加法），但我们通常希望合并来自两个不同对象的数据，而不必执行任何计算。  合并两个不同的表在数据库编程中称为join，此类任务在其中非常常见。  我们知道 Pandas 系列代表一个单列表，而 Pandas 数据框是一个多列表。  因此，我们遵循标准并使用join术语。

连接 Pandas 对象时，我们通常将其中一个数据框设置为连接中的“左表”。  这将是基础data frame。  然后我们使用 .join 方法将这个数据框与另一个代表“右表”的data frame结合起来。  例如，要将一个名为 left 的数据框连接到另一个名为 right 的数据框，一般这样做：

~~~
left.join(right, how=<join type>)
~~~

上面的 join type 旨在表示 Pandas 如何决定将哪些行包含在组合对象中。  join 方法在执行连接时提供了相当大的灵活性。  通过指定 how 参数，我们可以更改结果数据框中出现的行索引。  参数 how 可以采用以下值（所有字符串）：

- how='left' 告诉 Pandas 使用来自调用数据框索引 (left.index) 的行标签。  左侧数据框中的任何行标签都将出现在结果数据框中，即使它不在右侧数据框的索引中也是如此。  结果中将忽略出现在右侧数据框中但未出现在左侧的行标签。
- how='right' 是使用右侧数据框 (right.index) 中的行标签的指令。  右侧数据框的任何行标签都将出现在结果中，即使它不在左侧数据框的索引中也是如此。  结果中将忽略出现在左侧数据框中但不在右侧的行标签。
- how=outer' 表示结果数据帧的索引将包括索引 left.index 和 right.index 的并集。  来自左侧或右侧数据框的任何行标签都将出现在结果中，即使该标签仅出现在两个数据框之一中也是如此。  行标签将按字典顺序排序。
- how=inner' 指示 Pandas 返回一个包含两个索引 right.index 和 left.index 的交集的数据框。  结果中的行标签必须出现在两个数据框的索引中。  行标签将按照左侧调用数据框中使用的顺序显示。

~~~
left = pd.DataFrame(
        data=[('L1'), ('L2'), ('L3')],
        index=[1,2,3],
        columns=['L'],
        )
print(left)


right = pd.DataFrame(
        data=[('R3'), ('R4'), ('R5')],
        index=[3,4,5],
        columns=['R'],
        )
print(right)

print(left.join(right, how='left'))
output:?
print(left.join(right, how='right'))
output:?
print(left.join(right, how='inner'))
output:?
print(left.join(right, how='outer'))
output:?
~~~



## 使用布尔值选择观察值

### 使用布尔值的 Pandas 选择

将下面的代码复制并粘贴到 lec_pd_bools.py 文件中：

~~~
import pprint as pp

import pandas as pd


# ---------------------------------------------------------------------------- 
# Create an example dataset
# ---------------------------------------------------------------------------- 
data = {
    'date': [
        '2012-02-16 07:42:00',
        '2020-09-23 08:58:55',
        '2020-09-23 09:01:26',
        '2020-09-23 09:11:01',
        '2020-09-23 11:15:12',
        '2020-11-18 11:07:44',
        '2020-12-09 15:34:34',
        ],
    'firm': [
        'JP Morgan',
        'Deutsche Bank',
        'Deutsche Bank',
        'Wunderlich',
        'Deutsche Bank',
        'Morgan Stanley',
        'JP Morgan',
        ],
    'action': [
        'main',
        'main',
        'main',
        'down',
        'up',
        'up',
        'main',
        ],
}
~~~

此模块创建以下示例data frame：

~~~
data.loc[:, 'date'] = pd.to_datetime(data['date'])
print(type(data['date'])) # --> <class 'pandas.core.indexes.datetimes.DatetimeIndex'> 

# Create the dataframe and set the column 'date' as the index
df = pd.DataFrame(data=data).set_index('date') 
print(df)

# Output:
#                               firm  action
# date                                      
# 2012-02-16 07:42:00       JP Morgan   main
# 2020-09-23 08:58:55   Deutsche Bank   main
# 2020-09-23 09:01:26   Deutsche Bank   main
# 2020-09-23 09:11:01      Wunderlich   down
# 2020-09-23 11:15:12   Deutsche Bank     up
# 2020-11-18 11:07:44  Morgan Stanley     up
# 2020-12-09 15:34:34       JP Morgan   main

df.info()

# Output:
# <class 'pandas.core.frame.DataFrame'>
# DatetimeIndex: 7 entries, 2012-02-16 07:42:00 to 2020-12-09 15:34:34
# Data columns (total 2 columns):
#  #   Column  Non-Null Count  Dtype 
# ---  ------  --------------  ----- 
#  0   firm    7 non-null      object
#  1   action  7 non-null      object
# dtypes: object(2)
# memory usage: 168.0+ bytes
~~~

我们可以使用布尔值数组从 Pandas 系列或data frame中选择数据。  这适用于 [] 或 .loc。

~~~
# will be a series with boolean values 
cond = df.loc[:, 'action'] == 'up'
print(cond) 

# Output:
#
# 2012-02-16 07:42:00    False
# 2020-09-23 08:58:55    False
# 2020-09-23 09:01:26    False
# 2020-09-23 09:11:01    False
# 2020-09-23 11:15:12     True
# 2020-11-18 11:07:44     True
# 2020-12-09 15:34:34    False
# Name: action, dtype: bool
~~~

如您所见，这将返回一个布尔值系列（注意 dtype），指示条件 df.loc[:, 'action'] == 'up' 是真还是假。  我们可以在 .loc 方法中使用这个系列作为行索引器：

~~~~
# We can use this series as an indexer:
#   A series of booleans can be used to select rows that meet the criteria
res = df.loc[cond]
print(res)

# Output
#                               firm  action
# date                                      
# 2020-09-23 11:15:12   Deutsche Bank     up
# 2020-11-18 11:07:44  Morgan Stanley     up
~~~~

使用 .loc 时，仅使用布尔系列 cond 的值来选择行。  上面 cond 系列的索引无关紧要。  事实上，下面会产生相同的结果。

~~~
# Get the underlying values of `cond` as an array
new_cond = cond.array

# This will produce the same output as above
res = df.loc[new_cond]
print(res)

# Output
#                               firm  action
# date                                      
# 2020-09-23 11:15:12   Deutsche Bank     up
# 2020-11-18 11:07:44  Morgan Stanley     up
~~~

重要的是，cond 系列的大小必须与分度器中轴的大小相匹配。  例如，以下将返回错误，因为 cond 的切片不包括最后一个元素：

~~~
# Indexer not the same length as the dataframe
df.loc[cond[:-1]]   # --> raises an exception
~~~

布尔索引器可用于选择行或列。  例如，以下将选择数据框的第一列（和所有行）：

~~~
print(df.loc[:, [True, False]])

# Output:
#                                firm
# date                               
# 2012-02-16 07:42:00       JP Morgan
# 2020-09-23 08:58:55   Deutsche Bank
# 2020-09-23 09:01:26   Deutsche Bank
# 2020-09-23 09:11:01      Wunderlich
# 2020-09-23 11:15:12   Deutsche Bank
# 2020-11-18 11:07:44  Morgan Stanley
# 2020-12-09 15:34:34       JP Morgan
~~~

您可以使用布尔索引器来选择行、列或两者。  例如，以下将返回 df 的最后一列和带有“action == 'up'”的行：

~~~
cond = df.loc[:, 'action'] == 'up'
print(df.loc[cond, [False, True]])

#                     action
# date                      
# 2020-09-23 11:15:12     up
# 2020-11-18 11:07:44     up
~~~

您可以将具有布尔值的数据框传递给 []，但不能传递给 .loc。  与往常一样，请小心使用 []，因为结果可能不是您所期望的。  例如，以下示例将返回一个与 df 具有相同结构但具有值 True/False 的数据框，具体取决于观察是否缺失（“不可用”）：

~~~
print(df.isna())
# Output:
#                       firm  action
# date                              
# 2012-02-16 07:42:00  False   False
# 2020-09-23 08:58:55  False   False
# 2020-09-23 09:01:26  False   False
# 2020-09-23 09:11:01  False   False
# 2020-09-23 11:15:12  False   False
# 2020-11-18 11:07:44  False   False
# 2020-12-09 15:34:34  False   False

# df.loc[df.isna()]  # --> exception
~~~

原因是 .loc 方法需要一个行索引器作为 .loc[] 的第一个元素。  对于具有一维索引的data frame，此索引器也必须是一维的。  在这种情况下，data frame不能用作行索引器。

 另一方面，您可以使用布尔数据框来选择带有 [] 的观察值。  例如，以下是允许的，但它可能不会产生您想要的结果：

~~~
print(df[df.isna()])
# Output:
#                     firm  action
# date                           
# 2012-02-16 07:42:00  NaN    NaN
# 2020-09-23 08:58:55  NaN    NaN
# 2020-09-23 09:01:26  NaN    NaN
# 2020-09-23 09:11:01  NaN    NaN
# 2020-09-23 11:15:12  NaN    NaN
# 2020-11-18 11:07:44  NaN    NaN
# 2020-12-09 15:34:34  NaN    NaN
~~~

您可以使用布尔数组替换系列或数据框中的值。  接下来的两个示例说明了如何使用 [] 或 .loc 替换“action”列的元素。

 首先，我们将使用 [] 将action列中的“up”的所有实例替换为“UP”（大写）：

~~~
cond = df.loc[:, 'action'] == 'up'
df['action'][cond] = "UP"
print(df)
 
# Output:
#                                firm action
# date                                      
# 2012-02-16 07:42:00       JP Morgan   main
# 2020-09-23 08:58:55   Deutsche Bank   main
# 2020-09-23 09:01:26   Deutsche Bank   main
# 2020-09-23 09:11:01      Wunderlich   down
# 2020-09-23 11:15:12   Deutsche Bank     UP
# 2020-11-18 11:07:44  Morgan Stanley     UP
# 2020-12-09 15:34:34       JP Morgan   main
~~~

接下来，我们将使用 .loc 恢复更改（从“UP”到“up”）：

~~~
cond = df.loc[:, 'action'] == 'UP'
df.loc[cond, 'action'] = 'up'
print(df)

# Output:
#                                firm action
# date                                      
# 2012-02-16 07:42:00       JP Morgan   main
# 2020-09-23 08:58:55   Deutsche Bank   main
# 2020-09-23 09:01:26   Deutsche Bank   main
# 2020-09-23 09:11:01      Wunderlich   down
# 2020-09-23 11:15:12   Deutsche Bank     up
# 2020-11-18 11:07:44  Morgan Stanley     up
# 2020-12-09 15:34:34       JP Morgan   main
~~~

或者：

~~~
new_df = df.copy()
cond = df.loc[:, 'action'] == 'up'
new_df.loc[cond] = 'UP' 
print(new_df)
 
# Output:
#                               firm action
# date                                     
# 2012-02-16 07:42:00      JP Morgan   main
# 2020-09-23 08:58:55  Deutsche Bank   main
# 2020-09-23 09:01:26  Deutsche Bank   main
# 2020-09-23 09:11:01     Wunderlich   down
# 2020-09-23 11:15:12             UP     UP
# 2020-11-18 11:07:44             UP     UP
# 2020-12-09 15:34:34      JP Morgan   main
~~~

使用布尔值进行选择非常有用，您会经常使用它。  您甚至可以将不同的条件组合在一起。  例如，考虑仅选择“action”的值为“up”或“down”的日期的任务。

 有多种方法可以执行此任务。  例如，要根据涉及多个条件的标准选择观察值，我们可以使用运算符“|”，在 Python 中表示“逻辑或”：

~~~
# ----------------------------------------------------------------------------
#   Multiple criteria 
# ----------------------------------------------------------------------------
# Combine different criteria
crit = (df.loc[:, 'action'] == 'up') | (df.loc[:, 'action'] == 'down')
print(df.loc[crit])

# Output:
#                                firm action
# date                                      
# 2020-09-23 09:11:01      Wunderlich   down
# 2020-09-23 11:15:12   Deutsche Bank     up
# 2020-11-18 11:07:44  Morgan Stanley     up
~~~

Series.str.contains 将返回一系列布尔值，当特定观察包含给定文本时，这些布尔值的计算结果为 True。  此方法允许使用正则表达式，这使其非常强大。  如果你以前见过正则表达式，这是要走的路：

~~~
# ----------------------------------------------------------------------------
#   Using the `str.contains` method
# ----------------------------------------------------------------------------
crit = df.loc[:, 'action'].str.contains('up|down')
print(df.loc[crit])

# Output:
#                               firm  action
# date                                      
# 2020-09-23 09:11:01      Wunderlich   down
# 2020-09-23 11:15:12   Deutsche Bank     up
# 2020-11-18 11:07:44  Morgan Stanley     up
~~~

