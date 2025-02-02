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
        """
        self.start_update = True

    def __exit__(self, exc_type, exc_value, traceback):
        """
        结束 Trace
        """
        self.start_update = False
