# Pandas简介2

## Pandas 索引

在进入细节之前，让我们介绍一下这三种索引方法的一些基础知识：

- .loc：仅通过标签进行索引（基于标签的索引）      

- .iloc：仅通过整数位置进行索引（位置索引）      

- []：结合了基于标签和位置的索引。

将以下代码复制并粘贴到 lec_pd_indexing.py 文件中：

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

该模块创建了我们在上一节中使用的相同的Series和dataframe:

~~~
# ---------------------------------------------------------------------------- 
#   Create instances
# ---------------------------------------------------------------------------- 

# Create a series object
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


# Data Frame with close and Bday columns
df = pd.DataFrame(data={'Close': ser, 'Bday': bday}, index=dates)
print(df)

# Output:
#             Close  Bday
# 2020-01-02   7.16     1
# 2020-01-03   7.19     2
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 2020-01-08   6.86     5
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7
# 2020-01-13   7.02     8
# 2020-01-14   7.11     9
# 2020-01-15   7.04    10
~~~

### Pandas：使用 .loc 建立索引

#### 使用 .loc 建立Series索引

| Selection                         | Result       | Notes                               |
| --------------------------------- | ------------ | ----------------------------------- |
| Series.loc[label]                 | scalar value | Label 必须存在，否则 KeyError       |
| Series.loc[list of labels]        | Series       | 所有Label 必须存在，否则为 KeyError |
| Series.loc[start_label:end_label] | Series       | 结果各不相同                        |

#### Series.loc：使用单个标签进行选择

~~~
# 1.1 Series
# -------------

# 1.1.1 Series.loc: Selection using a single label
# ser.loc[label] --> scalar if label in index, error otherwise

# Set `x` below to be the price on 2020-01-10
x = ser.loc['2020-01-10'] # --> 7.0

# The following will raise a KeyError
ser.loc['3000-01-10'] # --> KeyError
~~~

您还可以使用 .loc 设置元素的值。  例如，我们可以将“2020-01-02”的价格设置为 0：

~~~
# Set the price for 2020-01-02 to zero
ser2 = ser.copy() 
ser2.loc['2020-01-02'] = 0  
print(ser2)                 

# Output: 
#    2020-01-02    0.00   <-- Note the difference
#    2020-01-03    7.19
#    2020-01-06    7.00
#    2020-01-07    7.10
#    2020-01-08    6.86
#    2020-01-09    6.95
#    2020-01-10    7.00
#    2020-01-13    7.02
#    2020-01-14    7.11
#    2020-01-15    7.04
#    dtype: float64
~~~

#### Series.loc：选择标签序列

~~~
# 1.1.2 Series.loc: Selection using sequence of labels
# will return a series

x = ser.loc[['2020-01-03', '2020-01-10']]
print(x)

# Output:
#  2020-01-03    7.19
#  2020-01-10    7.00
#  dtype: float64

print(type(x)) # --> <class 'pandas.core.series.Series'>
~~~

#### Series.loc：使用标记的切片进行选择

为 Series.loc 指定一个切片会返回一个Series。  重要的是，使用切片选择时将包括端点！

~~~
x = ser.loc['2020-01-03':'2020-01-10']
print(x)

# Output:
# 2020-01-03    7.19
# 2020-01-06    7.00
# 2020-01-07    7.10
# 2020-01-08    6.86
# 2020-01-09    6.95
# 2020-01-10    7.00
# dtype: float64
~~~

#### 使用 .loc 索引dataframe

#### DataFrame.loc：使用单个标签进行选择

这里我们必须区分两种情况：      

- 单个行和列标签返回单个值（标量）。      
- 单行或单列标签返回一个Series。

~~~
# For instance, selecting the close price on January 3, 2020
x = df.loc['2020-01-03', 'Close'] 
print(x) # --> 7.19 

# A single row **or** a single column label will return a series:
# The following will return a series corresponding to the column "Close"
x = df.loc[:,'Close'] 
print(x)

# Output :
# 2020-01-02    7.16
# 2020-01-03    7.19
# 2020-01-06    7.00
# 2020-01-07    7.10
# 2020-01-08    6.86
# 2020-01-09    6.95
# 2020-01-10    7.00
# 2020-01-13    7.02
# 2020-01-14    7.11
# 2020-01-15    7.04
# Name: Close, dtype: float64

type(df.loc[:,'Close']) # --> <class 'pandas.core.series.Series'>

y = df.loc['2020-01-03', :]
print(y)

# Output:
# Close    7.19
# Bday     2.00
# Name: 2020-01-03, dtype: float64

print(type(df.loc['2020-01-03', :])) # --> <class 'pandas.core.series.Series'>
~~~

上面的示例使用 : 表示我们想要所有行 ([:, 'Close']) 或所有列 (['2020-01-03', :])。  但是，当您想要一个包含数据框中一行的所有列值的系列时，您可以简单地这样写 :

~~~
# This is equivalent to df.loc['2020-01-03',:]
x = df.loc['2020-01-03']
print(x)

