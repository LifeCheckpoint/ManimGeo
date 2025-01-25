from manimgeo.components.base import PointLike, LineLike
from manimgeo.components.vector import VectorParam
from manimgeo.components.angle import AnglePP
from manimgeo.utils.utils import GeoUtils

from typing import List, overload, Optional, Union
import numpy as np

class FreePoint(PointLike):
    """自由点类型（叶子节点）"""
    def __init__(self, coord: np.ndarray, name: str = ""):
        super().__init__(name)
        self._coord = coord

    def _recalculate(self):
        # 自由点无需重新计算
        pass

class MidPointPP(PointLike):
    """中点类型（两点）"""
    point1: PointLike
    point2: PointLike

    def __init__(self, point1: PointLike, point2: PointLike, name: str = ""):
        super().__init__(name)
        self.point1 = point1
        self.point2 = point2

        self.point1.add_dependent(self)
        self.point2.add_dependent(self)

    def _recalculate(self):
        self._coord = (self.point1.coord + self.point2.coord) / 2

class MidPointL(PointLike):
    """中点类型（线段）"""
    from manimgeo.components.lines import LineSegment
    line: LineLike

    def __init__(self, line: LineSegment, name: str = ""):
        super().__init__(name)

        # 依赖于线段
        self.line = line
        self.line.add_dependent(self)

    def _recalculate(self):
        self._coord = (self.line.start.coord + self.line.end.coord) / 2

class ExtensionPointPP(PointLike):
    """延长点类型"""
    start_point: PointLike
    through_point: PointLike
    _factor: float

    @property
    def factor(self) -> float:
        """延长因子"""
        return self._factor
    
    @factor.setter
    def factor(self, value: float):
        self.update()
        self._factor = value

    def __init__(self, start_point: PointLike, through_point: PointLike, factor: float = 2.0, name: str = ""):
        super().__init__(name)
        self._factor = factor
        self.start_point = start_point
        self.through_point = through_point
        
        self.start_point.add_dependent(self)
        self.through_point.add_dependent(self)

    def _recalculate(self):
        self._coord = self.start_point.coord + self._factor*(self.through_point.coord - self.start_point.coord)

class IntersectionPointLL(PointLike):
    """两线交点"""
    line1: LineLike
    line2: LineLike

    def __init__(self, line1: LineLike, line2: LineLike, name: str = ""):
        super().__init__(name)
        self.line1 = line1
        self.line2 = line2
        
        self.line1.add_dependent(self)
        self.line2.add_dependent(self)

    def _recalculate(self):
        has_intersection, res = LineLike.find_intersection(self.line1, self.line2)
        if has_intersection and len(res) == 1:
            self.coord = res[0]
        elif has_intersection and len(res) >= 1:
            raise ValueError("Multiple intersections found")
        else:
            raise ValueError("No intersection found")
        
class AxisymmetricPointPL(PointLike):
    """轴对称点"""
    point: PointLike
    line: LineLike

    def __init__(self, point: PointLike, line: LineLike, name: str = ""):
        super().__init__(name)
        self.point = point
        self.line = line
        
        self.point.add_dependent(self)
        self.line.add_dependent(self)

    def _recalculate(self):
        u = GeoUtils.unit_direction_vector(self.line.start.coord, self.line.end.coord) # 单位方向向量
        base = self.line.start.coord # 基点
        ap = self.point.coord - base # 点相对于基点的向量
        projection_length = np.dot(ap, u) # 计算投影长度
        proj_vec = projection_length * u # 投影向量
        q = base + proj_vec # 投影点坐标
        self._coord = 2 * q - self.point.coord # 对称点坐标为投影点向量的两倍减去原坐标

class TranslationPoint(PointLike):
    """平移点"""
    point: PointLike
    vector: VectorParam

    def __init__(self, point: PointLike, vector: VectorParam, name: str = ""):
        super().__init__(name)
        self.point = point
        self.vector = vector

        self.point.add_dependent(self)
        self.vector.add_dependent(self)

    def _recalculate(self):
        self._coord = self.point.coord + self.vector.vector

class RotationPoint(PointLike):
    """旋转点"""
    point: PointLike
    center: PointLike
    angle: AnglePP

    def __init__(self, point: PointLike, center: PointLike, angle: AnglePP, name: str = ""):
        super().__init__(name)
        self.point = point
        self.center = center
        self.angle = angle

        self.point.add_dependent(self)
        self.center.add_dependent(self)
        self.angle.add_dependent(self)

    def _recalculate(self):
        angle = self.angle.angle
        # 计算旋转矩阵
        rot_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                               [np.sin(angle), np.cos(angle)]])
        # 计算相对于中心的坐标
        relative_coord = self.point.coord - self.center.coord
        # 计算旋转后的坐标
        self._coord = np.dot(rot_matrix, relative_coord) + self.center.coord

# class InversionPoint(PointLike):
#     """反演点"""
#     from manimgeo.components.conic_section import Circle, ThreePointCircle

#     def __init__(self, point: PointLike, circle: Union[Circle, ThreePointCircle], radius: float, name: str = ""):
#         super().__init__(name)
#         self._point = point
#         self._circle = circle

#         self._point.add_dependent(self)
#         self._circle.add_dependent(self)

#     def _recalculate(self):
#         op = self._point.coord - self._circle.center
#         d_squared = np.dot(op, op)
#         if d_squared == 0:
#             raise ValueError("Point p coincides with the center, inversion undefined.")
#         k = (self._circle.radius ** 2) / d_squared
#         self.coord = self._circle.center + op * k