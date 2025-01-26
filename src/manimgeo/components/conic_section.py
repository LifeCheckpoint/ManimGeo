from manimgeo.components.base import PointLike, ParametricGeometryLike
from manimgeo.utils.utils import GeoUtils

from typing import overload, Union, Optional, Literal, Tuple
import numpy as np

class CirclePP(ParametricGeometryLike):
    """圆心+半径点构造圆"""
    center: PointLike
    point: PointLike

    def __init__(self, center: PointLike, point: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"CirclePP@{id(self)}")

        self.center = center
        self.point = point

        self.center.add_dependent(self)
        self.point.add_dependent(self)

    def _recalculate(self):
        pass

    def parametric(self, t: float) -> np.ndarray:
        """0 <= t <= 2π"""
        center, radius = self.center.coord, np.linalg.norm(self.point.coord - self.center.coord)
        return center + radius*np.array([np.cos(t), np.sin(t)])
    
class CircleP(ParametricGeometryLike):
    """圆心+半径构造圆"""
    center: PointLike
    _radius: float

    @property
    def radius(self) -> float:
        """半径"""
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        self.update()
        self._radius = value

    def __init__(self, center: PointLike, radius: float, name: str = ""):
        super().__init__(name if name is not "" else f"CircleP@{id(self)}")

        self.center = center
        self._radius = radius

        self.center.add_dependent(self)

    def _recalculate(self):
        pass

    def parametric(self, t: float) -> np.ndarray:
        """0 <= t <= 2π"""
        return self.center.coord + self.radius*np.array([np.cos(t), np.sin(t)])
    
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

# class EllipseAB(ParametricGeometryLike):
#     """长短轴椭圆类型"""
#     data: tuple[np.ndarray, np.ndarray, np.ndarray] # center, a, b

#     @overload
#     def __init__(self, center: PointLike, x_axis: Union[int, float], y_axis: Union[int, float], name: str = ""):
#         """
#         x_axis: a
#         y_axis: b
#         """
#         ...

#     @overload
#     def __init__(self, center: PointLike, x_axis_point: PointLike, y_axis_point: PointLike, name: str = ""):
#         """points 必须与 center 处于同一水平或垂直线上"""
#         ...

#     def __init__(
#         self,
#         center: PointLike,
#         x_axis_or_point: Union[int, float, PointLike],
#         y_axis_or_point: Union[int, float, PointLike],
#         name: Optional[str] = ""
#     ):
#         super().__init__(name)
#         self._center = center

#         # 依赖于中心与 x y 轴
#         if isinstance(x_axis_or_point, (int, float)) and isinstance(x_axis_or_point, (int, float)):
#             if x_axis_or_point <= 0 or y_axis_or_point <= 0:
#                 raise ValueError("Invalid input arguments")
#             self._x_axis = x_axis_or_point
#             self._y_axis = y_axis_or_point

#         # 依赖于中心与 x y 轴点
#         elif isinstance(x_axis_or_point, PointLike) and isinstance(y_axis_or_point, PointLike):
#             if np.all(center.coord == x_axis_or_point.coord) or np.all(center.coord == y_axis_or_point.coord):
#                 raise ValueError("Invalid input arguments")
#             if x_axis_or_point.coord[1] != center.coord[1] or y_axis_or_point.coord[0] != center.coord[0]:
#                 raise ValueError("Invalid input arguments")
            
#             self._x_axis_point = x_axis_or_point
#             self._y_axis_point = y_axis_or_point
#             self._x_axis_point.add_dependent(self)
#             self._y_axis_point.add_dependent(self)

#         else:
#             raise ValueError("Invalid input arguments")
        
#         self._center.add_dependent(self)

#     def _recalculate(self):
#         if hasattr(self, "_x_axis"):
#             # 中心与轴确定椭圆
#             self.data = (self._center.coord, self._x_axis, self._y_axis)
#         elif hasattr("_x_axis_point"):
#             # 中心与轴点确定椭圆
#             self.data = (self._center.coord, abs(self._x_axis_point.coord[0] - self._center.coord[0]), abs(self._y_axis_point.coord[1] - self._center.coord[1]))

#     def parametric(self, t: float) -> np.ndarray:
#         """参数方程, 0 <= t <= 2π"""
#         center, a, b = self._center, self._x_axis, self._y_axis
#         return center + np.array([a*np.cos(t), b*np.sin(t)])
    
# class EllipseCE(ParametricGeometryLike):
#     @overload
#     def __init__(self, center: PointLike, focal_point: PointLike, eccentricity: Union[int, float], name: str = ""):
#         """
#         焦点离心率确定椭圆，focal_point 必须与 center 处于同一水平或垂直线上
#         focal_point: 焦点
#         eccentricity: 离心率 e
#         """
#         ...

#     @overload
#     def __init__(self, center: PointLike, focal_distance: Union[int, float], eccentricity: Union[int, float], axis: Literal["x", "y"], name: str = ""):
#         """
#         焦距离心率确定椭圆
#         axis: 焦点位置
#         focal_distance: 焦距
#         eccentricity: 离心率 e
#         """
#         ...