# Out:
# Close    7.19
# Bday     2.00
# Name: 2020-01-03, dtype: float64


print(type(df.loc['2020-01-03'])) # --> <class 'pandas.core.series.Series'>

# This will raise an exception because the label does not exist
df.loc['2020-01-01']
~~~

#### DataFrame.loc：使用多个标签进行选择

就像Series一样，您可以使用一段连续的标签（作为行或列索引器）。  例如：

~~~
# Set x so it contains the closing prices for '2020-01-02' and '2020-01-03'
x = df.loc[['2020-01-02', '2020-01-03'], 'Close']
print(x)

# Output:
#  2020-01-02    7.16
#  2020-01-03    7.19
#  Name: Close, dtype: float64
~~~

#### DataFrame.loc：使用切片进行选择

我们为所有列选择一部分行（日期），产生一个dataframe：

~~~
# the next statement is equivalent to x = df.loc['2020-01-01':'2020-01-10']
x = df.loc['2020-01-01':'2020-01-10', :]
print(x)

# Output:
#             Close  Bday
# 2020-01-02   7.16     1
# 2020-01-03   7.19     2
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 2020-01-08   6.86     5
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7

print(type(x)) # --> <class 'pandas.core.frame.DataFrame'>
~~~

重要的是要记住，在使用切片时，Pandas 会返回dataframe中位于请求的开始和结束之间的所有标签。  换句话说，如果切片的一部分没有包含在索引中，Pandas 不会抛出异常。  这类似于切片如何处理列表：

~~~
some_list = [1, 2, 3, 4]

# Slices do not include endpoints
# x -> [1]
x = some_list[0:1]

# This will not raise an exception
# x -> []
x = some_list[100:101]
~~~

对于Series或dataframe来说，这将返回一个空系列或数据框：

~~~
x = df.loc['2999-01-01':'2999-01-10', :]
print(x)

# Output:
# Empty DataFrame
# Columns: [Close, Bday]
# Index: []

print(type(x)) # --> <class 'pandas.core.frame.DataFrame'>
~~~

与列表一样，切片可以是开放式的。  如果我们指定一个起点并省略终点 (start:)，那么 Pandas 会为我们提供以起点开头的所有元素。   如果我们省略开头并指定结尾 (:end)，Pandas 会给出从开头到结尾的所有元素。  下面是一个带有开放式切片的示例：

~~~
# Slices can be open ended
# However, single row labels and open column slices will NOT return a
# data frame, they will return a series!!!

x = df.loc['2020-01-06':, :]
print(x)

# Out:
#             Close  Bday
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 2020-01-08   6.86     5
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7
# 2020-01-13   7.02     8
# 2020-01-14   7.11     9
# 2020-01-15   7.04    10

# print(type(x)) # --> <class 'pandas.core.frame.DataFrame'>

x = df.loc['2020-01-06', 'Close':]
print(x)

# Out:
# Close    7.0
# Bday     3.0
# Name: 2020-01-06, dtype: float64

# print(type(x)) # --> <class 'pandas.core.series.Series'>
~~~

重要的是，如果索引未排序，带有 .loc 的切片可能无法按预期工作。  让我们重点重复一遍！  如果索引未排序，带有 .loc 的切片可能无法按预期工作。  例如：

~~~
df2 = df.copy()

df2.rename(index={'2020-01-08':'1900-01-01'}, inplace=True)

print(df2)

# Out:
#             Close  Bday
# 2020-01-02   7.16     1
# 2020-01-03   7.19     2
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 1900-01-01   6.86     5
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7
# 2020-01-13   7.02     8
# 2020-01-14   7.11     9
# 2020-01-15   7.04    10

# print(type(df2)) # --> <class 'pandas.core.frame.DataFrame'>

x = df2.loc['2020-01-03':'2020-01-10', :]
print(x)

# Out:
#             Close  Bday
# 2020-01-03   7.19     2
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 1900-01-01   6.86     5
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7
~~~

这可以通过先对索引进行排序来避免。

~~~
# You can avoid these issues by sorting the dataframe first
df2.sort_index(inplace=True)
x = df2.loc['2020-01-03':'2020-01-10', :]
print(x) 

# Out:
#             Close  Bday
# 2020-01-03   7.19     2
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7
~~~

最后，请注意，如果我们在切片中指定相同的起点和终点，Pandas 将返回一个dataframe。

~~~
# This will return a DataFrame
x = df.loc['2020-01-03':'2020-01-03']
print(x)

# Output:
#             Close  Bday
# 2020-01-03   7.19     2

# print(type(x)) # --> <class 'pandas.core.frame.DataFrame'>


# This will return a series
x = df.loc['2020-01-03']
print(x)

# Output:
# Close    7.19
# Bday     2.00
# Name: 2020-01-03, dtype: float64

print(type(x)) # -->  <class 'pandas.core.series.Series'>
~~~

### Pandas：使用 .iloc 建立索引

#### 使用 .iloc 索引系列

