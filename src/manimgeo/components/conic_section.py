from manimgeo.components.base import PointLike, ParametricGeometryLike
from manimgeo.utils.utils import GeoUtils

from typing import overload, Union, Optional, Literal, Tuple
import numpy as np

class CirclePP(ParametricGeometryLike):
    """圆心半径点构造圆"""
    center_point: PointLike
    point: PointLike

    def __init__(self, center: PointLike, point: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"CirclePP@{id(self)}")

        self.center_point = center
        self.point = point

        self.center_point.add_dependent(self)
        self.point.add_dependent(self)

    def _recalculate(self):
        pass

    def parametric(self, t: float) -> np.ndarray:
        """0 <= t <= 2π"""
        center, radius = self.center_point.coord, np.linalg.norm(self.point.coord - self.center_point.coord)
        return center + radius*np.array([np.cos(t), np.sin(t)])
    
class CircleP(ParametricGeometryLike):
    """圆心半径构造圆"""
    center_point: PointLike
    _radius: float

    @property
    def radius(self) -> float:
        """半径"""
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        self.board_update_msg()
        self._radius = value

    def __init__(self, center: PointLike, radius: float, name: str = ""):
        super().__init__(name if name is not "" else f"CircleP@{id(self)}")

        self.center_point = center
        self._radius = radius

        self.center_point.add_dependent(self)

    def _recalculate(self):
        pass

    def parametric(self, t: float) -> np.ndarray:
        """0 <= t <= 2π"""
        return self.center_point.coord + self.radius*np.array([np.cos(t), np.sin(t)])
    
class CirclePPP(ParametricGeometryLike):
    """三点构造外接圆"""
    point1: PointLike
    point2: PointLike
    point3: PointLike

    def __init__(self, point1: PointLike, point2: PointLike, point3: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"CirclePPP@{id(self)}")

        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

        self.point1.add_dependent(self)
        self.point2.add_dependent(self)
        self.point3.add_dependent(self)

    @property
    def radius_and_center(self) -> Tuple[float, float]:
        """半径与圆心"""
        p1, p2, p3 = self.point1.coord, self.point2.coord, self.point3.coord
        a = np.linalg.norm(p2 - p3)
        b = np.linalg.norm(p1 - p3)
        c = np.linalg.norm(p1 - p2)
        s = (a + b + c) / 2
        r = a * b * c / (4 * np.sqrt(s * (s - a) * (s - b) * (s - c)))

        # 计算圆心
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        # 构造垂直平分线的方程组
        A = np.array([
            [2 * (x2 - x1), 2 * (y2 - y1)],
            [2 * (x3 - x2), 2 * (y3 - y2)]
        ])
        B = np.array([
            x2**2 + y2**2 - x1**2 - y1**2,
            x3**2 + y3**2 - x2**2 - y2**2
        ])

        center = np.linalg.solve(A, B)
        return r, center
    
    @property
    def radius(self) -> float:
        return self.radius_and_center[0]
    
    @property
    def center(self) -> np.ndarray:
        return self.radius_and_center[1]

    def _recalculate(self):
        pass

    def parametric(self, t: float) -> np.ndarray:
        """0 <= t <= 2π"""
        radius, center = self.radius_and_center
        return center + radius*np.array([np.cos(t), np.sin(t)])

class EllipseAB(ParametricGeometryLike):
    """轴点构造椭圆"""
    x_point: PointLike
    y_point: PointLike
    center: PointLike

    def __init__(self, center: PointLike, x_point: PointLike, y_point: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"EllipseAB@{id(self)}")

        if np.all(center.coord == x_point.coord) or np.all(center.coord == y_point.coord):
            raise ValueError("Invalid input arguments")
        if x_point.coord[1] != center.coord[1] or y_point.coord[0] != center.coord[0]:
            raise ValueError("Invalid input arguments")

        self.center = center
        self.x_point = x_point
        self.y_point = y_point

        self.center.add_dependent(self)
        self.x_point.add_dependent(self)
        self.y_point.add_dependent(self)

    def _recalculate(self):
        pass

    def parametric(self, t: float) -> np.ndarray:
        """0 <= t <= 2π"""
        center = self.center.coord
        a = np.linalg.norm(self.x_point.coord - center)
        b = np.linalg.norm(self.y_point.coord - center)
        return center + np.array([a*np.cos(t), b*np.sin(t)])

