import numpy as np
import pandas as pd


def TidySample(
        sequenceobj=None,
        size=None,
        frac=None,
        isreplace=0,
        weight_p=None,
        random_state=None):
    """
    这是一个随机抽样函数的文档字符串。

    参数:
    sequenceobj (1D-ndarray or list or df or series): ndarray数组或者列表或者dataframe或者Series对象。
    size (int): 要抽取的样本量大小。
    frac (float): 抽样比例。
    isreplace (binary): 是否有放回地重复抽样{1,0}。
    weight_p (list or 1D-ndarray): 抽样概率的权重。
    random_state (int): 随机数种子。

    返回:
    ndarray或者list或者dataframe或者series，对应与sequenceobj的类型。

    示例:
    ===============================================================================0
    导入模块
    >>> from TidyStats import TidySample
    >>> import numpy as np
    >>> import pandas as pd
    ===============================================================================1
    ndarray对象测试
    ===============================================================================2
    不指定随机数种子
    >>> arr = np.arange(10)
    >>> res = TidySample(arr)
    >>> print(res)
    ===============================================================================3
    指定随机数种子
    >>> arr = np.arange(10)
    >>> res = TidySample(arr, random_state=10)
    >>> print(res)
    ===============================================================================4
    指定抽样大小
    >>> arr = np.arange(10)
    >>> res = TidySample(arr, size=4)
    >>> print(res)
    ===============================================================================5
    有放回抽样
    >>> arr = np.arange(10)
    >>> res = TidySample(arr, size=10, isreplace=1)
    >>> print(res)
    ===============================================================================6
    指定抽样比例
    >>> arr = np.arange(10)
    >>> res = TidySample(arr, frac=0.4, isreplace=1)
    >>> print(res)
    ===============================================================================7
    指定抽样概率
    >>> arr = np.arange(10)
    >>> res = TidySample(arr, frac=0.4, weight_p=[0,0,0,0,0,0,0.1,0.1,0.2,0.6])
    >>> print(res)
    ===============================================================================8
    列表对象测试
    ===============================================================================9
    不指定随机数种子
    >>> lst = [i for i in range(10)]
    >>> res = TidySample(lst)
    >>> print(res)
    ===============================================================================10
    指定随机数种子
    >>> lst = [i for i in range(10)]
    >>> res = TidySample(lst, random_state=10)
    >>> print(res)
    ===============================================================================11
    指定抽样大小
    >>> lst = [i for i in range(10)]
    >>> res = TidySample(lst, size=4)
    >>> print(res)
    ===============================================================================12
    有放回抽样
    >>> lst = [i for i in range(10)]
    >>> res = TidySample(lst, size=10, isreplace=1)
    >>> print(res)
    ===============================================================================13
    指定抽样比例
    >>> lst = [i for i in range(10)]
    >>> res = TidySample(lst, frac=0.4, isreplace=1)
    >>> print(res)
    ===============================================================================14
    指定抽样概率
    >>> lst = [i for i in range(10)]
    >>> res = TidySample(lst, frac=0.4, weight_p=[0,0,0,0,0,0,0.1,0.1,0.2,0.6])
    >>> print(res)
    ===============================================================================15
    DataFrame对象测试
    ===============================================================================16
    不指定随机数种子
    >>> df = pd.DataFrame({"x": [i for i in range(10)], "y": [i**2 for i in range(10)]})
    >>> res = TidySample(df)
    >>> print(res)
    ===============================================================================17
    指定随机数种子
    >>> df = pd.DataFrame({"x": [i for i in range(10)], "y": [i**2 for i in range(10)]})
    >>> res = TidySample(df, random_state=10)
    >>> print(res)
    ===============================================================================18
    指定抽样大小
    >>> df = pd.DataFrame({"x": [i for i in range(10)], "y": [i**2 for i in range(10)]})
    >>> res = TidySample(df, size=4)
    >>> print(res)
    ===============================================================================19
    有放回抽样
    >>> df = pd.DataFrame({"x": [i for i in range(10)], "y": [i**2 for i in range(10)]})
    >>> res = TidySample(df, size=10, isreplace=1)
    >>> print(res)
    ===============================================================================20
    指定抽样比例
    >>> df = pd.DataFrame({"x": [i for i in range(10)], "y": [i**2 for i in range(10)]})
    >>> res = TidySample(df, frac=0.4, isreplace=1)
    >>> print(res)
    ===============================================================================21
    指定抽样概率
    >>> df = pd.DataFrame({"x": [i for i in range(10)], "y": [i**2 for i in range(10)]})
    >>> res = TidySample(df, frac=0.4, weight_p=[0,0,0,0,0,0,0.1,0.1,0.2,0.6])
    >>> print(res)
    ===============================================================================22
    Series对象测试
    ===============================================================================23
    不指定随机数种子
    >>> s = pd.Series([i%3 for i in range(10, 20)])
    >>> res = TidySample(s)
    >>> print(res)
    ===============================================================================24
    指定随机数种子
    >>> s = pd.Series([i%3 for i in range(10, 20)])
    >>> res = TidySample(s, random_state=10)
    >>> print(res)
    ===============================================================================25
    指定抽样大小
    >>> s = pd.Series([i%3 for i in range(10, 20)])
    >>> res = TidySample(s, size=4)
    >>> print(res)
    ===============================================================================26
    有放回抽样
    >>> s = pd.Series([i%3 for i in range(10, 20)])
    >>> res = TidySample(s, size=10, isreplace=1)
    >>> print(res)
    ===============================================================================27
    指定抽样比例
    >>> s = pd.Series([i%3 for i in range(10, 20)])
    >>> res = TidySample(s, frac=0.4, isreplace=1)
    >>> print(res)
    ===============================================================================28
    指定抽样概率
    >>> s = pd.Series([i%3 for i in range(10, 20)])
    >>> res = TidySample(s, frac=0.4, weight_p=[0,0,0,0,0,0,0.1,0.1,0.2,0.6])
    >>> print(res)
    ===============================================================================29
    """
    res = None
    if isinstance(sequenceobj, np.ndarray) or isinstance(sequenceobj, list):
        if random_state is None:
            pass
        else:
            np.random.seed(random_state)
        if size is None and frac is None:
            res = np.random.choice(sequenceobj, size=1,
                                   replace=bool(isreplace), p=weight_p)
        elif size is not None and frac is None:
            res = np.random.choice(
                sequenceobj, size=size, replace=bool(isreplace), p=weight_p)
        elif size is None and frac is not None:
            res = np.random.choice(sequenceobj, size=int(
                frac * len(sequenceobj)), replace=bool(isreplace), p=weight_p)
        else:
            pass
    elif isinstance(sequenceobj, pd.DataFrame) or isinstance(sequenceobj, pd.Series):
        if size is None and frac is None:
            res = sequenceobj.sample(n=1, frac=frac, replace=bool(
                isreplace), weights=weight_p, random_state=random_state)
        elif size is not None and frac is None:
            res = sequenceobj.sample(n=size, frac=frac, replace=bool(
                isreplace), weights=weight_p, random_state=random_state)
        elif size is None and frac is not None:
            res = sequenceobj.sample(n=size, frac=frac, replace=bool(
                isreplace), weights=weight_p, random_state=random_state)
        else:
            pass
    else:
        pass
    return res