#### Series.iloc：使用单个位置索引进行选择

Series包含一系列数据元素，如列表。  使用单个位置索引从系列中选择返回单个（标量）值：

~~~
# ser.iloc[pos] --> scalar if abs(pos) < len(ser), otherwise error
x = ser.iloc[0]  # --> 7.16 
x = ser.iloc[-1] # --> 7.04 

x = ser.iloc[100] # raises IndexError
~~~

与基于标签的索引一样，我们可以使用位置 .iloc 索引来分配值：

~~~
# Using .loc for assignment
# Copy the series
s2 = ser.copy()

# assign 
s2.iloc[0] = 0
print(s2)

# Output:
# 2020-01-02    0.00
# 2020-01-03    7.19
# 2020-01-06    7.00
# 2020-01-07    7.10
# 2020-01-08    6.86
# 2020-01-09    6.95
# 2020-01-10    7.00
# 2020-01-13    7.02
# 2020-01-14    7.11
# 2020-01-15    7.04
# dtype: float64
~~~

#### Series.iloc：使用一系列位置索引进行选择

如果我们指定一个索引序列，.iloc 返回一个包含位置索引处的数据项的Series：

~~~
# 2.1.2 Series.iloc: Selection using sequence of labels

x = ser.iloc[[0, 2]]
print(x)

# Output:
# 2020-01-02    7.16
# 2020-01-06    7.00
# dtype: float64
~~~

#### Series.iloc：使用位置索引切片进行选择

如开头所述，.iloc，切片将不包括端点，使 .iloc 的行为与 Python 中的其他位置索引方法一致：

~~~~
x = ser.iloc[0:1] # x --> series with one row
print(x)
# Output:
# 2020-01-02    7.16
# dtype: float64


x = ser.iloc[0:2]
print(x)
# Output:
# 2020-01-02    7.16
# 2020-01-03    7.19
# dtype: float64
~~~~

#### 使用 .iloc 索引 DataFrame

#### DataFrame.iloc：使用单一位置索引进行选择

如果我们指定单个行和列索引，.iloc 返回单个值（标量）。  单行或单列位置索引返回一个系列。  行索引器始终是必需的。  与系列一样，我们也可以使用列表作为索引器。

~~~
x = df.iloc[0]
print(x)

# Output:
#   Close    7.16
#   Bday     1.00

# Equivalent to
x = df.iloc[0,:]
print(x)

# Output:
#   Close    7.16
#   Bday     1.00


x = df.iloc[10] # --> raises IndexError because the DF contains 10 rows
~~~

我们可以对列使用单个索引器，但我们需要包括行索引器：

~~~
# First column (and all rows):
x = df.iloc[:,0]
print(x)

# Output:
# 2020-01-02    7.16
# 2020-01-03    7.19
# 2020-01-06    7.00
# 2020-01-07    7.10
# 2020-01-08    6.86
# 2020-01-09    6.95
# 2020-01-10    7.00
# 2020-01-13    7.02
# 2020-01-14    7.11
# 2020-01-15    7.04
# Name: Close, dtype: float64
~~~

#### DataFrame.iloc：使用索引序列进行选择

这与标签序列和 .loc 的工作方式相同，只是我们使用位置索引代替标签索引。  请记住，如果我们在行索引器中使用单个索引，则输出是一个系列。

~~~
# This will return a series with the first two columns as labels:
x = df.iloc[0,[0,1]]
print(x)

# Output :
#   Close    7.16
#   Bday     1.00
#   Name: 2020-01-02, dtype: float64

# This will return a *dataframe* with the first row of df
x = df.iloc[0:1,:]
print(x)

# Output:
#             Close  Bday
# 2020-01-02   7.16     1

# print(type(x)) # --> <class 'pandas.core.frame.DataFrame'>

# If the column indexer is omitted, all columns will be returned.

# df.iloc[list of row pos] --> dataframe with rows in the list
# Note: will raise IndexError if pos is out of bounds
x = df.iloc[[0, 1]] # --> DF with first two rows of df
print(x)

# Output:
#             Close  Bday
# 2020-01-02   7.16     1
# 2020-01-03   7.19     2
~~~

但是，如果任何索引超出范围，Pandas 会引发异常：

~~~
# The following will raise an exception
x = df.iloc[[0, 10]] # --> raises IndexError

# The following will raise an exception
x = df.iloc[[0,100], :] 
~~~

#### DataFrame.iloc：使用切片进行选择

~~~
x = df.iloc[1:1000, :]
print(x)

# Output:
#             Close  Bday
# 2020-01-03   7.19     2
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 2020-01-08   6.86     5
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7
# 2020-01-13   7.02     8
# 2020-01-14   7.11     9
# 2020-01-15   7.04    10

# print(type(x)) # --> <class 'pandas.core.frame.DataFrame'>

x = df.iloc[999:1000, :]
print(x)

# Output:
# Empty DataFrame
# Columns: [Close, Bday]
# Index: []
~~~

