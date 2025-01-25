from manimgeo.components.base import PointLike, ParametricGeometry
from manimgeo.utils.utils import GeoUtils

from typing import overload, Union, Optional
import numpy as np

class Circle(ParametricGeometry):
    """圆类型"""
    data: tuple[np.ndarray, Union[float, np.ndarray]]

    @overload
    def __init__(self, center: PointLike, radius: float, name: str = ""):
        ...

    @overload
    def __init__(self, center: PointLike, point: PointLike, name: str = ""):
        ...

    def __init__(self, center: PointLike, radius_or_point: Union[int, float, PointLike], name: str = ""):
        super().__init__(name)
        self._center = center

        # 依赖于圆心与半径
        if isinstance(radius_or_point, (int, float)):
            self._radius = radius_or_point

        # 依赖于圆心与半径点
        elif isinstance(radius_or_point, PointLike):
            self._radius_point = radius_or_point
            self._radius_point.add_dependent(self)

        else:
            raise ValueError("Invalid input arguments")

        # 圆依赖圆心
        self._center.add_dependent(self)

    def _recalculate(self):
        if hasattr(self, "_radius"):
            # 圆心与半径确定圆
            self.data = (self._center.coord, self._radius)
        else:
            # 圆心与半径点确定圆
            self.data = (self._center.coord, self._radius_point.coord)

    def parametric(self, t: float) -> np.ndarray:
        """参数方程, 0 <= t <= 2π"""
        if hasattr(self, "_radius"):
            center, radius = self.data
        else:
            center, radius = self.data[0], np.linalg.norm(self.data[1] - self.data[0])
        return center + radius*np.array([np.cos(t), np.sin(t)])
    
class Ellipse(ParametricGeometry):
    """椭圆类型"""
    data: tuple[np.ndarray, np.ndarray, np.ndarray] # center, a, b

    @overload
    def __init__(self, center: PointLike, x_axis: Union[int, float], y_axis: Union[int, float], name: str = ""):
        """
        x_axis: a
        y_axis: b
        """
        ...

    @overload
    def __init__(self, center: PointLike, x_axis_point: PointLike, y_axis_point: PointLike, name: str = ""):
        """points 必须与 center 处于同一水平或垂直线上"""
        ...

    @overload
    def __init__(self, center: PointLike, focal_point: PointLike, eccentricity: Union[int, float], name: str = ""):
        """
        焦点确定椭圆，focal_point 必须与 center 处于同一水平或垂直线上
        focal_point: 焦点
        eccentricity: 离心率 e
        """
        ...

    def __init__(
        self,
        center: PointLike,
        x_axis_or_focal_point: Union[int, float, PointLike],
        y_axis_or_eccentricity_point: Union[int, float, PointLike],
        name: Optional[str] = ""
    ):
        super().__init__(name)
        self._center = center

        # 依赖于中心与 x y 轴
        if isinstance(x_axis_or_focal_point, (int, float)) and isinstance(x_axis_or_focal_point, (int, float)):
            if x_axis_or_focal_point <= 0 or y_axis_or_eccentricity_point <= 0:
                raise ValueError("Invalid input arguments")
            self._x_axis = x_axis_or_focal_point
            self._y_axis = y_axis_or_eccentricity_point

        # 依赖于中心与 x y 轴点
        elif isinstance(x_axis_or_focal_point, PointLike) and isinstance(y_axis_or_eccentricity_point, PointLike):
            if np.all(center.coord == x_axis_or_focal_point.coord) or np.all(center.coord == y_axis_or_eccentricity_point.coord):
                raise ValueError("Invalid input arguments")
            if x_axis_or_focal_point.coord[1] != center.coord[1] or y_axis_or_eccentricity_point.coord[0] != center.coord[0]:
                raise ValueError("Invalid input arguments")
            
            self._x_axis_point = x_axis_or_focal_point
            self._y_axis_point = y_axis_or_eccentricity_point
            self._x_axis_point.add_dependent(self)
            self._y_axis_point.add_dependent(self)

        # 依赖于中心与焦点
        elif isinstance(x_axis_or_focal_point, PointLike) and isinstance(y_axis_or_eccentricity_point, (int, float)):
            if np.all(center.coord == x_axis_or_focal_point.coord):
                raise ValueError("Invalid input arguments")
            if x_axis_or_focal_point.coord[1] != center.coord[1] and x_axis_or_focal_point.coord[0] != center.coord[0]:
                raise ValueError("Invalid input arguments")
            
            self._focal_point = x_axis_or_focal_point
            self._focal_point.add_dependent(self)
            self._eccentricity = y_axis_or_eccentricity_point

        else:
            raise ValueError("Invalid input arguments")
        
        self._center.add_dependent(self)

    def _recalculate(self):
        if hasattr(self, "_x_axis"):
            # 中心与轴确定椭圆
            self.data = (self._center.coord, self._x_axis, self._y_axis)
        elif hasattr("_x_axis_point"):
            # 中心与轴点确定椭圆
            self.data = (self._center.coord, abs(self._x_axis_point.coord[0] - self._center.coord[0]), abs(self._y_axis_point.coord[1] - self._center.coord[1]))
        elif hasattr("_focal_point"):
            # 中心与焦点确定椭圆
            e = self._eccentricity
            c = np.linalg.norm(self._focal_point.coord - self._center.coord)
            a = c / e
            b = np.sqrt(a**2 - c**2)
            self.data = (self._center.coord, a, b)

    def parametric(self, t: float) -> np.ndarray:
        """参数方程, 0 <= t <= 2π"""
        center, a, b = self._center, self._x_axis, self._y_axis
        return center + a*np.array([np.cos(t), np.sin(t)]) + b*np.array([-np.sin(t), np.cos(t)])
    
