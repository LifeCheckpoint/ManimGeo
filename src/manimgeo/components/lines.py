from manimgeo.components.base import BaseGeometryLike, PointLike, LineLike
from manimgeo.components.points import ImplicitPoint
from manimgeo.utils.utils import GeoUtils

from typing import overload, Union, List, Literal
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

class TangentLine(BaseGeometryLike):
    from manimgeo.components.conic_section import Circle, ThreePointCircle

    _lines: List[LineLike]

    @property
    def lines(self) -> List[LineLike]:
        return self._lines
    
    @lines.setter
    def lines(self, value: List[LineLike]):
        self._lines = value

    def _is_on_circle(self) -> Literal[-1, 0, 1]:
        eps = 1e-7
        if np.linalg.norm(self._point.coord - self._circle.center) < self._circle.radius - eps:
            return -1
        elif np.linalg.norm(self._point.coord - self._circle.center) - self._circle.radius < eps:
            return 0    
        else:
            return 1

    def __init__(self, circle: Union[Circle, ThreePointCircle], point: PointLike, name: str = ""):
        """过一点的圆切线"""
        super().__init__(name)
        self._circle = circle
        self._point: PointLike = point
        self._lines: List[LineLike] = []

        if self._is_on_circle() == -1:
            # 点在圆内
            raise ValueError("The point is inside the circle")
        
        elif self._is_on_circle() >= 0:
            # 点在圆上或圆外
            self._lines = [
                LineSegment(self._point, np.array([1, 0]), f"{name}_tangent@{id(self)}_0"),
                LineSegment(self._point, np.array([1, 0]), f"{name}_tangent@{id(self)}_1")
            ]

        # 切线依赖圆和点
        for line in self._lines:
            self._circle.add_dependent(line)
            self._point.add_dependent(line)

    def _recalculate(self):
        on_circle = self._is_on_circle()
        
        # 圆上，将两条线同理处理
        if on_circle == 0:
            cx, cy = self._circle.center  # 圆心 (x_c, y_c)
            px, py = self._point.coord    # 圆上点 (x_p, y_p)
            # 计算半径向量 (Δx, Δy)
            dx = px - cx
            dy = py - cy
            # 计算切线方向向量（两个可能的方向）
            self._lines[0].direction = (-dy, dx)
            self._lines[0].base_point = self._point.coord
            self._lines[1].direction = (-dy, dx)
            self._lines[1].base_point = self._point.coord

        # 圆外，计算切线
        if on_circle == 1:
            cx, cy = self._circle.center
            px, py = self._point.coord
            r = self._circle.radius
            
            # 计算向量CP的坐标差和长度
            dx = px - cx
            dy = py - cy
            d_squared = dx ** 2 + dy ** 2
            
            r_squared_over_d_squared = (r ** 2) / d_squared
            sqrt_term = np.sqrt(d_squared - r ** 2)
            coeff = r * sqrt_term / d_squared  # 垂直分量的系数
            
            # 计算两个切点的坐标
            tx1 = cx + r_squared_over_d_squared * dx - coeff * dy
            ty1 = cy + r_squared_over_d_squared * dy + coeff * dx
            tx2 = cx + r_squared_over_d_squared * dx + coeff * dy
            ty2 = cy + r_squared_over_d_squared * dy - coeff * dx
            
            self._lines[0].direction = np.array([-(ty1 - cy), tx1 - cx])
            self._lines[0].base_point = self._point.coord
            self._lines[1].direction = np.array([-(ty2 - cy), tx2 - cx])
            self._lines[1].base_point = self._point.coord

        # 圆内
        else:
            raise ValueError("The point is inside the circle")