切片也可以是开放式的。  省略端点会产生指定起始位置的所有数据。  当省略起始位置时，我们获取从开始到指定结束位置的所有数据。

~~~
# Slices can be open ended
x = df.iloc[2:, :]
print(x)

# Output :
#             Close  Bday
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 2020-01-08   6.86     5
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7
# 2020-01-13   7.02     8
# 2020-01-14   7.11     9
# 2020-01-15   7.04    10

x = df.iloc[0, 0:]
print(x)

# Output:
# Close    7.16
# Bday     1.00
# Name: 2020-01-02, dtype: float64
# print(type(x)) # --> <class 'pandas.core.series.Series'>

# This will return an empty series
x = df.iloc[0, 10:]
print(x)

# Output:
# Series([], Name: 2020-01-02, dtype: float64)

# print(type(x)) # -->  <class 'pandas.core.series.Series'>
~~~

### 用[ ]索引pandas

#### Series 和 []

| Selection                     | Result       | Notes                           |
| ----------------------------- | ------------ | ------------------------------- |
| Series[label]                 | scalar value | Label必须存在，否则KeyError     |
| Series[list of labels]        | Series       | 所有Label必须存在，否则KeyError |
| Series[start_label:end_label] | Series       | 结果会有所不同                  |
| Series[pos]                   | scalar       | 类似于列表                      |
| Series[list of pos]           | Series       | 类似于列表                      |
| Series[start_pos:end_pos]     | Series       | 不包括端点                      |

为了说明每种方法，让我们使用之前创建的 ser 系列：

~~~
print(ser)

# Out:
#    2020-01-02    7.16
#    2020-01-03    7.19
#    2020-01-06    7.00
#    2020-01-07    7.10
#    2020-01-08    6.86
#    2020-01-09    6.95
#    2020-01-10    7.00
#    2020-01-13    7.02
#    2020-01-14    7.11
#    2020-01-15    7.04
#    dtype: float64
~~~

#### Series：使用单个标签的基于 [] 的选择

使用单个标签的选择在语法上等同于使用键访问字典中的元素。  重要的是要记住标签必须存在，否则 Python 会生成 KeyError：

~~~
# 3.1.1 label, list of labels, label slices

# Set `x` to be the price for '2020-01-13'
x = ser['2020-01-13'] 
print(x) # --> 7.02

# The following raises KeyError because label not part of ser.index
x = ser['3000-01-10'] 
~~~

通过在方括号之间指定标签列表，我们可以从一系列中选择多个元素。  如果一步完成，最外面的括号定义索引运算符，内部括号定义标签列表。  这将返回一个系列，其中包含与标签对应的行。  所有标签都必须是索引的一部分，否则 Pandas 会产生错误。

~~~
# Set `x` to be a series with the first two rows of `ser`
x = ser[['2020-01-02', '2020-01-03']] # --> first two rows

# All labels must exist
x = ser[['2020-01-02', '3000-01-10']] # raises KeyError because a label is not part of ser.index
~~~

#### Series：使用标记切片的基于 [] 的选择

(1) 如果索引中包含start_label和end_label，则返回start_label和end_label之间的所有元素（包括端点）。

~~~
# Set `x` to include all obs between  '2020-01-13' and '2020-01-14'
x = ser['2020-01-13':'2020-01-14']
print(x)

# Output:
# 2020-01-13    7.02
# 2020-01-14    7.11
#  dtype: float64
~~~

(2) 如果 start_label 或 end_label 不包含在索引中：      

- 如果索引已排序，则切片使用在 start_label 和 end_label 之间找到的所有标签。      
- 如果索引未排序，Pandas 会产生错误。  首先考虑索引排序时的情况：

~~~
# The `ser` above is sorted by index. 
# Set `x` to include all obs between '2020-01-13' and '3000-01-01'. The
# end data (obviously) is not part of the series
x = ser['2020-01-13':'3000-01-01'] 
print(x) 
~~~

请注意，x 包含从“2020-01-13”开始的所有元素。要查看索引未排序时会发生什么，让我们修改标签。  我们将使用字母标签“a”、“c”和“b”。  这些没有排序，因为它们不是按字母顺序排列的；  因此，索引未按系列排序。  我们将为此示例创建一个新系列：

~~~
# Create a series with an unsorted index 
new_ser = pd.Series(data=[1,3,2], index=['a', 'c', 'b']) 

# First, select a slice from 'a' to 'b'. Because both labels are included in
# the index, the slice will contain all obs between the indexes 'a' and 'b'
x = new_ser['a':'b'] 
print(x) 

# Next, select a slice from 'b' to 'z'. Note that 'z' is not part of the
# index. Since the index is not sorted, the following will result in an error
x = new_ser['b':'z'] 

# Series also have a method called `sort_index`, which will return a copy of the
# series with sorted indexes:

# Sort the series
sorted_ser = new_ser.sort_index() 
print(sorted_ser) 

# Output:
#  a    1
#  b    2
#  c    3
#  dtype: int64

