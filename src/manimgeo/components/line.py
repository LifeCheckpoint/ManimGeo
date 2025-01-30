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

LineConstructType = Literal[
    "PP", "PV", "TranslationLV", "VerticalPL", "ParallelPL"
]

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
        PP: 始终点构造线
        PV: 始点方向构造线
        TranslationLV: 平移构造线
        VerticalPL: 点与线构造垂直线
        ParallelPL: 点与线构造平行线
        """
        super().__init__(construct_type)

        [obj.add_dependent(current_geo_obj) for obj in objs if isinstance(obj, BaseGeometry)]

    def __call__(self, *objs: Union[BaseGeometry, any]):
        from manimgeo.components.point import Point, PointVerticalPL
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

            case "TranslationLV":
                GeoUtils.check_params(objs, Line, Vector)
                self.start = objs[0].start + objs[1].vec
                self.end = objs[0].end + objs[1].vec

            case "VerticalPL":
                GeoUtils.check_params(objs, Point, Line)
                if not GeoMathe.is_point_on_infinite_line(objs[0].coord, objs[1].start, objs[1].end):
                    self.start = GeoMathe.vertical_point_to_line(objs[0].coord, objs[1].start, objs[1].end)
                    self.end = objs[0].coord
                else:
                    direction = GeoMathe.vertical_line(objs[1].start, objs[1].end)
                    self.start = objs[0].coord
                    self.end = self.start + direction

            case "ParallelPL":
                GeoUtils.check_params(objs, Point, Line)
                self.start = objs[0].coord
                self.end = objs[0].coord + (objs[1].end - objs[1].start)
            
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

def LineTranslation(line: Line, vec: Vector, name: str = ""):
    """
    ## 平移构造线

    `line`: 原线
    `vec`: 平移向量
    """
    return line.__class__("TranslationLV", line, vec, name=name)

def LineVerticalPL(point: Point, line: Line, name: str = ""):
    """
    ## 垂直构造线

    `point`: 垂线经过点
    `line`: 原线
    """
    return line.__class__("VerticalPL", point, line, name=name)

def LineParallelPL(point: Point, line: Line, name: str = ""):
    """
    ## 平行构造线

    `point`: 平行线经过点
    `line`: 原线
    """
    return line.__class__("ParallelPL", point, line, name=name)