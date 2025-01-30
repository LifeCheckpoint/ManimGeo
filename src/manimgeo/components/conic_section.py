from manimgeo.components.base import PointLike, ParametricGeometryLike
from manimgeo.utils.utils import GeoUtils

from typing import overload, Union, Optional, Literal, Tuple
import numpy as np

# class EllipseAB(ParametricGeometryLike):
#     """轴点构造椭圆"""
#     x_point: PointLike
#     y_point: PointLike
#     center: PointLike

#     def __init__(self, center: PointLike, x_point: PointLike, y_point: PointLike, name: str = ""):
#         super().__init__(name if name is not "" else f"EllipseAB@{id(self)}")

#         if np.all(center.coord == x_point.coord) or np.all(center.coord == y_point.coord):
#             raise ValueError("Invalid input arguments")
#         if x_point.coord[1] != center.coord[1] or y_point.coord[0] != center.coord[0]:
#             raise ValueError("Invalid input arguments")

#         self.center = center
#         self.x_point = x_point
#         self.y_point = y_point

#         self.center.add_dependent(self)
#         self.x_point.add_dependent(self)
#         self.y_point.add_dependent(self)

#     def _recalculate(self):
#         pass

#     def parametric(self, t: float) -> np.ndarray:
#         """0 <= t <= 2π"""
#         center = self.center.coord
#         a = np.linalg.norm(self.x_point.coord - center)
#         b = np.linalg.norm(self.y_point.coord - center)
#         return center + np.array([a*np.cos(t), b*np.sin(t)])

# class EllipseCE(ParametricGeometryLike):
#     """焦点离心率构造椭圆"""
#     center: PointLike
#     focal_point: PointLike
#     _eccentricity: float

#     @property
#     def eccentricity(self) -> float:
#         """离心率"""
#         return self._eccentricity
    
#     @eccentricity.setter
#     def eccentricity(self, value: float):
#         self.board_update_msg()
#         self._eccentricity = value

#     def __init__(self, center: PointLike, focal_point: PointLike, eccentricity: float, name: str = ""):
#         super().__init__(name if name is not "" else f"EllipseCE@{id(self)}")

#         if np.all(center.coord == focal_point.coord):
#             raise ValueError("Invalid input arguments")
#         if focal_point.coord[1] != center.coord[1] and focal_point.coord[0] != center.coord[0]:
#             raise ValueError("Invalid input arguments")
        
#         self.center = center
#         self.focal_point = focal_point
#         self._eccentricity = eccentricity

#         self.center.add_dependent(self)
#         self.focal_point.add_dependent(self)

#     def _recalculate(self):
#         pass

#     def parametric(self, t: float) -> np.ndarray:
#         """0 <= t <= 2π"""
#         e = self._eccentricity
#         c = np.linalg.norm(self.focal_point.coord - self.center.coord)
#         a = c / e
#         b = np.sqrt(a**2 - c**2)
#         return self.center.coord + np.array([a*np.cos(t), b*np.sin(t)])

# class HyperbolaAB(ParametricGeometryLike):
#     """轴点构造双曲线"""
#     x_point: PointLike
#     y_point: PointLike
#     center: PointLike

#     def __init__(self, center: PointLike, x_point: PointLike, y_point: PointLike, name: str = ""):
#         super().__init__(name if name is not "" else f"HyperbolaAB@{id(self)}")

#         if np.all(center.coord == x_point.coord) or np.all(center.coord == y_point.coord):
#             raise ValueError("Invalid input arguments")
#         if x_point.coord[1] != center.coord[1] or y_point.coord[0] != center.coord[0]:
#             raise ValueError("Invalid input arguments")

#         self.center = center
#         self.x_point = x_point
#         self.y_point = y_point

#         self.center.add_dependent(self)
#         self.x_point.add_dependent(self)
#         self.y_point.add_dependent(self)

#     def _recalculate(self):
#         pass

#     def parametric(self, t: float) -> np.ndarray:
#         """0 <= t <= 2π"""
#         center = self.center.coord
#         a = np.linalg.norm(self.x_point.coord - center)
#         b = np.linalg.norm(self.y_point.coord - center)
#         return center + np.array([a*np.cosh(t), b*np.sinh(t)])
    
# class HyperbolaCE(ParametricGeometryLike):
#     """焦点离心率构造双曲线"""
#     center: PointLike
#     focal_point: PointLike
#     _eccentricity: float

#     @property
#     def eccentricity(self) -> float:
#         """离心率"""
#         return self._eccentricity
    
#     @eccentricity.setter
#     def eccentricity(self, value: float):
#         self.board_update_msg()
#         self._eccentricity = value

#     def __init__(self, center: PointLike, focal_point: PointLike, eccentricity: float, name: str = ""):
#         super().__init__(name if name is not "" else f"HyperbolaCE@{id(self)}")

#         if np.all(center.coord == focal_point.coord):
#             raise ValueError("Invalid input arguments")
#         if focal_point.coord[1] != center.coord[1] and focal_point.coord[0] != center.coord[0]:
#             raise ValueError("Invalid input arguments")
        
#         self.center = center
#         self.focal_point = focal_point
#         self._eccentricity = eccentricity

#         self.center.add_dependent(self)
#         self.focal_point.add_dependent(self)

#     def _recalculate(self):
#         pass

#     def parametric(self, t: float) -> np.ndarray:
#         """0 <= t <= 2π"""
#         e = self._eccentricity
#         c = np.linalg.norm(self.focal_point.coord - self.center.coord)
#         a = c / e
#         b = np.sqrt(c**2 - a**2)
#         return self.center.coord + np.array([a*np.cosh(t), b*np.sinh(t)])

# class ParabolaPP(ParametricGeometryLike):
#     """中心与交点构造抛物线"""
#     center: PointLike
#     focal: PointLike

#     def __init__(self, center: PointLike, focal: PointLike, name: str = ""):
#         super().__init__(name if name is not "" else f"Parabola@{id(self)}")
        
#         if np.all(center.coord == focal.coord):
#             raise ValueError("Invalid input arguments")
#         if focal.coord[1] != center.coord[1] and focal.coord[0] != center.coord[0]:
#             raise ValueError("Invalid input arguments")
        
#         self.center = center
#         self.focal = focal

#         self.center.add_dependent(self)
#         self.focal.add_dependent(self)

#     def _recalculate(self):
#         pass

#     def parametric(self, t: float) -> np.ndarray:
#         center = self.center.coord
#         focal = self.focal.coord
#         return center + np.array([focal[0]*t**2, focal[1]*t])