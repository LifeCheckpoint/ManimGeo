from __future__ import annotations

import numpy as np
from typing import TYPE_CHECKING, Union, Literal
from numbers import Number

from manimgeo.components.base import GeometryAdapter, BaseGeometry
from manimgeo.utils.utils import GeoUtils
from manimgeo.utils.mathe import GeoMathe

if TYPE_CHECKING:
    from manimgeo.components.point import Point
    from manimgeo.components.line import LineSegment

class CircleAdapter(GeometryAdapter):
    center: np.ndarray
    radius: Number
    area: Number
    circumference: Number

    def __init__(
            self, 
            construct_type: Literal["PR", "PP", "L", "PPP"], 
            current_geo_obj: "Circle", 
            *objs: Union[BaseGeometry, any]
        ):
        """
        PR: 中心与半径
        PP: 中心与圆上一点
        L: 半径线段
        PPP: 圆上三点
        """
        super().__init__(construct_type)

        # 添加依赖
        [obj.add_dependent(current_geo_obj) for obj in objs if isinstance(obj, BaseGeometry)]
        
    def __call__(self, *objs: Union[BaseGeometry, any]):
        from manimgeo.components.point import Point
        from manimgeo.components.line import LineSegment

        match self.construct_type:
            case "PR":
                GeoUtils.check_params(objs, Point, Number)
                self.center = objs[0].coord
                self.radius = objs[1]

            case "PP":
                GeoUtils.check_params(objs, Point, Point)
                self.center = objs[0].coord
                self.radius = np.linalg.norm(objs[1].coord - objs[0].coord)

            case "L":
                GeoUtils.check_params(objs, LineSegment)
                self.center = objs[0].start.coord
                self.radius = np.linalg.norm(objs[0].end.coord - objs[0].start.coord)

            case "PPP":
                GeoUtils.check_params(objs, Point, Point, Point)
                self.radius, self.center = GeoMathe.three_points_circle_r_c(
                    objs[0].coord, objs[1].coord, objs[2].coord
                )

            case _:
                raise ValueError(f"Invalid constructing method: {self.construct_type}")

        self.area = np.pi * self.radius ** 2
        self.circumference = 2 * np.pi * self.radius

class Circle(BaseGeometry):
    attrs = ["center", "radius", "area", "circumference"]
    center: np.ndarray
    radius: Number
    area: Number
    circumference: Number

    def __init__(
            self, 
            construct_type: Literal["PR", "PP", "L", "PPP"], 
            *objs, 
            name: str = ""
        ):
        """通过指定构造方式与对象构造圆"""
        super().__init__(GeoUtils.get_name(name, self, construct_type))
        self.objs = objs
        self.adapter = CircleAdapter(construct_type, self, *objs)
        self.update()

# Constructing Methods

def CirclePR(center: Point, radius: Number, name: str = ""):
    """
    ## 中心与半径构造圆

    `center`: 中心点
    `radius`: 数值半径
    """
    return Circle("PR", center, radius, name=name)

def CirclePP(center: Point, point: Point, name: str = ""):
    """
    ## 中心与圆上一点构造圆

    `center`: 圆心
    `point`: 圆上一点
    """
    return Circle("PP", center, point, name=name)

def CircleL(radius_segment: LineSegment, name: str = ""):
    """
    ## 半径线段构造圆

    `radius_segment`: 半径线段
    """
    return Circle("L", radius_segment, name=name)

def CirclePPP(point1: Point, point2: Point, point3: Point, name: str = ""):
    """
    ## 圆上三点构造圆

    `point1`: 圆上一点
    `point2`: 圆上一点
    `point3`: 圆上一点
    """
    return Circle("PPP", point1, point2, point3, name=name)