from ..utils.config import GeoConfig
from typing import Union
import functools
import numpy as np

type Number = Union[int, float]
cfg = GeoConfig()

def close(a: Union[np.ndarray, Number], b: Union[np.ndarray, Number]) -> bool:
    """
    判断两个数值是否相近
    """
    if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
        return np.allclose(a, b, atol=cfg.atol, rtol=cfg.rtol)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if np.isnan(a) or np.isnan(b):
            return False # NaN 永远不等于任何值，包括自身
        if np.isinf(a) and np.isinf(b):
            return (a == b) # 只有符号相同才相等 (inf == inf, -inf == -inf)
        if np.isinf(a) or np.isinf(b):
            return False # 一个是无穷大，另一个是有限数，则不相等
        return abs(a - b) <= cfg.atol + cfg.rtol * abs(b)
    else:
        raise TypeError("不允许比较类型不同的两个数据是否一致: {} and {}".format(type(a), type(b)))
    
def array2float(func):
    """
    将参数中所有 np.ndarray 类型的参数自动转换为 float64
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        processed_args = []

        # 处理位置参数
        for arg in args:
            if isinstance(arg, np.ndarray) and not np.issubdtype(arg.dtype, np.floating):
                processed_args.append(arg.astype(np.float64))
            else:
                processed_args.append(arg)
        processed_kwargs = {}
        
        # 处理关键字参数
        for k, v in kwargs.items():
            if isinstance(v, np.ndarray) and not np.issubdtype(v.dtype, np.floating):
                processed_kwargs[k] = v.astype(np.float64)
            else:
                processed_kwargs[k] = v
        return func(*processed_args, **processed_kwargs)

    return wrapper