class Hyperbola(ParametricGeometry):
    """双曲线类型"""
    data: tuple[np.ndarray, np.ndarray, np.ndarray] # center, a, b

    @overload
    def __init__(self, center: PointLike, x_axis: Union[int, float], y_axis: Union[int, float], name: str = ""):
        """
        x_axis: a
        y_axis: b
        """
        ...

    @overload
    def __init__(self, center: PointLike, x_axis_point: PointLike, y_axis_point: PointLike, name: str = ""):
        """points 必须与 center 处于同一水平或垂直线上"""
        ...

    @overload
    def __init__(self, center: PointLike, focal_point: PointLike, eccentricity: Union[int, float], name: str = ""):
        """
        焦点确定双曲线，focal_point 必须与 center 处于同一水平或垂直线上
        focal_point: 焦点
        eccentricity: 离心率 e
        """
        ...

    def __init__(
        self,
        center: PointLike,
        x_axis_or_focal_point: Union[int, float, PointLike],
        y_axis_or_eccentricity_point: Union[int, float, PointLike],
        name: Optional[str] = ""
    ):
        super().__init__(name)
        self._center = center

        # 依赖于中心与 x y 轴
        if isinstance(x_axis_or_focal_point, (int, float)) and isinstance(x_axis_or_focal_point, (int, float)):
            if x_axis_or_focal_point <= 0 or y_axis_or_eccentricity_point <= 0:
                raise ValueError("Invalid input arguments")
            self._x_axis = x_axis_or_focal_point
            self._y_axis = y_axis_or_eccentricity_point

        # 依赖于中心与 x y 轴点
        elif isinstance(x_axis_or_focal_point, PointLike) and isinstance(y_axis_or_eccentricity_point, PointLike):
            if np.all(center.coord == x_axis_or_focal_point.coord) or np.all(center.coord == y_axis_or_eccentricity_point.coord):
                raise ValueError("Invalid input arguments")
            if x_axis_or_focal_point.coord[1] != center.coord[1] or y_axis_or_eccentricity_point.coord[0] != center.coord[0]:
                raise ValueError("Invalid input arguments")
            
            self._x_axis_point = x_axis_or_focal_point
            self._y_axis_point = y_axis_or_eccentricity_point
            self._x_axis_point.add_dependent(self)
            self._y_axis_point.add_dependent(self)

        # 依赖于中心与焦点
        elif isinstance(x_axis_or_focal_point, PointLike) and isinstance(y_axis_or_eccentricity_point, (int, float)):
            if np.all(center.coord == x_axis_or_focal_point.coord):
                raise ValueError("Invalid input arguments")
            if x_axis_or_focal_point.coord[1] != center.coord[1] and x_axis_or_focal_point.coord[0] != center.coord[0]:
                raise ValueError("Invalid input arguments")
            
            self._focal_point = x_axis_or_focal_point
            self._focal_point.add_dependent(self)
            self._eccentricity = y_axis_or_eccentricity_point

        else:
            raise ValueError("Invalid input arguments")
        
        self._center.add_dependent(self)
        
    def _recalculate(self):
        if hasattr(self, "_x_axis"):
            # 中心与轴确定双曲线
            self.data = (self._center.coord, self._x_axis, self._y_axis)
        elif hasattr("_x_axis_point"):
            # 中心与轴点确定双曲线
            self.data = (self._center.coord, abs(self._x_axis_point.coord[0] - self._center.coord[0]), abs(self._y_axis_point.coord[1] - self._center.coord[1]))
        elif hasattr("_focal_point"):
            # 中心与焦点确定双曲线
            e = self._eccentricity
            c = np.linalg.norm(self._focal_point.coord - self._center.coord)
            a = c / e
            b = np.sqrt(a**2 + c**2)
            self.data = (self._center.coord, a, b)

    def parametric(self, t: float) -> np.ndarray:
        """参数方程, 0 <= t <= 2π"""
        center, a, b = self._center, self._x_axis, self._y_axis
        return center + a*np.array([np.cosh(t), np.sinh(t)]) + b*np.array([-np.sinh(t), np.cosh(t)])
    
