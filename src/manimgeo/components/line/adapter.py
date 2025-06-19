from __future__ import annotations

from ...utils.mathe import GeoMathe
from ...utils.utils import GeoUtils
from ..base import GeometryAdapter, BaseGeometry
from .construct import LineConstructType, Number
from pydantic import Field
from typing import TYPE_CHECKING, Union, List, Any, cast
import numpy as np

if TYPE_CHECKING:
    from ..circle import Circle
    from ..point import Point
    from ..vector import Vector
    from .line import Line

class LineAdapter(GeometryAdapter):
    start: np.ndarray = Field(default=np.zeros(2), description="计算线首坐标", init=False)
    end: np.ndarray = Field(default=np.zeros(2), description="计算线尾坐标", init=False)
    length: Number = Field(default=0.0, description="计算线长度", init=False)

    unit_direction: np.ndarray = Field(default=np.zeros(2), description="计算线单位方向向量", init=False)
    objs: List[Union[BaseGeometry, Any]] = Field(description="线适配器依赖的其他对象列表")

    construct_type: LineConstructType = Field(description="线计算方式")

    def __call__(self, *objs: Union[BaseGeometry, Any]):
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