TuShare是一个免费、开源的Python财经数据接口包。主要实现对股票等金融产品从数据采集、清洗加工到数据存储的全过程自动化运作，为金融分析人士提供快速、整洁、和多样的便于分析的数据，为他们在数据获取方面极大地减轻工作量，使他们更加专注于策略和模型的研究和实现上。

使用TuShare获取股票数据的步骤大致如下：

### 1. 安装TuShare

你可以使用pip命令在Python环境中安装TuShare：

```python
pip install tushare
```

### 2. 导入TuShare库

在你的Python脚本或者Jupyter notebook中，你可以这样导入TuShare库：

```python
import tushare as ts
```

### 3. 设置Token

在使用TuShare获取数据之前，你需要在TuShare官网注册并获取一个token，然后使用该token初始化TuShare：

```python
ts.set_token('your token')
```

### 4. 获取技术面数据

TuShare提供了`get_hist_data`函数可以获取股票的历史交易数据，这些数据可以用于技术分析。例如，获取中科曙光的历史交易数据：

```python
df = ts.get_hist_data('603019')
print(df)
```

### 5. 获取基本面数据

TuShare提供了`get_stock_basics`函数可以获取股票的基本面数据，例如市盈率、流通股本等。例如，获取所有股票的基本面数据：

```python
df = ts.get_stock_basics()
print(df)
```

以上就是使用TuShare获取股票数据的基本步骤。需要注意的是，由于TuShare的数据更新可能有延迟，因此获取的数据可能并非最新数据，需要在使用时注意。此外，TuShare的API可能会有变动，使用时应根据官方文档和示例进行调整。

如果你需要获取更详细的数据或者使用更高级的功能，你可以查看[TuShare的官方文档](http://tushare.org/)，里面有详细的API说明和使用示例。

以下是一个非常简单的示例，它检查一个特定股票的5天移动平均线与20天移动平均线，如果5天移动平均线从下方穿越20天移动平均线，则生成一个"买入"信号。

```python
import tushare as ts

# 设置你的token
ts.set_token('your_token')

# 选择你感兴趣的股票
stock_code = '603019'

# 获取历史数据
df = ts.get_hist_data(stock_code)

# 计算5天和20天的移动平均线
df['MA5'] = df['close'].rolling(window=5).mean()
df['MA20'] = df['close'].rolling(window=20).mean()

# 找到5天移动平均线从下方穿越20天移动平均线的点
buy_signals = (df['MA5'] > df['MA20']) & (df['MA5'].shift(1) < df['MA20'].shift(1))

# 如果存在买入信号，打印买入
if buy_signals.any():
    print(f"Buy signal for {stock_code} on dates {buy_signals[buy_signals == True].index}")
```