# This will return only the first rows (not the entire series as before)
x = sorted_ser['a':'b'] 
print(x) 

# Output:
#  a    1
#  b    2
#  dtype: int64

# `sorted_ser` is sorted so the following will return the intersection between
# the slice and the row labels
x = sorted_ser['b':'z'] 
print(x) 

# Output:
#  b    2
#  c    3
#  dtype: int64
~~~

#### Series: []-基于按数值位置选择

此代码示例通过使用数字位置演示了每种选择方法：

~~~
# Using the ser created above
print(ser)
# Out:
#    2020-01-02    7.16
#    2020-01-03    7.19
#    2020-01-06    7.00
#    2020-01-07    7.10
#    2020-01-08    6.86
#    2020-01-09    6.95
#    2020-01-10    7.00
#    2020-01-13    7.02
#    2020-01-14    7.11
#    2020-01-15    7.04
#    dtype: float64

# Get the first element of the series
x = ser[0] 

# Get the first and fourth element (series)
x = ser[[0,3]] 

# NOTE: When using slices, the endpoints are NOT included
# This will return a series with the first element only
x = ser[0:1] 
print(x)

# Output:
#  2020-01-02    7.16
#  dtype: float64

# This will return the first five elements of the series
x = ser[:5]
print(x)
# Returns:
# 2020-01-02    7.16
# 2020-01-03    7.19
# 2020-01-06    7.00
# 2020-01-07    7.10
# 2020-01-08    6.86
# dtype: float64

# This will return every other element, starting at position 0
x = ser[::2]
# Out:
# 2020-01-02    7.16
# 2020-01-06    7.00
# 2020-01-08    6.86
# 2020-01-10    7.00
# 2020-01-14    7.11
# dtype: float64

# This returns the series in reverse order
x = ser[::-1]
# Out:
# 2020-01-15    7.04
# 2020-01-14    7.11
# 2020-01-13    7.02
# 2020-01-10    7.00
# 2020-01-09    6.95
# 2020-01-08    6.86
# 2020-01-07    7.10
# 2020-01-06    7.00
# 2020-01-03    7.19
# 2020-01-02    7.16
# dtype: float64
~~~

如前所述，当索引包含整数时，我们强烈建议不要使用这种方法来选择数据。  我们提供了一个示例，说明当索引中有整数时会发生什么，这样我们就可以识别潜在的问题并知道为什么不建议再自己的项目中这样做：

~~~
new_ser = pd.Series(data=['a','b', 'c'], index=[1, -4, 10])
# This will produce an empty series (because pandas thinks these are positions, not labels)
x = new_ser[1:-4] 
print(x)
~~~

#### Dataframe 和 []

#### DataFrames：使用单个标签的基于 [] 的选择

~~~
print(df)

# Output:
#             Close  Bday
# 2020-01-02   7.16     1
# 2020-01-03   7.19     2
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 2020-01-08   6.86     5
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7
# 2020-01-13   7.02     8
# 2020-01-14   7.11     9
# 2020-01-15   7.04    10


# df[column label] --> series if column exists, error otherwise
# `x` will be a series with values in Close
x = df['Close'] 
print(x)
# Returns a series:
# Out:
# 2020-01-02    7.16
# 2020-01-03    7.19
# 2020-01-06    7.00
# 2020-01-07    7.10
# 2020-01-08    6.86
# 2020-01-09    6.95
# 2020-01-10    7.00
# 2020-01-13    7.02
# 2020-01-14    7.11
# 2020-01-15    7.04
# Name: Close, dtype: float64

print(type(df["Close"]))
# <class 'pandas.core.series.Series'>

# Note that the label is case sensitive. For instance the following 
# raises KeyError 
#df['CLOSE'] 
~~~

#### DataFrames：使用标签序列的基于[]的选择

使用标签序列的选择将返回dataframe

~~~
# Sequences of labels
# df[list of column labels] --> dataframe with columns in the same order
# as the column labels
# Note: All column labels must exist, otherwise error
cols = ['Close', 'Bday']
print(df[cols])

# Output:
#             Close  Bday
# 2020-01-02   7.16     1
# 2020-01-03   7.19     2
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 2020-01-08   6.86     5
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7
# 2020-01-13   7.02     8
# 2020-01-14   7.11     9
# 2020-01-15   7.04    10


# We can pass the list of columns directly to the DataFrame:

print(df[["Close", "Bday"]])
# Output:
#             Close  Bday
# 2020-01-02   7.16     1
# 2020-01-03   7.19     2
# 2020-01-06   7.00     3
# 2020-01-07   7.10     4
# 2020-01-08   6.86     5
# 2020-01-09   6.95     6
# 2020-01-10   7.00     7
# 2020-01-13   7.02     8
# 2020-01-14   7.11     9
# 2020-01-15   7.04    10

print(type(df[["Close", "Bday"]]))
# <class 'pandas.core.frame.DataFrame'>
~~~

#### DataFrame：使用切片的基于 [] 的选择：

