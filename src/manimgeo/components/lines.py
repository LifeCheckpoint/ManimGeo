from manimgeo.components.base import PointLike, LineLike
from manimgeo.components.points import ImplicitPoint
from manimgeo.utils.utils import GeoUtils

from typing import overload, Union
import numpy as np

class LineSegment(LineLike):
    """线段类型"""
    def __init__(self, start: PointLike, end: PointLike, name: str = ""):
        super().__init__(name)
        self._start = start
        self._end = end

        # 线段依赖端点
        self._start.add_dependent(self)
        self._end.add_dependent(self)

    def _recalculate(self):
        self.direction = GeoUtils.normalize(self._end.coord - self._start.coord)
        self.base_point = self._start.coord

    def parametric(self, t: float) -> np.ndarray:
        """参数方程, 0 <= t <= 1"""
        return self._start.coord + t*(self._end.coord - self._start.coord)

class Ray(LineLike):
    """射线类型"""
    @overload
    def __init__(self, start: PointLike, through: PointLike, name: str = ""):
        ...

    @overload
    def __init__(self, start: PointLike, direction: np.ndarray, name: str = ""):
        ...
    
    def __init__(self, start: PointLike, through_or_direction: Union[PointLike, np.ndarray], name: str = ""):
        super().__init__(name)

        if isinstance(through_or_direction, PointLike):
            self._start = start
            self._through = through_or_direction
        else:
            self._start = start
            self.direction = GeoUtils.normalize(through_or_direction)
            self._through = ImplicitPoint(self._start.coord + self.direction, f"{name}_through@{id(self)}") # 建立一个隐式点

        # 射线依赖端点
        self._start.add_dependent(self)
        self._through.add_dependent(self)

    def _recalculate(self):
        direction = GeoUtils.normalize(self._through.coord - self._start.coord).copy()
        base_point = self._start.coord.copy()

        self.direction = direction
        self.base_point = base_point
        # 同时更新隐式点
        self._through.coord = base_point + direction

    def parametric(self, t: float) -> np.ndarray:
        """参数方程, t >= 0"""
        return self._start.coord + t*(self._through.coord - self._start.coord)

class InfinityLine(LineLike):
    pass