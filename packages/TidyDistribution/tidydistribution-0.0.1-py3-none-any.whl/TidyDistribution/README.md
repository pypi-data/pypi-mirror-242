# TidyDistribution
使用Scipy库实现统计分布的简洁程序库，纯代码封装不含任何技术含量

## 使用示例

```python
# 导入模块
>>> from TidyDistribution import TidyDistribution
>>> from TidyDistribution import TidyProbability
>>> from TidyDistribution import TidyQuantile
>>> from TidyDistribution import TidyRandom
>>> from TidyDistribution import TidySample
>>> import numpy as np
```

### 正态分布的分布函数
```python
>>> x = np.linspace(-1, 1, 10)
>>> y1 = TidyDistribution(x, whichdist="norm")
>>> print(y1)
>>> y2 = TidyDistribution(x, whichdist="norm", loc=3, scale=2)
>>> print(y2)
>>> y3 = TidyDistribution((x-3)/2, whichdist="norm")
>>> print(y3)
```

```plain
array([0.15865525, 0.21835002, 0.28925736, 0.36944134, 0.45576412,
       0.54423588, 0.63055866, 0.71074264, 0.78164998, 0.84134475])
array([0.02275013, 0.02945336, 0.03772018, 0.04779035, 0.05990691,
       0.074307  , 0.09121122, 0.1108118 , 0.13326026, 0.15865525])
array([0.02275013, 0.02945336, 0.03772018, 0.04779035, 0.05990691,
       0.074307  , 0.09121122, 0.1108118 , 0.13326026, 0.15865525])
```

### 正态分布的密度函数
```python
>>> x = np.linspace(-1, 1, 10)
>>> y1 = TidyProbability(x, whichdist="norm")
>>> print(y1)
>>> y2 = TidyProbability(x, whichdist="norm", loc=3, scale=2)
>>> print(y2)
>>> y3 = TidyProbability((x-3)/2, whichdist="norm")/2
>>> print(y3)
```

```plain
array([0.24197072, 0.29481487, 0.34189229, 0.37738323, 0.39648726,
       0.39648726, 0.37738323, 0.34189229, 0.29481487, 0.24197072])
array([0.02699548, 0.03350581, 0.04107594, 0.04973857, 0.0594891 ,
       0.07027806, 0.08200504, 0.09451476, 0.10759623, 0.12098536])
array([0.02699548, 0.03350581, 0.04107594, 0.04973857, 0.0594891 ,
       0.07027806, 0.08200504, 0.09451476, 0.10759623, 0.12098536])
```

### 正态分布的分位数函数
```python
>>> q = np.linspace(0, 1, 10)
>>> y = TidyQuantile(q, whichdist="norm")
>>> print(y)
```

```plain
array([       -inf, -1.22064035, -0.76470967, -0.4307273 , -0.1397103 ,
        0.1397103 ,  0.4307273 ,  0.76470967,  1.22064035,         inf])
```

### 正态分布随机数

```python
>>> size = 10
>>> y = TidyRandom(size=size, random_state=1, whichdist="norm")
>>> print(y)
```

```plain
array([ 1.62434536, -0.61175641, -0.52817175, -1.07296862,  0.86540763,
       -2.3015387 ,  1.74481176, -0.7612069 ,  0.3190391 , -0.24937038])
```

还有其他很多分布，常用的离散型和连续型分布，一元分布，多元分布应有尽有，快尝试一下吧。