使用 [] 对数据帧进行切片时，Pandas 查看与切片匹配的行标签，而不是列。  此外，当切片不匹配任何行标签时，它会返回一个空数据框。

~~~
# Slices work similar to ser[slice], i.e., they operate on row indexes
# `x` will be an empty datafame because the slice is not part of the row
# labels
x = df['Close': 'Bday']  
print(x) 

# Output:
# Empty DataFrame
# Columns: [Close, Bday]
# Index: []

# Slicing DFs with [] works very differently than one would expect:
# x --> dataframe with first two rows
x = df['2020-01-02':'2020-01-03']  
print(x) 
# Returns:
#             Close  Bday
# 2020-01-02   7.16     1
# 2020-01-03   7.19     2
~~~

在对数据框的行进行切片时，我们还可以使用位置而不是标签。  但是，端点不包括在内。

~~~
# You can use position instead of row labels, but endpoints are NOT included
# x --> all rows but the last one
x = df[:-1] 
print(x)

# Will NOT raise error if out of bounds
# x -> returns empty DF
x = df[100:1001] 
print(x)
# Returns:
# Empty DataFrame
# Columns: [Close, Bday]
# Index: []
~~~

您还可以选择 DataFrame 的列作为属性。  例如：

~~~
df.Close 
~~~



## 使用 Pandas 存储和检索数据

### 从 CSV 文件中检索数据

将以下代码复制并粘贴到 lec_pd_csv.py 文件中：

~~~
import os
import pandas as pd
import toolkit_config as cfg

QAN_PRC_CSV = os.path.join(cfg.DATADIR, 'qan_prc_2020.csv')
QAN_NOHEAD_CSV = os.path.join(cfg.DATADIR, 'qan_prc_no_header.csv')
QAN_CLOSE_CSV = os.path.join(cfg.DATADIR, 'qan_close_ser.csv')
~~~

Pandas 让我们通过 read_csv 从 CSV 文件中检索数据。  此方法是整个 Pandas 包的一部分。  因此，我们通过 pandas 的 pd 别名使用此方法：pd.read_csv。  pd.read_csv 总是返回一个dataframe，即使 CSV 只有一个有意义的列。

~~~
# Load the data contained in qan_prc_2020.csv to a DF
qan_naive_read = pd.read_csv(QAN_PRC_CSV)
print(qan_naive_read)

# Output:
#             Date  Open   High   Low  Close  Adj Close    Volume
#  0    2020-01-02  7.14  7.210  7.12   7.16   6.985208   4980666
#  1    2020-01-03  7.28  7.310  7.16   7.19   7.014476   2763615
#  2    2020-01-06  7.01  7.030  6.91   7.00   6.829114   7859151
#  3    2020-01-07  7.23  7.255  7.08   7.10   6.926673   7589056
#  4    2020-01-08  7.05  7.080  6.76   6.86   6.692532  13449760
#  ..          ...   ...    ...   ...    ...        ...       ...
#  249  2020-12-22  4.83  4.860  4.78   4.80   4.800000  12150719
#  250  2020-12-23  4.80  4.950  4.80   4.91   4.910000   6895232
#  251  2020-12-24  5.03  5.030  4.89   4.89   4.890000   3588668
#  252  2020-12-29  4.95  5.010  4.94   4.96   4.960000   4330876
#  253  2020-12-30  4.95  4.980  4.91   4.96   4.960000   4010174
#  
#  [254 rows x 7 columns]
           
qan_naive_read.info()

# Output:
#   <class 'pandas.core.frame.DataFrame'>
#   RangeIndex: 223 entries, 0 to 222
#   Data columns (total 7 columns):
#     #   Column     Non-Null Count  Dtype  
#    ---  ------     --------------  -----  
#     0   Date       223 non-null    object 
#     1   Open       223 non-null    float64
#     2   High       223 non-null    float64
#     3   Low        223 non-null    float64
#     4   Close      223 non-null    float64
#     5   Adj Close  223 non-null    float64
#     6   Volume     223 non-null    int64  
#   dtypes: float64(5), int64(1), object(1)
#   memory usage: 12.3+ KB
~~~

我们已经知道我们可以使用列来设置数据框的索引：

~~~
# Using the `set_index` method
qan_naive_read.set_index('Date', inplace=True)
print(qan_naive_read)

# Output:
#              Open   High   Low  Close  Adj Close    Volume
#  Date                                                     
#  2020-01-02  7.14  7.210  7.12   7.16   6.985208   4980666
#  2020-01-03  7.28  7.310  7.16   7.19   7.014476   2763615
#  2020-01-06  7.01  7.030  6.91   7.00   6.829114   7859151
#  2020-01-07  7.23  7.255  7.08   7.10   6.926673   7589056
#  2020-01-08  7.05  7.080  6.76   6.86   6.692532  13449760
#  ...          ...    ...   ...    ...        ...       ...
#  2020-12-22  4.83  4.860  4.78   4.80   4.800000  12150719
#  2020-12-23  4.80  4.950  4.80   4.91   4.910000   6895232
#  2020-12-24  5.03  5.030  4.89   4.89   4.890000   3588668
#  2020-12-29  4.95  5.010  4.94   4.96   4.960000   4330876
#  2020-12-30  4.95  4.980  4.91   4.96   4.960000   4010174
#  
#  [254 rows x 6 columns]

