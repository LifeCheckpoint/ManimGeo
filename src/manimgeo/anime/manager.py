from manimgeo.components import *

class GeoManager:
    """管理几何对象向动画对象的转换"""
    start_update: bool

    def __init__(self):
        self.start_update = False
    
    def start_trace(self):
        """
        追踪所有部件几何运动

        等同于 __enter__()

        不同的库中有不同的初始化时机：
         - `ManimGL`: 在执行变换前进入上下文
         - `JAnim`: 在创建对象前进入上下文（创建时已默认开启）
        """
        self.__enter__()

    def stop_trace(self):
        """
        结束 Trace

        等同于 __exit__()
        """
        self.__exit__()

    def __enter__(self):
        """
        追踪所有部件几何运动
        
        不同的库中有不同的初始化时机：
         - `ManimGL`: 在执行变换前进入上下文
         - `JAnim`: 在创建对象前进入上下文（创建时已默认开启）
        """
        self.start_update = True

    def __exit__(self, exc_type, exc_value, traceback):
        """
        结束 Trace
        """
        self.start_update = False
