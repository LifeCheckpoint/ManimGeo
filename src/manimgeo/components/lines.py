from manimgeo.components.base import PointLike, LineLike
from manimgeo.utils.utils import GeoUtils

import numpy as np

class LineSegmentPP(LineLike):
    """线段类型（两点）"""
    def __init__(self, start: PointLike, end: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"LineSegment@{id(self)}")

        if np.allclose(start.coord, end.coord):
            raise ValueError(f"For line {self.name}, Points {start.name} and {end.name} causing degenerating")
        
        self.start = start
        self.end = end

        # 线段依赖端点
        self.start.add_dependent(self)
        self.end.add_dependent(self)

    def _recalculate(self):
        # 几何依赖自动更新，无需重算
        pass

class RayPP(LineLike):
    """射线类型（两点）"""
    def __init__(self, start: PointLike, end: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"RayPP@{id(self)}")

        if np.allclose(start.coord, end.coord):
            raise ValueError(f"For line {self.name}, Points {start.name} and {end.name} causing degenerating")
        
        self.start = start
        self.end = end

        # 线段依赖端点
        self.start.add_dependent(self)
        self.end.add_dependent(self)

    def _recalculate(self):
        # 几何依赖自动更新，无需重算
        pass

class InfinityLinePP(LineLike):
    """直线类型（两点）"""
    
    def __init__(self, start: PointLike, end: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"InfinityLinePP@{id(self)}")

        if np.allclose(start.coord, end.coord):
            raise ValueError(f"For line {self.name}, Points {start.name} and {end.name} causing degenerating")

        self.start = start
        self.end = end

        # 无穷直线依赖端点
        self.start.add_dependent(self)
        self.end.add_dependent(self)

    def _recalculate(self):
        # 几何依赖自动更新，无需重算
        pass

# class TangentLine(BaseGeometryLike):
#     from manimgeo.components.conic_section import Circle, ThreePointCircle

#     _lines: List[LineLike]

#     @property
#     def lines(self) -> List[LineLike]:
#         return self._lines
    
#     @lines.setter
#     def lines(self, value: List[LineLike]):
#         self._lines = value

#     def _is_on_circle(self) -> Literal[-1, 0, 1]:
#         eps = 1e-7
#         if np.linalg.norm(self._point.coord - self._circle.center) < self._circle.radius - eps:
#             return -1
#         elif np.linalg.norm(self._point.coord - self._circle.center) - self._circle.radius < eps:
#             return 0    
#         else:
#             return 1

#     def __init__(self, circle: Union[Circle, ThreePointCircle], point: PointLike, name: str = ""):
#         """过一点的圆切线"""
#         super().__init__(name)
#         self._circle = circle
#         self._point: PointLike = point
#         self._lines: List[LineLike] = []

#         if self._is_on_circle() == -1:
#             # 点在圆内
#             raise ValueError("The point is inside the circle")
        
#         elif self._is_on_circle() >= 0:
#             # 点在圆上或圆外
#             self._lines = [
#                 LineSegment(self._point, np.array([1, 0]), f"{name}_tangent@{id(self)}_0"),
#                 LineSegment(self._point, np.array([1, 0]), f"{name}_tangent@{id(self)}_1")
#             ]

#         # 切线依赖圆和点
#         for line in self._lines:
#             self._circle.add_dependent(line)
#             self._point.add_dependent(line)

#     def _recalculate(self):
#         on_circle = self._is_on_circle()
        
#         # 圆上，将两条线同理处理
#         if on_circle == 0:
#             cx, cy = self._circle.center  # 圆心 (x_c, y_c)
#             px, py = self._point.coord    # 圆上点 (x_p, y_p)
#             # 计算半径向量 (Δx, Δy)
#             dx = px - cx
#             dy = py - cy
#             # 计算切线方向向量（两个可能的方向）
#             self._lines[0].direction = (-dy, dx)
#             self._lines[0].base_point = self._point.coord
#             self._lines[1].direction = (-dy, dx)
#             self._lines[1].base_point = self._point.coord

#         # 圆外，计算切线
#         if on_circle == 1:
#             cx, cy = self._circle.center
#             px, py = self._point.coord
#             r = self._circle.radius
            
#             # 计算向量CP的坐标差和长度
#             dx = px - cx
#             dy = py - cy
#             d_squared = dx ** 2 + dy ** 2
            
#             r_squared_over_d_squared = (r ** 2) / d_squared
#             sqrt_term = np.sqrt(d_squared - r ** 2)
#             coeff = r * sqrt_term / d_squared  # 垂直分量的系数
            
#             # 计算两个切点的坐标
#             tx1 = cx + r_squared_over_d_squared * dx - coeff * dy
#             ty1 = cy + r_squared_over_d_squared * dy + coeff * dx
#             tx2 = cx + r_squared_over_d_squared * dx + coeff * dy
#             ty2 = cy + r_squared_over_d_squared * dy - coeff * dx
            
#             self._lines[0].direction = np.array([-(ty1 - cy), tx1 - cx])
#             self._lines[0].base_point = self._point.coord
#             self._lines[1].direction = np.array([-(ty2 - cy), tx2 - cx])
#             self._lines[1].base_point = self._point.coord

#         # 圆内
#         else:
#             raise ValueError("The point is inside the circle")