class EllipseCE(ParametricGeometryLike):
    """焦点离心率构造椭圆"""
    center: PointLike
    focal_point: PointLike
    _eccentricity: float

    @property
    def eccentricity(self) -> float:
        """离心率"""
        return self._eccentricity
    
    @eccentricity.setter
    def eccentricity(self, value: float):
        self.board_update_msg()
        self._eccentricity = value

    def __init__(self, center: PointLike, focal_point: PointLike, eccentricity: float, name: str = ""):
        super().__init__(name if name is not "" else f"EllipseCE@{id(self)}")

        if np.all(center.coord == focal_point.coord):
            raise ValueError("Invalid input arguments")
        if focal_point.coord[1] != center.coord[1] and focal_point.coord[0] != center.coord[0]:
            raise ValueError("Invalid input arguments")
        
        self.center = center
        self.focal_point = focal_point
        self._eccentricity = eccentricity

        self.center.add_dependent(self)
        self.focal_point.add_dependent(self)

    def _recalculate(self):
        pass

    def parametric(self, t: float) -> np.ndarray:
        """0 <= t <= 2π"""
        e = self._eccentricity
        c = np.linalg.norm(self.focal_point.coord - self.center.coord)
        a = c / e
        b = np.sqrt(a**2 - c**2)
        return self.center.coord + np.array([a*np.cos(t), b*np.sin(t)])

class HyperbolaAB(ParametricGeometryLike):
    """轴点构造双曲线"""
    x_point: PointLike
    y_point: PointLike
    center: PointLike

    def __init__(self, center: PointLike, x_point: PointLike, y_point: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"HyperbolaAB@{id(self)}")

        if np.all(center.coord == x_point.coord) or np.all(center.coord == y_point.coord):
            raise ValueError("Invalid input arguments")
        if x_point.coord[1] != center.coord[1] or y_point.coord[0] != center.coord[0]:
            raise ValueError("Invalid input arguments")

        self.center = center
        self.x_point = x_point
        self.y_point = y_point

        self.center.add_dependent(self)
        self.x_point.add_dependent(self)
        self.y_point.add_dependent(self)

    def _recalculate(self):
        pass

    def parametric(self, t: float) -> np.ndarray:
        """0 <= t <= 2π"""
        center = self.center.coord
        a = np.linalg.norm(self.x_point.coord - center)
        b = np.linalg.norm(self.y_point.coord - center)
        return center + np.array([a*np.cosh(t), b*np.sinh(t)])
    
class HyperbolaCE(ParametricGeometryLike):
    """焦点离心率构造双曲线"""
    center: PointLike
    focal_point: PointLike
    _eccentricity: float

    @property
    def eccentricity(self) -> float:
        """离心率"""
        return self._eccentricity
    
    @eccentricity.setter
    def eccentricity(self, value: float):
        self.board_update_msg()
        self._eccentricity = value

    def __init__(self, center: PointLike, focal_point: PointLike, eccentricity: float, name: str = ""):
        super().__init__(name if name is not "" else f"HyperbolaCE@{id(self)}")

        if np.all(center.coord == focal_point.coord):
            raise ValueError("Invalid input arguments")
        if focal_point.coord[1] != center.coord[1] and focal_point.coord[0] != center.coord[0]:
            raise ValueError("Invalid input arguments")
        
        self.center = center
        self.focal_point = focal_point
        self._eccentricity = eccentricity

        self.center.add_dependent(self)
        self.focal_point.add_dependent(self)

    def _recalculate(self):
        pass

    def parametric(self, t: float) -> np.ndarray:
        """0 <= t <= 2π"""
        e = self._eccentricity
        c = np.linalg.norm(self.focal_point.coord - self.center.coord)
        a = c / e
        b = np.sqrt(c**2 - a**2)
        return self.center.coord + np.array([a*np.cosh(t), b*np.sinh(t)])

class ParabolaPP(ParametricGeometryLike):
    """中心与交点构造抛物线"""
    center: PointLike
    focal: PointLike

    def __init__(self, center: PointLike, focal: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"Parabola@{id(self)}")
        
        if np.all(center.coord == focal.coord):
            raise ValueError("Invalid input arguments")
        if focal.coord[1] != center.coord[1] and focal.coord[0] != center.coord[0]:
            raise ValueError("Invalid input arguments")
        
        self.center = center
        self.focal = focal

        self.center.add_dependent(self)
        self.focal.add_dependent(self)

    def _recalculate(self):
        pass

    def parametric(self, t: float) -> np.ndarray:
        center = self.center.coord
        focal = self.focal.coord
        return center + np.array([focal[0]*t**2, focal[1]*t])