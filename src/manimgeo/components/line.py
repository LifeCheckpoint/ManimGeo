from __future__ import annotations

from ..components.base import GeometryAdapter, BaseGeometry
from ..utils.mathe import GeoMathe
from ..utils.utils import GeoUtils
from pydantic import Field
from typing import TYPE_CHECKING, Union, Literal, List, Callable, Optional, Any, cast
import numpy as np

if TYPE_CHECKING:
    from .point.point import Point
    from ..components.vector import Vector
    from ..components.circle import Circle

LineConstructType = Literal[
    "PP", "PV", "TranslationLV", "VerticalPL", "ParallelPL",
    # "TangentsCirP", "TangentsOutCirCir", "TangentsInCirCir",
]
Number = Union[float, int]

class LineAdapter(GeometryAdapter):
    start: np.ndarray = Field(default=np.zeros(2), description="计算线首坐标", init=False)
    end: np.ndarray = Field(default=np.zeros(2), description="计算线尾坐标", init=False)
    length: Number = Field(default=0.0, description="计算线长度", init=False)

    unit_direction: np.ndarray = Field(default=np.zeros(2), description="计算线单位方向向量", init=False)
    objs: List[Union[BaseGeometry, Any]] = Field(description="线适配器依赖的其他对象列表")

    construct_type: LineConstructType = Field(description="线计算方式")

    def __call__(self, *objs: Union[BaseGeometry, Any]):
        from .point.point import Point
        from ..components.vector import Vector
        from ..components.circle import Circle

        op_type_map = {
            "PP": [Point, Point],
            "PV": [Point, Vector],
            "TranslationLV": [Line, Vector],
            "VerticalPL": [Point, Line],
            "ParallelPL": [Point, Line],
            "TangentsCirP": [Circle, Point],
            "TangentsOutCirCir": [Circle, Circle],
            "TangentsInCirCir": [Circle, Circle],
        }
        GeoUtils.check_params_batch(op_type_map, self.construct_type, objs)
        
        match self.construct_type:
            case "PP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                self.start = point1.coord
                self.end = point2.coord

            case "PV":
                point = cast(Point, objs[0])
                vector = cast(Vector, objs[1])
                self.start = point.coord
                self.end = point.coord + vector.vec

            case "TranslationLV":
                line = cast(Line, objs[0])
                vector = cast(Vector, objs[1])
                self.start = line.start + vector.vec
                self.end = line.end + vector.vec

            case "VerticalPL":
                point = cast(Point, objs[0])
                line = cast(Line, objs[1])
                if not GeoMathe.is_point_on_infinite_line(point.coord, line.start, line.end):
                    self.start = GeoMathe.vertical_point_to_line(point.coord, line.start, line.end)
                    self.end = point.coord
                else:
                    direction = GeoMathe.vertical_line_unit_direction(line.start, line.end)
                    self.start = point.coord
                    self.end = self.start + direction

            case "ParallelPL":
                point = cast(Point, objs[0])
                line = cast(Line, objs[1])
                self.start = point.coord
                self.end = point.coord + (line.end - line.start)

            # case "TangentsCirP":
            #     circle = cast(Circle, objs[0])
            #     point = cast(Point, objs[1])
            #     self.start1 = point.coord.copy()
            #     self.start2 = point.coord.copy()
            #     tangent_ps = GeoMathe.find_tangent_points(point.coord, circle.center, circle.radius)
            #     if len(tangent_ps) == 2:
            #         self.end1 = tangent_ps[0]
            #         self.end2 = tangent_ps[1]
            #     elif len(tangent_ps) == 1:
            #         self.end1 = tangent_ps[0] + GeoMathe.vertical_line_unit_direction(tangent_ps[0], objs[0].center)
            #         self.end2 = self.end1.copy()
            #     else:
            #         raise ValueError("No tangent points found")
                
            # case "TangentsOutCirCir":
            #     outs = GeoMathe.external_tangents(objs[0].center, objs[0].radius, objs[1].center, objs[1].radius)
            #     if len(outs) == 2:
            #         self.start1, self.end1 = outs[0][0], outs[0][1]
            #         self.start2, self.end2 = outs[1][0], outs[1][1]
            #     else:
            #         raise ValueError("No tangent points found")

            # case "TangentsInCirCir":
            #     outs = GeoMathe.internal_tangents(objs[0].center, objs[0].radius, objs[1].center, objs[1].radius)
            #     if len(outs) == 2:
            #         self.start1, self.end1 = outs[0][0], outs[0][1]
            #         self.start2, self.end2 = outs[1][0], outs[1][1]
            #     else:
            #         raise ValueError("No tangent points found")
                
            # case "2":
            #     if objs[1] == 0:
            #         self.start, self.end = objs[0].start1, objs[0].end1
            #     elif objs[1] == 1:
            #         self.start, self.end = objs[0].start2, objs[0].end2
            #     else:
            #         raise ValueError("Index of lines should be 0 or 1")
                
            # case "2Filter":
            #     if objs[1](objs[0].start1, objs[0].end1):
            #         self.start, self.end = objs[0].start1, objs[0].end1
            #     elif objs[1](objs[0].start2, objs[0].end2):
            #         self.start, self.end = objs[0].start2, objs[0].end2
            #     else:
            #         raise ValueError("No line fits condition")
            
            case _:
                raise ValueError(f"Invalid constructing method: {self.construct_type}")
            
        # if hasattr(self, "end"): # 检查是否为单线对象
        self.length = np.linalg.norm(self.end - self.start) # type: ignore
        self.unit_direction = (self.end - self.start) / self.length