qan_naive_read.info()

# <class 'pandas.core.frame.DataFrame'>
# Index: 254 entries, 2020-01-02 to 2020-12-30
# Data columns (total 6 columns):
#  #   Column     Non-Null Count  Dtype  
# ---  ------     --------------  -----  
#  0   Open       254 non-null    float64
#  1   High       254 non-null    float64
#  2   Low        254 non-null    float64
#  3   Close      254 non-null    float64
#  4   Adj Close  254 non-null    float64
#  5   Volume     254 non-null    int64  
# dtypes: float64(5), int64(1)
# memory usage: 13.9+ KB
~~~

在下面的示例代码中，我们使用列标签来指定索引列。

~~~
# Using the `index_col` parameter:
qan_better_read = pd.read_csv(QAN_PRC_CSV, index_col='Date')
print(qan_better_read)

# Output:
#              Open   High   Low  Close  Adj Close    Volume
#  Date                                                     
#  2020-01-02  7.14  7.210  7.12   7.16   6.985208   4980666
#  2020-01-03  7.28  7.310  7.16   7.19   7.014476   2763615
#  2020-01-06  7.01  7.030  6.91   7.00   6.829114   7859151
#  2020-01-07  7.23  7.255  7.08   7.10   6.926673   7589056
#  2020-01-08  7.05  7.080  6.76   6.86   6.692532  13449760
#  ...          ...    ...   ...    ...        ...       ...
#  2020-12-22  4.83  4.860  4.78   4.80   4.800000  12150719
#  2020-12-23  4.80  4.950  4.80   4.91   4.910000   6895232
#  2020-12-24  5.03  5.030  4.89   4.89   4.890000   3588668
#  2020-12-29  4.95  5.010  4.94   4.96   4.960000   4330876
#  2020-12-30  4.95  4.980  4.91   4.96   4.960000   4010174
#  
#  [254 rows x 6 columns]

          
qan_better_read.info()

# Output:
# <class 'pandas.core.frame.DataFrame'>
# Index: 254 entries, 2020-01-02 to 2020-12-30
# Data columns (total 6 columns):
#  #   Column     Non-Null Count  Dtype  
# ---  ------     --------------  -----  
#  0   Open       254 non-null    float64
#  1   High       254 non-null    float64
#  2   Low        254 non-null    float64
#  3   Close      254 non-null    float64
#  4   Adj Close  254 non-null    float64
#  5   Volume     254 non-null    int64  
# dtypes: float64(5), int64(1)
~~~

### 将数据存储在 CSV 文件中

例如，假设我们要将创建的 qan_better_read 数据框中包含的数据保存到另一个 CSV 文件中。  但是，我们希望此文件仅包含数据，而不包含列标题。  在lec_pd_csv.py模块中，我们会发现如下语句：

~~~
# First, we read the data into a dataframe
qan_better_read = pd.read_csv(QAN_PRC_CSV, index_col='Date')

# We then save the data into the file located at QAN_NOHEAD_CSV above.
# The column headers will not be saved
qan_better_read.to_csv(QAN_NOHEAD_CSV, header=False)
~~~

#### 从 CSV 文件读取/写入系列

但是如果我们想将一个系列的内容保存到一个 CSV 文件中呢？  为了了解它是如何工作的，我们将创建一个名为 ser 的系列，其中包含来自 qan_better_read 数据框的“Close”列的数据。  然后我们将把这个系列保存到 QAN_CLOSE_CSV 代表的文件中：

~~~
# ----------------------------------------------------------------------------
#  Saving the contents of a series to a CSV file
# ----------------------------------------------------------------------------
# Create a series
qan_better_read = pd.read_csv(QAN_PRC_CSV, index_col='Date')
ser = qan_better_read.loc[:, 'Close']
print(ser)

# Output:
#  Date
#  2020-01-02    7.16
#  2020-01-03    7.19
#  2020-01-06    7.00
#  2020-01-07    7.10
#  2020-01-08    6.86
#                ... 
#  2020-12-22    4.80
#  2020-12-23    4.91
#  2020-12-24    4.89
#  2020-12-29    4.96
#  2020-12-30    4.96
#  Name: Close, Length: 254, dtype: float64

# Save the series to a CSV file
ser.to_csv(QAN_CLOSE_CSV)
~~~

这是我们所期望的。  但是 Pandas 是如何知道该系列包含“Close”列中的数据的呢？  默认情况下，每当我们从数据框列创建一个系列时，Pandas 都会为该系列命名，这将是该列的名称。  您可以通过尝试以下操作来了解这一点：

~~~
# Note that the name of the series will be the same as the column label
print(ser.name)

# Output:
#  'Close'
~~~

