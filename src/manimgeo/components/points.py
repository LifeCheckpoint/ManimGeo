from manimgeo.components.base import BaseGeometry, PointLike, LineLike
from manimgeo.components.vector import VectorParam, VectorPP
from manimgeo.components.angle import AnglePP
from manimgeo.utils.utils import GeoUtils

from typing import Union, TypeAlias
import numpy as np

class FreePoint(PointLike):
    """## 构造自由点（叶子节点）"""
    def __init__(self, coord: np.ndarray, name: str = ""):
        super().__init__(name if name is not "" else f"FreePoint@{id(self)}")
        self._coord = coord

    def _recalculate(self):
        # 自由点无需重新计算
        pass

class ConstraintPoint(PointLike):
    """## 构造约束点（非叶子节点）"""
    def __init__(self, coord: np.ndarray, name: str = ""):
        super().__init__(name if name is not "" else f"ConstraintPoint@{id(self)}")
        self._coord = coord

    def _recalculate(self):
        # 自由点无需重新计算
        pass

class MidPointPP(PointLike):
    """## 构造中点（两点）"""
    point1: PointLike
    point2: PointLike

    def __init__(self, point1: PointLike, point2: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"MidPoint@{id(self)}")
        self.point1 = point1
        self.point2 = point2

        self.point1.add_dependent(self)
        self.point2.add_dependent(self)

    def _recalculate(self):
        self._coord = (self.point1.coord + self.point2.coord) / 2

class MidPointL(PointLike):
    """## 构造中点（线段）"""
    from manimgeo.components.lines import LineSegmentPP
    line: LineLike

    def __init__(self, line: LineSegmentPP, name: str = ""):
        super().__init__(name if name is not "" else f"MidPointL@{id(self)}")

        # 依赖于线段
        self.line = line
        self.line.add_dependent(self)

    def _recalculate(self):
        self._coord = (self.line.start.coord + self.line.end.coord) / 2

class ExtensionPointPP(PointLike):
    """## 构造延长（位似）点"""
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
        super().__init__(name if name is not "" else f"ExtensionPointPP@{id(self)}")
        self._factor = factor
        self.start_point = start_point
        self.through_point = through_point
        
        self.start_point.add_dependent(self)
        self.through_point.add_dependent(self)

    def _recalculate(self):
        self._coord = self.start_point.coord + self._factor*(self.through_point.coord - self.start_point.coord)
        
class AxisymmetricPointPL(PointLike):
    """## 构造轴对称点"""
    point: PointLike
    line: LineLike

    def __init__(self, point: PointLike, line: LineLike, name: str = ""):
        super().__init__(name if name is not "" else f"AxisymmetricPointPL@{id(self)}")
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

class TranslationPointP(PointLike):
    """## 构造平移点"""
    point: PointLike
    vector: Union[VectorParam, VectorPP]

    def __init__(self, point: PointLike, vector: Union[VectorParam, VectorPP], name: str = ""):
        super().__init__(name if name is not "" else f"TranslationPoint@{id(self)}")
        self.point = point
        self.vector = vector

        self.point.add_dependent(self)
        self.vector.add_dependent(self)

    def _recalculate(self):
        self._coord = self.point.coord + self.vector.vector

class RotationPointPPA(PointLike):
    """## 构造旋转点"""
    point: PointLike
    center: PointLike
    angle: AnglePP

    def __init__(self, point: PointLike, center: PointLike, angle: AnglePP, name: str = ""):
        super().__init__(name if name is not "" else f"RotationPoint@{id(self)}")
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

class VerticalPointPL(PointLike):
    """## 构造垂点"""
    point: PointLike
    line: LineLike

    def __init__(self, point: PointLike, line: LineLike, name: str = ""):
        super().__init__(name if name is not "" else f"VerticalPoint@{id(self)}")
        self.point = point
        self.line = line

        self.point.add_dependent(self)
        self.line.add_dependent(self)

    def _recalculate(self):
        direction = GeoUtils.unit_direction_vector(self.line.start.coord, self.line.end.coord)
        projection_scalar = np.dot(self.point.coord - self.line.start.coord, direction)
        self._coord = self.line.start.coord + projection_scalar * direction