class Line(BaseGeometry):
    """
    线对象，允许以下构造
    - `PP`: 始终点构造线
    - `PV`: 始点方向构造线
    - `TranslationLV`: 平移构造线
    - `VerticalPL`: 点与线构造垂直线
    - `ParallelPL`: 点与线构造平行线
    - `TangentsCirP`: 圆与点构造切线
    - `TangentsOutCirCir`: 圆与圆构造外切线
    - `TangentsInCirCir`: 圆与圆构造内切线
    """
    
    attrs: List[str] = Field(default=["start", "end", "length", "unit_direction"], description="线对象属性列表", init=False)
    start: np.ndarray = Field(default=np.zeros(2), description="线首坐标", init=False)
    end: np.ndarray = Field(default=np.zeros(2), description="线尾坐标", init=False)
    length: Number = Field(default=0.0, description="线长度", init=False)
    unit_direction: np.ndarray = Field(default=np.zeros(2), description="线单位方向向量", init=False)

    construct_type: LineConstructType = Field(description="线构造方式")
    adapter: LineAdapter = Field(description="线参数适配器", init=False)
    line_type: str = Field(description="线类型")

    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        self.adapter = LineAdapter(
            construct_type=self.construct_type,
            objs=self.objs,
        )
        self.name = GeoUtils.get_name(self.name, self, self.adapter.construct_type)

        # 为上游对象添加依赖关系
        for obj in self.objs:
            if isinstance(obj, BaseGeometry):
                obj.add_dependent(self)

        self.update()

    # 构造方法

    @staticmethod
    def TranslationLV(line: Line, vec: Vector, name: str = "") -> Line:
        """
        ## 平移构造线

        `line`: 原线
        `vec`: 平移向量
        """
        return Line(
            name=name,
            construct_type="TranslationLV",
            objs=[line, vec],
            line_type=line.line_type
        )

