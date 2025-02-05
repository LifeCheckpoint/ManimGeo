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
    from manimgeo.components.vector import Vector

CircleConstructType = Literal[
    "PR", "PP", "L", "PPP", "TranslationCirV",
    "InverseCirCir"
]

class CircleAdapter(GeometryAdapter):
    center: np.ndarray
    radius: Number
    area: Number
    circumference: Number

    def __init__(
            self, 
            construct_type: CircleConstructType, 
            current_geo_obj: "Circle", 
            *objs: Union[BaseGeometry, any]
        ):
        """
        PR: 中心与半径构造圆
        PP: 中心与圆上一点构造圆
        L: 半径线段构造圆
        PPP: 圆上三点构造圆
        TranslationCirV: 构造平移圆
        InverseCirCir: 构造反形圆
        InscribePPP: 构造三点内切圆
        """
        super().__init__(construct_type)

        # 添加依赖
        [obj.add_dependent(current_geo_obj) for obj in objs if isinstance(obj, BaseGeometry)]
        
    def __call__(self, *objs: Union[BaseGeometry, any]):
        from manimgeo.components.point import Point
        from manimgeo.components.line import LineSegment
        from manimgeo.components.vector import Vector

        op_type_map = {
            "PR": [Point, Number],
            "PP": [Point, Point],
            "L": [LineSegment],
            "PPP": [Point, Point, Point],
            "TranslationCirV": [Circle, Vector],
            "InverseCirCir": [Circle, Circle],
            "InscribePPP": [Point, Point, Point]
        }
        GeoUtils.check_params_batch(op_type_map, self.construct_type, objs)

        match self.construct_type:
            case "PR":
                self.center = objs[0].coord.copy()
                self.radius = objs[1]

            case "PP":
                self.center = objs[0].coord.copy()
                self.radius = np.linalg.norm(objs[1].coord - objs[0].coord)

            case "L":
                self.center = objs[0].start.copy()
                self.radius = np.linalg.norm(objs[0].end - objs[0].start)

            case "PPP":
                self.radius, self.center = GeoMathe.circumcenter_r_c(
                    objs[0].coord, objs[1].coord, objs[2].coord
                )

            case "TranslationCirV":
                self.center = objs[0].center + objs[1].vec
                self.radius = objs[0].radius

            case "InverseCirCir":
                self.center, self.radius = GeoMathe.inverse_circle(objs[0].center, objs[0].radius, objs[1].center, objs[1].radius)

            case "InscribePPP":
                self.radius, self.center = GeoMathe.inscribed_r_c(objs[0].coord, objs[1].coord, objs[2].coord)

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

    def __init__(self, construct_type: CircleConstructType, *objs, name: str = ""):
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

def CircleTranslationCirV(circle: Circle, vec: Vector, name: str = ""):
    """
    ## 平移构造圆

    `circle`: 原始圆
    `vec`: 平移向量
    """
    return Circle("TranslationCirV", circle, vec, name=name)

def CircleInverseCirCir(circle: Circle, base_circle: Circle, name: str = ""):
    """
    ## 构造反形圆

    `circle`: 将要进行反演的圆
    `base_circle`: 基圆
    """
    return Circle("InverseCirCir", circle, base_circle, name=name)

def CircleInscribePPP(point1: Point, point2: Point, point3: Point, name: str = ""):
    """
    构造三点内切圆

    `point1`: 第一个点
    `point2`: 第二个点
    `point3`: 第三个点
    """
    return Circle("InscribePPP", point1, point2, point3, name=name)