class ParallelPointPL(PointLike):
    """## 构造平行点"""
    point: PointLike
    line: LineLike
    _distance: float

    @property
    def distance(self) -> float:
        """构造距离"""
        return self._distance
    
    @distance.setter
    def distance(self, value: float):
        self.update()
        self._distance = value

    def __init__(self, point: PointLike, line: LineLike, distance: float = 1.0, name: str = ""):
        super().__init__(name if name is not "" else f"ParallelPointPL@{id(self)}")
        self.point = point
        self.line = line
        self._distance = distance

        self.point.add_dependent(self)
        self.line.add_dependent(self)

    def _recalculate(self):
        direction = GeoUtils.unit_direction_vector(self.line.start.coord, self.line.end.coord)
        self._coord = self.point.coord + self._distance*direction

class AngleBisectorPointPPP(PointLike):
    pass

class InversionPointPCir(PointLike):
    """## 构造反演点"""
    from manimgeo.components.conic_section import CircleP, CirclePP, CirclePPP
    Circles: TypeAlias = Union[CircleP, CirclePP, CirclePPP]

    point: PointLike
    circle: Circles

    def __init__(self, point: PointLike, circle: Circles, name: str = ""):
        super().__init__(name if name is not "" else f"InversionPointCir@{id(self)}")
        self.point = point
        self.circle = circle

        self.point.add_dependent(self)
        self.circle.add_dependent(self)

    def _recalculate(self):
        # 对于 PPP
        from manimgeo.components.conic_section import CirclePPP
        center_coord = self.circle.center_point.coord if not isinstance(self.circle, CirclePPP) else self.circle.center
        radius = np.linalg.norm(self.circle.center_point.coord - self.circle.point.coord) if not isinstance(self.circle, CirclePPP) else self.circle.radius

        op = self.point.coord - center_coord
        d_squared = np.dot(op, op)
        if d_squared == 0:
            raise ValueError("Point p coincides with the center, inversion undefined.")
        k = (radius ** 2) / d_squared
        self._coord = center_coord + op * k

class IntersectionPointLL(PointLike):
    """## 构造两线交点"""
    line1: LineLike
    line2: LineLike

    def __init__(self, line1: LineLike, line2: LineLike, name: str = ""):
        super().__init__(name if name is not "" else f"IntersectionPointLL@{id(self)}")
        self.line1 = line1
        self.line2 = line2
        
        self.line1.add_dependent(self)
        self.line2.add_dependent(self)

    def _recalculate(self):
        has_intersection, res = LineLike.find_intersection(self.line1, self.line2)
        if has_intersection and len(res) == 1:
            self.coord = res[0]
        elif has_intersection and len(res) >= 1:
            raise ValueError(f"For {self.line1.name} and {self.line2.name}, Multiple intersections found")
        else:
            raise ValueError(f"For {self.line1.name} and {self.line2.name}, No intersection found")

