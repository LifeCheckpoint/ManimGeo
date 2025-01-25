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

        # 无穷直线依赖端点
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
        """参数方程, t in R"""
        return self._start.coord + t*(self._through.coord - self._start.coord)
    
class VerticalLine(LineLike):
    def __init__(self, point: PointLike, line: LineLike, name: str = ""):
        super().__init__(name)
        self._point = point
        self._line = line

        # 垂线依赖点和线
        self._point.add_dependent(self)
        self._line.add_dependent(self)

    def _recalculate(self):
        direction = GeoUtils.normalize(self._line.direction).copy()
        base_point = self._point.coord.copy()

        self.direction = np.array([-direction[1], direction[0]])
        self.base_point = base_point

class ParallelLine(LineLike):
    def __init__(self, point: PointLike, line: LineLike, name: str = ""):
        super().__init__(name)
        self._point = point
        self._line = line

        # 平行线依赖点和线
        self._point.add_dependent(self)
        self._line.add_dependent(self)

    def _recalculate(self):
        direction = GeoUtils.normalize(self._line.direction).copy()
        base_point = self._point.coord.copy()

        self.direction = direction
        self.base_point = base_point

class PerpendicularLine(LineLike):
    @overload
    def __init__(self, point1: PointLike, point2: PointLike, name: str = ""):
        super().__init__(name)
        ...

    @overload
    def __init__(self, line: LineSegment, name: str = ""):
        super().__init__(name)
        ...
        
    def __init__(self, point1_or_line: Union[PointLike, LineSegment], point2: PointLike = None, name: str = ""):
        super().__init__(name)

        # 垂线依赖线段
        if isinstance(point1_or_line, LineSegment) and point2 is None:
            line = point1_or_line
            self._point1 = line._start
            self._point2 = line._end
            parents = [line]

        # 垂线依赖点
        elif isinstance(point1_or_line, PointLike) and point2 is not None:
            self._point1 = point1_or_line
            self._point2 = point2
            parents = [self._point1, self._point2]

        else:
            raise ValueError("Invalid input arguments")

        for parent in parents:
            parent.add_dependent(self)

    def _recalculate(self):
        direction = GeoUtils.normalize(self._point2.coord - self._point1.coord).copy()
        self.direction = np.array([-direction[1], direction[0]])
        self.base_point = (self._point1.coord.copy() + self._point2.coord.copy()) / 2

class AngleBisector(LineLike):
    @overload
    def __init__(self, line1: LineLike, line2: LineLike, name: str = ""):
        ...

    @overload
    def __init__(self, center: PointLike, point1: PointLike, point2: PointLike, name: str = ""):
        ...

    def __init__(
        self, 
        line1_or_center: Union[LineLike, PointLike], 
        line2_or_point1: Union[LineLike, PointLike] = None, 
        point2: PointLike = None, 
        name: str = ""
    ):
        super().__init__(name)

        # 角平分线依赖两线
        if isinstance(line1_or_center, LineLike) and isinstance(line2_or_point1, LineLike) and point2 is None:
            self._line1 = line1_or_center
            self._line2 = line2_or_point1
            parents = [self._line1, self._line2]

        # 角平分线依赖三点
        elif isinstance(line1_or_center, PointLike) and isinstance(line2_or_point1, PointLike) and point2 is not None and isinstance(point2, PointLike):
            self._center = line1_or_center
            self._point1 = line2_or_point1
            self._point2 = point2
            parents = [self._center, self._point1, self._point2]

        else:
            raise ValueError("Invalid input arguments")

        for parent in parents:
            parent.add_dependent(self)

    def _recalculate(self):
        if hasattr(self, "_center"):
            # 三点确定角平分线
            direction1 = GeoUtils.normalize(self._point1.coord - self._center.coord).copy()
            direction2 = GeoUtils.normalize(self._point2.coord - self._center.coord).copy()
            self.direction = GeoUtils.normalize(direction1 + direction2)
            self.base_point = self._center.coord
        else:
            # 两线确定角平分线
            direction1 = GeoUtils.normalize(self._line1.direction).copy()
            direction2 = GeoUtils.normalize(self._line2.direction).copy()
            self.direction = GeoUtils.normalize(direction1 + direction2)
            intersection = LineLike.find_intersection(self._line1, self._line2)
            if intersection[0]:
                self.base_point = intersection[1][0]
            else:
                raise ValueError("No intersection found even though infinite lines are given")