但是，我们经常创建没有名称的系列。  将系列保存到 CSV 文件时，这可能会出现一些问题。  要查看其工作原理，请按如下方式修改上面的代码：

~~~
# Create a series without a name
dates = list(qan_better_read.index) # --> list with the index labels
data = list(qan_better_read.Close)  # --> list with closing prices
ser_no_name = pd.Series(data, index=dates)
print(ser_no_name)

# Output:
#  2020-01-02    7.16
#  2020-01-03    7.19
#  2020-01-06    7.00
#  2020-01-07    7.10
#  2020-01-08    6.86
#                ... 
#  2020-12-22    4.80
#  2020-12-23    4.91
#  2020-12-24    4.89
#  2020-12-29    4.96
#  2020-12-30    4.96
#  Length: 254, dtype: float64

print(f'The name of the series is {ser_no_name.name}')

# Output:
#  'The name of the series is None'
~~~

如您所见，这个系列没有名字。  接下来，我们将其保存为 CSV 文件：

~~~
# Now save it to the same CSV file as above
ser_no_name.to_csv(QAN_CLOSE_CSV)
~~~

当我们尝试将这个新的 CSV 文件中的数据加载到一个系列中时会发生什么？  如果没有 index_col 参数，数据将作为数据框加载：

~~~
# Read the data back
as_df = pd.read_csv(QAN_CLOSE_CSV)
print(as_df)

# Output:
#      Unnamed: 0     0
# 0    2020-01-02  7.16
# 1    2020-01-03  7.19
# 2    2020-01-06  7.00
# 3    2020-01-07  7.10
# 4    2020-01-08  6.86
# ..          ...   ...
# 249  2020-12-22  4.80
# 250  2020-12-23  4.91
# 251  2020-12-24  4.89
# 252  2020-12-29  4.96
# 253  2020-12-30  4.96
# 
# [254 rows x 2 columns]
~~~

解决上述问题的一种方法是保存不带列标题的系列内容，然后使用参数 index_col=0 加载回数据。  这将告诉 Pandas 第一列包含索引。  请注意，它仍将返回一个dataframe。  此外，Pandas 将分别使用标签“0”和“1”自动命名索引和第一列。

~~~
# Using the ser_no_name created above
# Save the contents without column headers
ser_no_name.to_csv(QAN_CLOSE_CSV, header=False)
# Read it back 
as_df = pd.read_csv(QAN_CLOSE_CSV, header=None, index_col=0)
print(as_df)

# Output:
#                1
# 0               
# 2020-01-02  7.16
# 2020-01-03  7.19
# 2020-01-06  7.00
# 2020-01-07  7.10
# 2020-01-08  6.86
# ...          ...
# 2020-12-22  4.80
# 2020-12-23  4.91
# 2020-12-24  4.89
# 2020-12-29  4.96
# 2020-12-30  4.96
# 
# [254 rows x 1 columns]
~~~

我们可以使用 read_csv 函数的参数名称来告诉 Pandas 在创建数据框之前命名 CSV 文件的列。  例如，我们可以设置 names=["Date", "Close"] 如下例所示：

~~~
# Using the ser_no_name created above
# Save the contents without column headers
ser_no_name.to_csv(QAN_CLOSE_CSV, header=False)
# Read it back 
as_df = pd.read_csv(QAN_CLOSE_CSV, header=None, names=["Date", "Close"], index_col=0)
print(as_df)

# Output:
#             Close
# Date             
# 2020-01-02   7.16
# 2020-01-03   7.19
# 2020-01-06   7.00
# 2020-01-07   7.10
# 2020-01-08   6.86
# ...           ...
# 2020-12-22   4.80
# 2020-12-23   4.91
# 2020-12-24   4.89
# 2020-12-29   4.96
# 2020-12-30   4.96
# 
# [254 rows x 1 columns]
~~~

尽管如此，要在保存Series时明确指定列，我们需要指定一个 index_label 选项和一个 header 选项。  index_label 只是一个带有索引名称的字符串。  标题选项应该是列名列表。  在Series的情况下，这应该是一个包含单个元素的列表，即列的名称。

~~~
# ----------------------------------------------------------------------------
#   Saving the contents of an unnamed series (best version) 
# ----------------------------------------------------------------------------
# Using the ser_no_name created above
# Save the contents without column headers
ser_no_name.to_csv(QAN_CLOSE_CSV, 
        index_label="Date", 
        header=['Close'],
        )
# Read it back 
as_df = pd.read_csv(QAN_CLOSE_CSV, index_col=0)
print(as_df)

# Output:
#             Close
# Date             
# 2020-01-02   7.16
# 2020-01-03   7.19
# 2020-01-06   7.00
# 2020-01-07   7.10
# 2020-01-08   6.86
# ...           ...
# 2020-12-22   4.80
# 2020-12-23   4.91
# 2020-12-24   4.89
# 2020-12-29   4.96
# 2020-12-30   4.96
# 
# [254 rows x 1 columns]
~~~