class LineSegment(Line):
    line_type: str = Field(default="LineSegment", description="线段类型", init=False)

    @staticmethod
    def PP(start: Point, end: Point, name: str = "") -> LineSegment:
        """
        ## 起始点构造线段

        `start`: 起点
        `end`: 终点
        """
        return LineSegment(
            name=name,
            construct_type="PP",
            objs=[start, end]
        )
    
    @staticmethod
    def PV(start: Point, vector: Vector, name: str = "") -> LineSegment:
        """
        ## 起点方向构造线段

        `start`: 起点
        `vector`: 方向向量
        """
        return LineSegment(
            name=name,
            construct_type="PV",
            objs=[start, vector]
        )
    
    @staticmethod
    def VerticalPL(point: Point, line: Line, name: str = "") -> LineSegment:
        """
        ## 点与线构造垂直线段

        `point`: 垂线经过点
        `line`: 原线
        """
        return LineSegment(
            name=name,
            construct_type="VerticalPL",
            objs=[point, line]
        )
    
    @staticmethod
    def ParallelPL(point: Point, line: Line, name: str = "") -> LineSegment:
        """
        ## 点与线构造平行线段

        `point`: 平行线经过点
        `line`: 原线
        """
        return LineSegment(
            name=name,
            construct_type="ParallelPL",
            objs=[point, line]
        )

class Ray(Line):
    line_type: str = Field(default="Ray", description="射线类型", init=False)

    @staticmethod
    def PP(start: Point, end: Point, name: str = "") -> Ray:
        """
        ## 起始点构造射线

        `start`: 起点
        `end`: 终点
        """
        return Ray(
            name=name,
            construct_type="PP",
            objs=[start, end]
        )
    
    @staticmethod
    def PV(start: Point, vector: Vector, name: str = "") -> Ray:
        """
        ## 起点方向构造射线

        `start`: 起点
        `vector`: 方向向量
        """
        return Ray(
            name=name,
            construct_type="PV",
            objs=[start, vector]
        )
    
    @staticmethod
    def VerticalPL(point: Point, line: Line, name: str = "") -> Ray:
        """
        ## 点与线构造垂直射线

        `point`: 垂线经过点
        `line`: 原线
        """
        return Ray(
            name=name,
            construct_type="VerticalPL",
            objs=[point, line]
        )
    
    @staticmethod
    def ParallelPL(point: Point, line: Line, name: str = "") -> Ray:
        """
        ## 点与线构造平行射线

        `point`: 平行线经过点
        `line`: 原线
        """
        return Ray(
            name=name,
            construct_type="ParallelPL",
            objs=[point, line]
        )
    
class InfinityLine(Line):
    line_type: str = Field(default="InfinityLine", description="直线类型", init=False)

    @staticmethod
    def PP(start: Point, end: Point, name: str = "") -> InfinityLine:
        """
        ## 起始点构造直线

        `start`: 起点
        `end`: 终点
        """
        return InfinityLine(
            name=name,
            construct_type="PP",
            objs=[start, end]
        )
    
    @staticmethod
    def PV(start: Point, vector: Vector, name: str = "") -> InfinityLine:
        """
        ## 起点方向构造直线

        `start`: 起点
        `vector`: 方向向量
        """
        return InfinityLine(
            name=name,
            construct_type="PV",
            objs=[start, vector]
        )
    
    @staticmethod
    def VerticalPL(point: Point, line: Line, name: str = "") -> InfinityLine:
        """
        ## 点与线构造垂直直线

        `point`: 垂线经过点
        `line`: 原线
        """
        return InfinityLine(
            name=name,
            construct_type="VerticalPL",
            objs=[point, line]
        )
    
    @staticmethod
    def ParallelPL(point: Point, line: Line, name: str = "") -> InfinityLine:
        """
        ## 点与线构造平行直线

        `point`: 平行线经过点
        `line`: 原线
        """
        return InfinityLine(
            name=name,
            construct_type="ParallelPL",
            objs=[point, line]
        )


# 多线条

# class Lines2(BaseGeometry):
#     attrs = ["start1", "end1", "start2", "end2"]
#     start1: np.ndarray
#     end1: np.ndarray
#     start2: np.ndarray
#     end2: np.ndarray

#     line_type: str