#     def __init__(
#         self,
#         center: PointLike,
#         focal_or_focal_distance: Union[PointLike, int, float],
#         eccentricity: Union[int, float],
#         axis_or_name: Optional[Literal["x", "y"]] = None,
#         name: Optional[str] = ""
#     ):
#         self._center = center

#         # 依赖于中心与焦点
#         if isinstance(focal_or_focal_distance, PointLike) and isinstance(axis_or_name, (int, float)):
#             super().__init__(axis_or_name)

#             if np.all(center.coord == focal_or_focal_distance.coord):
#                 raise ValueError("Invalid input arguments")
#             if focal_or_focal_distance.coord[1] != center.coord[1] and focal_or_focal_distance.coord[0] != center.coord[0]:
#                 raise ValueError("Invalid input arguments")
            
#             self._focal_point = focal_or_focal_distance
#             self._focal_point.add_dependent(self)
#             self._eccentricity = eccentricity

#         # 依赖于中心与焦距
#         elif isinstance(focal_or_focal_distance, (int, float)) and isinstance(axis_or_name, (int, float)):
#             super().__init__(name)

#             self._focal_distance = focal_or_focal_distance
#             self._eccentricity = eccentricity
#             self._axis = axis_or_name

#         else:
#             raise ValueError("Invalid input arguments")
        
#         self._center.add_dependent(self)

#     def _recalculate(self):
#         if hasattr(self, "_focal_point"):
#             # 中心与焦点确定椭圆
#             e = self._eccentricity
#             c = np.linalg.norm(self._focal_point.coord - self._center.coord)
#             a = c / e
#             b = np.sqrt(a**2 - c**2)
#             self.data = (self._center.coord, a, b)
#         elif hasattr("_focal_distance"):
#             # 中心与焦距确定椭圆，axis 为 x 或 y
#             e = self._eccentricity
#             c = self._focal_distance / 2
#             a = c / e
#             b = np.sqrt(a**2 - c**2)
#             if self._axis == "x":
#                 self.data = (self._center.coord, a, b)
#             elif self._axis == "y":
#                 self.data = (self._center.coord, b, a)
#             else:
#                 raise ValueError("Invalid input arguments")
            
#     def parametric(self, t: float) -> np.ndarray:
#         """参数方程, 0 <= t <= 2π"""
#         center, a, b = self.data
#         return center + np.array([a*np.cos(t), b*np.sin(t)])

# class HyperbolaAB(ParametricGeometryLike):
#     """双曲线类型"""
#     data: tuple[np.ndarray, np.ndarray, np.ndarray] # center, a, b

#     @overload
#     def __init__(self, center: PointLike, x_axis: Union[int, float], y_axis: Union[int, float], name: str = ""):
#         """
#         x_axis: a
#         y_axis: b
#         """
#         ...

#     @overload
#     def __init__(self, center: PointLike, x_axis_point: PointLike, y_axis_point: PointLike, name: str = ""):
#         """points 必须与 center 处于同一水平或垂直线上"""
#         ...

#     def __init__(
#         self,
#         center: PointLike,
#         x_axis_or_point: Union[int, float, PointLike],
#         y_axis_or_point: Union[int, float, PointLike],
#         name: Optional[str] = ""
#     ):
#         super().__init__(name)
#         self._center = center

#         # 依赖于中心与 x y 轴
#         if isinstance(x_axis_or_point, (int, float)) and isinstance(x_axis_or_point, (int, float)):
#             if x_axis_or_point <= 0 or y_axis_or_point <= 0:
#                 raise ValueError("Invalid input arguments")
#             self._x_axis = x_axis_or_point
#             self._y_axis = y_axis_or_point

#         # 依赖于中心与 x y 轴点
#         elif isinstance(x_axis_or_point, PointLike) and isinstance(y_axis_or_point, PointLike):
#             if np.all(center.coord == x_axis_or_point.coord) or np.all(center.coord == y_axis_or_point.coord):
#                 raise ValueError("Invalid input arguments")
#             if x_axis_or_point.coord[1] != center.coord[1] or y_axis_or_point.coord[0] != center.coord[0]:
#                 raise ValueError("Invalid input arguments")
            
#             self._x_axis_point = x_axis_or_point
#             self._y_axis_point = y_axis_or_point
#             self._x_axis_point.add_dependent(self)
#             self._y_axis_point.add_dependent(self)

#         else:
#             raise ValueError("Invalid input arguments")
        
#         self._center.add_dependent(self)
        
#     def _recalculate(self):
#         if hasattr(self, "_x_axis"):
#             # 中心与轴确定双曲线
#             self.data = (self._center.coord, self._x_axis, self._y_axis)
#         elif hasattr("_x_axis_point"):
#             # 中心与轴点确定双曲线
#             self.data = (self._center.coord, abs(self._x_axis_point.coord[0] - self._center.coord[0]), abs(self._y_axis_point.coord[1] - self._center.coord[1]))

#     def parametric(self, t: float) -> np.ndarray:
#         """参数方程, 0 <= t <= 2π"""
#         center, a, b = self._center, self._x_axis, self._y_axis
#         return center + np.array([a*np.cosh(t), b*np.sinh(t)])
    