class Parabola(ParametricGeometry):
    """抛物线类型"""
    data: tuple[np.ndarray, np.ndarray] # center, p

    @overload
    def __init__(self, center: PointLike, focal_length: float, name: str = ""):
        """
        focal_length: 焦距 p
        """
        ...

    @overload
    def __init__(self, center: PointLike, focal_point: PointLike, name: str = ""):
        """焦点确定抛物线"""
        ...

    def __init__(self, center: PointLike, focal_or_focal_point: Union[int, float, PointLike], name: str = ""):
        super().__init__(name)
        self._center = center

        # 依赖于中心与焦距
        if isinstance(focal_or_focal_point, (int, float)):
            if focal_or_focal_point <= 0:
                raise ValueError("Invalid input arguments")
            self._focal_length = focal_or_focal_point

        # 依赖于中心与焦点
        elif isinstance(focal_or_focal_point, PointLike):
            if np.all(center.coord == focal_or_focal_point.coord):
                raise ValueError("Invalid input arguments")
            self._focal_point = focal_or_focal_point
            self._focal_point.add_dependent(self)

        else:
            raise ValueError("Invalid input arguments")
        
        self._center.add_dependent(self)
        
    def _recalculate(self):
        if hasattr(self, "_focal_length"):
            # 中心与焦距确定抛物线
            self.data = (self._center.coord, self._focal_length)
        elif hasattr("_focal_point"):
            # 中心与焦点确定抛物线
            p = np.linalg.norm(self._focal_point.coord - self._center.coord) / 2
            self.data = (self._center.coord, p)

    def parametric(self, t: float) -> np.ndarray:
        """参数方程, 0 <= t <= 2π"""
        center, p = self.data
        return center + np.array([t, t**2])/(4*p)