class IntersectionPointLCir(BaseGeometry):
    """
    ## 构造线与圆交点
    
    通过 `point1` `point2` 访问两个约束得到的交点，未添加线段范围限制
    """
    from manimgeo.components.conic_section import CircleP, CirclePP, CirclePPP
    Circles: TypeAlias = Union[CircleP, CirclePP, CirclePPP]

    line: LineLike
    circle: Circles
    _point1: PointLike
    _point2: PointLike

    @property
    def point1(self) -> PointLike:
        if self.ret_updated:
            self._recalculate()
            self.ret_updated = False
        return self._point1
    
    @point1.setter
    def point1(self, value: PointLike):
        self._point1 = value

    @property
    def point2(self) -> PointLike:
        if self.ret_updated:
            self._recalculate()
            self.ret_updated = False
        return self._point2
    
    @point2.setter
    def point2(self, value: PointLike):
        self._point2 = value

    def __init__(self, line: LineLike, circle: Circles, name: str = ""):
        super().__init__(name if name is not "" else f"IntersectionPointLCir@{id(self)}")
        self.line = line
        self.circle = circle
        self._point1 = ConstraintPoint(np.zeros(2), "IntersectionPointLCir_P1@{id(self)}")
        self._point2 = ConstraintPoint(np.zeros(2), "IntersectionPointLCir_P2@{id(self)}")

        self.line.add_dependent(self)
        self.circle.add_dependent(self)

        # 反向注册
        self.add_dependent(self._point1)
        self.add_dependent(self._point2)

    def _recalculate(self):
        # 对于 PPP
        from manimgeo.components.conic_section import CirclePPP

        center_coord = self.circle.center_point.coord if not isinstance(self.circle, CirclePPP) else self.circle.center
        radius = np.linalg.norm(self.circle.center_point.coord - self.circle.point.coord) if not isinstance(self.circle, CirclePPP) else self.circle.radius

        intersections = GeoUtils.line_circle_intersection(self.line.start.coord, self.line.end.coord, center_coord, radius)

        if len(intersections) == 2:
            self._point1.coord = intersections[0]
            self._point2.coord = intersections[1]
        elif len(intersections) == 1:
            self._point1.coord = intersections[0]
            self._point2.coord = intersections[0]
        else:
            raise ValueError(f"For {self.line.name} and {self.circle.name}, No intersection found")

class IntersectionPointCirCir(BaseGeometry):
    """
    ## 构造两圆交点

    通过 `point1` `point2` 访问两个约束得到的交点
    """
    from manimgeo.components.conic_section import CircleP, CirclePP, CirclePPP
    Circles: TypeAlias = Union[CircleP, CirclePP, CirclePPP]

    circle1: Circles
    circle2: Circles
    point1: PointLike
    point2: PointLike

    def __init__(self, circle1: CircleP, circle2: CircleP, name: str = ""):
        super().__init__(name if name is not "" else f"IntersectionPointCirCir@{id(self)}")
        self.circle1 = circle1
        self.circle2 = circle2
        self.point1 = ConstraintPoint(np.zeros(2), "IntersectionPointCirCir_P1@{id(self)}")
        self.point2 = ConstraintPoint(np.zeros(2), "IntersectionPointCirCir_P2@{id(self)}")

        self.circle1.add_dependent(self)
        self.circle2.add_dependent(self)

        # 反向注册
        self.add_dependent(self.point1)
        self.add_dependent(self.point2)

    def _recalculate(self):
        # 对于 PPP
        from manimgeo.components.conic_section import CirclePPP

        center_coord1 = self.circle1.center_point.coord if not isinstance(self.circle1, CirclePPP) else self.circle1.center
        radius1 = np.linalg.norm(self.circle1.center_point.coord - self.circle1.point.coord) if not isinstance(self.circle1, CirclePPP) else self.circle1.radius

        center_coord2 = self.circle2.center_point.coord if not isinstance(self.circle2, CirclePPP) else self.circle2.center
        radius2 = np.linalg.norm(self.circle2.center_point.coord - self.circle2.point.coord) if not isinstance(self.circle2, CirclePPP) else self.circle2.radius

        intersections = GeoUtils.circle_circle_intersection(center_coord1, radius1, center_coord2, radius2)

        if len(intersections) == 2:
            self.point1.coord = intersections[0]
            self.point2.coord = intersections[1]
        elif len(intersections) == 1:
            self.point1.coord = intersections[0]
            self.point2.coord = intersections[0]
        else:
            raise ValueError(f"For {self.circle1.name} and {self.circle2.name}, No intersection found")
        