#     def __init__(self, construct_type: LineConstructType, line_type: str, *objs, name: str = ""):
#         """通过指定构造方式与对象构造线对"""
#         super().__init__(GeoUtils.get_name(name, self, construct_type))
#         self.line_type = line_type
#         self.objs = objs
#         self.adapter = LineAdapter(construct_type, self, *objs)
#         self.update()

# class LineSegments2(Lines2):
#     def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
#         """通过指定构造方式与对象构造线段对"""
#         super().__init__(construct_type, "LineSegment", *objs, name=name)

# class Rays2(Lines2):
#     def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
#         """通过指定构造方式与对象构造射线对"""
#         super().__init__(construct_type, "Ray", *objs, name=name)

# class InfinityLines2(Lines2):
#     def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
#         """通过指定构造方式与对象构造直线对"""
#         super().__init__(construct_type, "InfinityLine", *objs, name=name)

# Constructing Methods

# def Lines2TangentsCirP(circle: Circle, point: Point, name: str = ""):
#     """
#     ## 过一点构造圆切线

#     `circle`: 圆
#     `point`: 圆外或圆上一点
#     """
#     return InfinityLines2("TangentsCirP", circle, point, name=name)

# def Lines2TangentsOutCirCir(
#         circle1: Circle, circle2: Circle, 
#         filter: Optional[Callable[[np.ndarray, np.ndarray], bool]] = None, 
#         name: str = ""
#     ) -> Union[List[InfinityLine], InfinityLine]:
#     """
#     ## 构造两圆外切线

#     `circle1`: 圆1
#     `circle2`: 圆2
#     `filter`: 返回线始终点须满足的条件，如果提供则返回第一个满足条件的单线对象
#     """
#     lines2 = InfinityLines2("TangentsOutCirCir", circle1, circle2, name=name)
#     if filter == None:
#         return LineOfLines2List(lines2, name=name)
#     else:
#         return LineOfLines2Fit(lines2, filter, name=name)

# def Lines2TangentsInCirCir(
#         circle1: Circle, circle2: Circle, 
#         filter: Optional[Callable[[np.ndarray, np.ndarray], bool]] = None, 
#         name: str = ""
#     ) -> Union[List[InfinityLine], InfinityLine]:
#     """
#     ## 构造两圆内切线

#     `circle1`: 圆1
#     `circle2`: 圆2
#     `filter`: 返回线始终点须满足的条件，如果提供则返回第一个满足条件的单线对象
#     """
#     lines2 = InfinityLines2("TangentsInCirCir", circle1, circle2, name=name)
#     if filter == None:
#         return LineOfLines2List(lines2, name=name)
#     else:
#         return LineOfLines2Fit(lines2, filter, name=name)

# def LineOfLines2(lines2: Lines2, index: Literal[0, 1], name: str = "") -> Line:
#     """
#     ## 获取两条线中的单线对象

#     `lines2`: 两线组合对象
#     `index`: 两线中的其中一线索引
#     """
#     line_map = {
#         LineSegments2: LineSegment,
#         Rays2: Ray,
#         InfinityLines2: InfinityLine
#     }
#     return line_map[lines2.__class__]("2", lines2, index, name=name)

# def LineOfLines2List(lines2: Lines2, name: str = "") -> List[Line, Line]:
#     """
#     ## 获取两线中的单线对象列表

#     `lines2`: 两线组合对象
#     """
#     return [LineOfLines2(lines2, 0, name), LineOfLines2(lines2, 1, name)]

# def LineOfLines2Fit(lines2: Lines2, filter: Callable[[np.ndarray, np.ndarray], bool], name: str = ""):
#     """
#     ## 获得两点中符合条件的第一个单点对象

#     `points2`: 两点组合对象
#     `filter`: 给定点坐标，返回是否符合条件
#     """
#     line_map = {
#         LineSegments2: LineSegment,
#         Rays2: Ray,
#         InfinityLines2: InfinityLine
#     }
#     return line_map[lines2.__class__]("2Filter", lines2, filter, name=name)