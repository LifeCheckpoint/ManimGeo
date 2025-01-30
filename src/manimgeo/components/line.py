from __future__ import annotations

import numpy as np
from typing import TYPE_CHECKING, Union, Literal
from numbers import Number

from manimgeo.components.base import GeometryAdapter, BaseGeometry
from manimgeo.utils.utils import GeoUtils
from manimgeo.utils.mathe import GeoMathe

if TYPE_CHECKING:
    from manimgeo.components.point import Point
    from manimgeo.components.vector import Vector

LineConstructType = Literal["PP", "PV"]

class LineAdapter(GeometryAdapter):
    start: np.ndarray
    end: np.ndarray
    length: np.ndarray
    unit_direction: np.ndarray

    def __init__(
            self,
            construct_type: LineConstructType,
            current_geo_obj: Union["LineSegment", "Ray", "InfinityLine"],
            *objs: Union[BaseGeometry, any]
        ):
        """
        PP: 线上始终点
        """
        super().__init__(construct_type)

        [obj.add_dependent(current_geo_obj) for obj in objs if isinstance(obj, BaseGeometry)]

    def __call__(self, *objs: Union[BaseGeometry, any]):
        from manimgeo.components.point import Point
        from manimgeo.components.vector import Vector
        
        match self.construct_type:
            case "PP":
                GeoUtils.check_params(objs, Point, Point)
                self.start = objs[0].coord
                self.end = objs[1].coord

            case "PV":
                GeoUtils.check_params(objs, Point, Vector)
                self.start = objs[0].coord
                self.end = objs[0].coord + objs[1].vec
            
            case _:
                raise ValueError(f"Invalid constructing method: {self.construct_type}")
            
        self.length = np.linalg.norm(self.end - self.start)
        self.unit_direction = (self.end - self.start) / self.length

class Line(BaseGeometry):
    attrs = ["start", "end", "length", "unit_direction"]
    start: np.ndarray
    end: np.ndarray
    length: np.ndarray
    unit_direction: np.ndarray

    line_type: str

    def __init__(self, construct_type: LineConstructType, line_type: str, *objs, name: str = ""):
        """通过指定构造方式与对象构造线"""
        super().__init__(GeoUtils.get_name(name, self, construct_type))
        self.line_type = line_type
        self.objs = objs
        self.adapter = LineAdapter(construct_type, self, *objs)
        self.update()

class LineSegment(Line):
    def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
        """通过指定构造方式与对象构造线段"""
        super().__init__(construct_type, "LineSegment", *objs, name=name)

class Ray(Line):
    def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
        """通过指定构造方式与对象构造射线"""
        super().__init__(construct_type, "Ray", *objs, name=name)

class InfinityLine(Line):
    def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
        """通过指定构造方式与对象构造直线"""
        super().__init__(construct_type, "InfinityLine", *objs, name=name)

# Constructing Methods

def LineSegmentPP(start: Point, end: Point, name: str = ""):
    """
    ## 起始点构造线段

    `start`: 起点
    `end`: 终点
    """
    return LineSegment("PP", start, end, name=name)

def RayPP(start: Point, end: Point, name: str = ""):
    """
    ## 起始点构造射线

    `start`: 起点
    `end`: 终点
    """
    return Ray("PP", start, end, name=name)

def InfinityLinePP(start: Point, end: Point, name: str = ""):
    """
    ## 起始点构造直线

    `start`: 起点
    `end`: 终点
    """
    return InfinityLine("PP", start, end, name=name)