# class HyperbolaCE(ParametricGeometryLike):
#     @overload
#     def __init__(self, center: PointLike, focal_point: PointLike, eccentricity: Union[int, float], name: str = ""):
#         """
#         焦点离心率确定双曲线，focal_point 必须与 center 处于同一水平或垂直线上
#         focal_point: 焦点
#         eccentricity: 离心率 e
#         """
#         ...

#     @overload
#     def __init__(self, center: PointLike, focal_distance: Union[int, float], eccentricity: Union[int, float], axis: Literal["x", "y"], name: str = ""):
#         """
#         焦距离心率确定双曲线
#         axis: 焦点位置
#         focal_distance: 焦距
#         eccentricity: 离心率 e
#         """
#         ...

#     def __init__(
#         self,
#         center: PointLike,
#         focal_or_focal_distance: Union[PointLike, int, float],
#         eccentricity: Union[int, float],
#         axis_or_name: Optional[Literal["x", "y"]] = None,
#         name: Optional[str] = ""
#     ):
#         self._center = center

#         # 依赖于中心与焦点
#         if isinstance(focal_or_focal_distance, PointLike) and isinstance(axis_or_name, (int, float)):
#             super().__init__(axis_or_name)

#             if np.all(center.coord == focal_or_focal_distance.coord):
#                 raise ValueError("Invalid input arguments")
#             if focal_or_focal_distance.coord[1] != center.coord[1] and focal_or_focal_distance.coord[0] != center.coord[0]:
#                 raise ValueError("Invalid input arguments")
            
#             self._focal_point = focal_or_focal_distance
#             self._focal_point.add_dependent(self)
#             self._eccentricity = eccentricity

#         # 依赖于中心与焦距
#         elif isinstance(focal_or_focal_distance, (int, float)) and isinstance(axis_or_name, (int, float)):
#             super().__init__(name)

#             self._focal_distance = focal_or_focal_distance
#             self._eccentricity = eccentricity
#             self._axis = axis_or_name

#         else:
#             raise ValueError("Invalid input arguments")
        
#         self._center.add_dependent(self)

#     def _recalculate(self):
#         if hasattr(self, "_focal_point"):
#             # 中心与焦点确定双曲线
#             e = self._eccentricity
#             c = np.linalg.norm(self._focal_point.coord - self._center.coord)
#             a = c / e
#             b = np.sqrt(a**2 + c**2)
#             self.data = (self._center.coord, a, b)
#         elif hasattr("_focal_distance"):
#             # 中心与焦距确定双曲线，axis 为 x 或 y
#             e = self._eccentricity
#             c = self._focal_distance / 2
#             a = c / e
#             b = np.sqrt(a**2 + c**2)
#             if self._axis == "x":
#                 self.data = (self._center.coord, a, b)
#             elif self._axis == "y":
#                 self.data = (self._center.coord, b, a)
#             else:
#                 raise ValueError("Invalid input arguments")
            
#     def parametric(self, t: float) -> np.ndarray:
#         """参数方程, 0 <= t <= 2π"""
#         center, a, b = self.data
#         return center + np.array([a*np.cosh(t), b*np.sinh(t)])

# class Parabola(ParametricGeometryLike):
#     """抛物线类型"""
#     data: tuple[np.ndarray, np.ndarray] # center, p

#     @overload
#     def __init__(self, center: PointLike, focal_length: float, name: str = ""):
#         """
#         focal_length: 焦距 p
#         """
#         ...

#     @overload
#     def __init__(self, center: PointLike, focal_point: PointLike, name: str = ""):
#         """焦点确定抛物线"""
#         ...

#     def __init__(self, center: PointLike, focal_or_focal_point: Union[int, float, PointLike], name: str = ""):
#         super().__init__(name)
#         self._center = center

#         # 依赖于中心与焦距
#         if isinstance(focal_or_focal_point, (int, float)):
#             if focal_or_focal_point <= 0:
#                 raise ValueError("Invalid input arguments")
#             self._focal_length = focal_or_focal_point

#         # 依赖于中心与焦点
#         elif isinstance(focal_or_focal_point, PointLike):
#             if np.all(center.coord == focal_or_focal_point.coord):
#                 raise ValueError("Invalid input arguments")
#             self._focal_point = focal_or_focal_point
#             self._focal_point.add_dependent(self)

#         else:
#             raise ValueError("Invalid input arguments")
        
#         self._center.add_dependent(self)
        
#     def _recalculate(self):
#         if hasattr(self, "_focal_length"):
#             # 中心与焦距确定抛物线
#             self.data = (self._center.coord, self._focal_length)
#         elif hasattr("_focal_point"):
#             # 中心与焦点确定抛物线
#             p = np.linalg.norm(self._focal_point.coord - self._center.coord) / 2
#             self.data = (self._center.coord, p)

#     def parametric(self, t: float) -> np.ndarray:
#         """参数方程, 0 <= t <= 2π"""
#         center, p = self.data
#         return center + np.array([p*t**2, 2*p*t])
