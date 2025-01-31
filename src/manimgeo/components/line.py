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
    from manimgeo.components.circle import Circle

LineConstructType = Literal[
    "PP", "PV", "TranslationLV", "VerticalPL", "ParallelPL",
    "TangentsCirP", "TangentsOutCirCir", "TangentsInCirCir"
]

class LineAdapter(GeometryAdapter):
    start: np.ndarray
    end: np.ndarray
    length: np.ndarray
    unit_direction: np.ndarray

    start1: np.ndarray
    end1: np.ndarray
    start2: np.ndarray
    end2: np.ndarray

    def __init__(
            self,
            construct_type: LineConstructType,
            current_geo_obj: Union[
                "LineSegment", "Ray", "InfinityLine", 
                "LineSegments2", "Rays2", "InfinityLines2"
            ],
            *objs: Union[BaseGeometry, any]
        ):
        """
        PP: 始终点构造线
        PV: 始点方向构造线
        TranslationLV: 平移构造线
        VerticalPL: 点与线构造垂直线
        ParallelPL: 点与线构造平行线
        TangentsCirP: 圆与点构造切线
        TangentsOutCirCir: 圆与圆构造外切线
        TangentsInCirCir: 圆与圆构造内切线
        """
        super().__init__(construct_type)

        [obj.add_dependent(current_geo_obj) for obj in objs if isinstance(obj, BaseGeometry)]

    def __call__(self, *objs: Union[BaseGeometry, any]):
        from manimgeo.components.point import Point
        from manimgeo.components.vector import Vector
        from manimgeo.components.circle import Circle

        op_type_map = {
            "PP": [Point, Point],
            "PV": [Point, Vector],
            "TranslationLV": [Line, Vector],
            "VerticalPL": [Point, Line],
            "ParallelPL": [Point, Line],
            "TangentsCirP": [Circle, Point],
            "TangentsOutCirCir": [Circle, Circle],
            "TangentsInCirCir": [Circle, Circle]
        }
        GeoUtils.check_params_batch(op_type_map, self.construct_type, objs)
        
        match self.construct_type:
            case "PP":
                self.start = objs[0].coord
                self.end = objs[1].coord

            case "PV":
                self.start = objs[0].coord
                self.end = objs[0].coord + objs[1].vec

            case "TranslationLV":
                self.start = objs[0].start + objs[1].vec
                self.end = objs[0].end + objs[1].vec

            case "VerticalPL":
                if not GeoMathe.is_point_on_infinite_line(objs[0].coord, objs[1].start, objs[1].end):
                    self.start = GeoMathe.vertical_point_to_line(objs[0].coord, objs[1].start, objs[1].end)
                    self.end = objs[0].coord
                else:
                    direction = GeoMathe.vertical_line_unit_direction(objs[1].start, objs[1].end)
                    self.start = objs[0].coord
                    self.end = self.start + direction

            case "ParallelPL":
                self.start = objs[0].coord
                self.end = objs[0].coord + (objs[1].end - objs[1].start)

            case "TangentsCirP":
                self.start1 = objs[1].coord.copy()
                self.start2 = objs[1].coord.copy()
                tangent_ps = GeoMathe.find_tangent_points(objs[1].coord, objs[0].center, objs[0].radius)
                if len(tangent_ps) == 2:
                    self.end1 = tangent_ps[0]
                    self.end2 = tangent_ps[1]
                elif len(tangent_ps) == 1:
                    self.end1 = tangent_ps[0] + GeoMathe.vertical_line_unit_direction(tangent_ps[0], objs[0].center)
                    self.end2 = self.end1.copy()
                else:
                    raise ValueError("No tangent points found")
                
            case "TangentsOutCirCir":
                outs = GeoMathe.external_tangents(objs[0].center, objs[0].radius, objs[1].center, objs[1].radius)
                if len(outs) == 2:
                    self.start1, self.end1 = outs[0][0], outs[0][1]
                    self.start2, self.end2 = outs[1][0], outs[1][1]
                else:
                    raise ValueError("No tangent points found")

            case "TangentsInCirCir":
                outs = GeoMathe.internal_tangents(objs[0].center, objs[0].radius, objs[1].center, objs[1].radius)
                if len(outs) == 2:
                    self.start1, self.end1 = outs[0][0], outs[0][1]
                    self.start2, self.end2 = outs[1][0], outs[1][1]
                else:
                    raise ValueError("No tangent points found")
            
            case _:
                raise ValueError(f"Invalid constructing method: {self.construct_type}")
            
        self.length = np.linalg.norm(self.end - self.start)
        self.unit_direction = (self.end - self.start) / self.length

# 单线条

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

# 多线条

class Lines2(BaseGeometry):
    attrs = ["start1", "end1", "start2", "end2"]
    start1: np.ndarray
    end1: np.ndarray
    start2: np.ndarray
    end2: np.ndarray

    line_type: str

    def __init__(self, construct_type: LineConstructType, line_type: str, *objs, name: str = ""):
        """通过指定构造方式与对象构造线对"""
        super().__init__(GeoUtils.get_name(name, self, construct_type))
        self.line_type = line_type
        self.objs = objs
        self.adapter = LineAdapter(construct_type, self, *objs)
        self.update()

class LineSegments2(Lines2):
    def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
        """通过指定构造方式与对象构造线段对"""
        super().__init__(construct_type, "LineSegment", *objs, name=name)

class Rays2(Lines2):
    def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
        """通过指定构造方式与对象构造射线对"""
        super().__init__(construct_type, "Ray", *objs, name=name)

class InfinityLines2(Lines2):
    def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
        """通过指定构造方式与对象构造直线对"""
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

def LineTangentsCirP(circle: Circle, point: Point, name: str = ""):
    """
    ## 过一点构造圆切线

    `circle`: 圆
    `point`: 圆外或圆上一点
    """
    return InfinityLines2("TangentsCirP", circle, point, name=name)

def LineTangentsOutCirCir(circle1: Circle, circle2: Circle, name: str = ""):
    """
    ## 构造两圆外切线

    `circle1`: 圆1
    `circle2`: 圆2
    """
    return InfinityLines2("TangentsOutCirCir", circle1, circle2, name=name)

def LineTangentsInCirCir(circle1: Circle, circle2: Circle, name: str = ""):
    """
    ## 构造两圆内切线

    `circle1`: 圆1
    `circle2`: 圆2
    """
    return InfinityLines2("TangentsInCirCir", circle1, circle2, name=name)
