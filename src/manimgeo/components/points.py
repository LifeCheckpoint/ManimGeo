from manimgeo.components.base import PointLike, LineLike
from manimgeo.utils.utils import GeoUtils

from typing import List, overload, Optional, Union
import numpy as np

class FreePoint(PointLike):
    """自由点类型（叶子节点）"""
    def __init__(self, coord: np.ndarray, name: str = ""):
        super().__init__(name)
        self.coord = coord

    def _recalculate(self):
        pass

class ImplicitPoint(PointLike):
    """隐式点类型（非叶子节点）"""
    def __init__(self, coord: np.ndarray, name: str = ""):
        super().__init__(name)
        self.coord = coord

    def _recalculate(self):
        pass

class MidPoint(PointLike):
    """中点类型（构造点）"""
    @overload
    def __init__(self, line: LineLike, name: str = ""):
        """构造线段的中点"""
        ...
    
    @overload
    def __init__(self, start: PointLike, end: PointLike, name: str = ""):
        """构造两点的中点"""
        ...
    
    def __init__(self, line_or_start: Union[LineLike, PointLike], end: Optional[PointLike] = None, name: str = ""):
        super().__init__(name)
        from manimgeo.components.lines import LineSegment  # 延迟导入

        # 依赖于线段
        if isinstance(line_or_start, LineSegment) and end is None:
            line = line_or_start
            self.start = line._start
            self.end = line._end
            parents = [line]

        # 依赖于两点
        elif end is not None and isinstance(line_or_start, PointLike):
            self.start = line_or_start
            self.end = end
            parents = [self.start, self.end]
            
        else:
            raise ValueError("Invalid input arguments")

        for parent in parents:
            parent.add_dependent(self)

    def _recalculate(self):
        self.coord = (self.start.coord + self.end.coord) / 2

class ExtensionPoint(PointLike):
    """延长点类型"""
    def __init__(self, start: PointLike, end: PointLike, factor: float = 2.0, name: str = ""):
        super().__init__(name)
        self.factor = factor
        self.start = start
        self.end = end
        
        self.start.add_dependent(self)
        self.end.add_dependent(self)

    def _recalculate(self):
        self.coord = self.start.coord + self.factor*(self.end.coord - self.start.coord)

class IntersectionPoint(PointLike):
    """交点"""
    def __init__(self, line1: LineLike, line2: LineLike, name: str = ""):
        super().__init__(name)
        self.line1 = line1
        self.line2 = line2
        
        self.line1.add_dependent(self)
        self.line2.add_dependent(self)

    def _recalculate(self):
        has_intersection, res = LineLike.find_intersection(self.line1, self.line2)
        if has_intersection:
            self.coord = res[0]
        else:
            raise ValueError("No intersection found")
        
class AxisymmetricPoint(PointLike):
    """轴对称点"""
    def __init__(self, point: PointLike, line: LineLike, name: str = ""):
        super().__init__(name)
        self.point = point
        self.line = line
        
        self.point.add_dependent(self)
        self.line.add_dependent(self)

    def _recalculate(self):
        # 将方向向量归一化为单位向量
        u = GeoUtils.normalize(self.line.direction)
        base = self.line.base_point
        # 计算点相对于基点的向量
        ap = self.point.coord - base
        # 计算投影长度（点积）
        projection_length = np.dot(ap, u)
        # 投影向量
        proj_vec = projection_length * u
        # 计算投影点坐标
        q = base + proj_vec
        # 对称点坐标为投影点向量的两倍减去原坐标
        self.coord = 2 * q - self.point.coord

class TranslationPoint(PointLike):
    """平移点"""
    def __init__(self, point: PointLike, vector: np.ndarray, name: str = ""):
        super().__init__(name)
        self.point = point
        self.vector = vector

        self.point.add_dependent(self)

    def _recalculate(self):
        self.coord = self.point.coord + self.vector

class RotationPoint(PointLike):
    """旋转点"""
    def __init__(self, point: PointLike, center: PointLike, angle: float, name: str = ""):
        super().__init__(name)
        self.point = point
        self.center = center
        self.angle = angle

        self.point.add_dependent(self)
        self.center.add_dependent(self)

    def _recalculate(self):
        # 计算旋转矩阵
        rot_matrix = np.array([[np.cos(self.angle), -np.sin(self.angle)],
                               [np.sin(self.angle), np.cos(self.angle)]])
        # 计算相对于中心的坐标
        relative_coord = self.point.coord - self.center.coord
        # 计算旋转后的坐标
        self.coord = np.dot(rot_matrix, relative_coord) + self.center.coord

class InversionPoint(PointLike):
    """反演点"""
    from manimgeo.components.conic_section import Circle, ThreePointCircle

    def __init__(self, point: PointLike, circle: Union[Circle, ThreePointCircle], radius: float, name: str = ""):
        super().__init__(name)
        self._point = point
        self._circle = circle

        self._point.add_dependent(self)
        self._circle.add_dependent(self)

    def _recalculate(self):
        op = self._point.coord - self._circle.center
        d_squared = np.dot(op, op)
        if d_squared == 0:
            raise ValueError("Point p coincides with the center, inversion undefined.")
        k = (self._circle.radius ** 2) / d_squared
        self.coord = self._circle.center + op * k