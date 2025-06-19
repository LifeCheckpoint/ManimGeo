from __future__ import annotations

from .construct import PointConstructType, Number
from .point import Point
from ..base import GeometryAdapter, BaseGeometry
from ...utils.mathe import GeoMathe
from ...utils.utils import GeoUtils
from pydantic import Field
from typing import TYPE_CHECKING, Union, Any, List, cast
import numpy as np

if TYPE_CHECKING:
    from ..angle.angle import Angle
    from ..line.line import Line, LineSegment
    from ..vector.vector import Vector


class PointAdapter(GeometryAdapter):
    coord: np.ndarray = Field(default=np.zeros(2), description="计算点坐标", init=False)
    
    construct_type: PointConstructType = Field(description="点计算方式")
    objs: List[Union[BaseGeometry, Any]] = Field(description="点适配器依赖的其他对象列表")

    def __call__(self, *objs: Union[BaseGeometry, Any]):
        from ..line.line import Line, LineSegment
        from ..circle.circle import Circle
        from ..vector.vector import Vector
        from ..angle.angle import Angle

        op_type_map = {
            "Free": [np.ndarray], "Constraint": [np.ndarray],
            "MidPP": [Point, Point],
            "MidL": [LineSegment],
            "ExtensionPP": [Point, Point, Number], # start, through, factor
            "AxisymmetricPL": [Point, Line],
            "VerticalPL": [Point, Line],
            "ParallelPL": [Point, Line, Number], # point, line, absolute_distance
            "InversionPCir": [Point, Circle],
            "IntersectionLL": [Line, Line, bool], # line1, line2, regard_as_infinite
            "IntersectionLCir": [Line, Circle, bool], # line, circle, regard_as_infinite
            "IntersectionCirCir": [Circle, Circle],
            "TranslationPV": [Point, Vector],
            "CentroidPPP": [Point, Point, Point],
            "CircumcenterPPP": [Point, Point, Point],
            "IncenterPPP": [Point, Point, Point],
            "OrthocenterPPP": [Point, Point, Point],
            "Cir": [Circle],
            "RotatePPA": [Point, Point, Angle] # point, center, angle
        }
        GeoUtils.check_params_batch(op_type_map, self.construct_type, objs)

        match self.construct_type:
            case "Free" | "Constraint":
                self.coord = cast(np.ndarray, objs[0])

            case "MidPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                self.coord = (point1.coord + point2.coord) / 2

            case "MidL":
                seg_line = cast(LineSegment, objs[0])
                self.coord = (seg_line.start + seg_line.end) / 2

            case "ExtensionPP":
                start = cast(Point, objs[0])
                through = cast(Point, objs[1])
                factor = cast(Number, objs[2])
                self.coord = start.coord + factor * (through.coord - start.coord)

            case "AxisymmetricPL":
                point = cast(Point, objs[0])
                line = cast(Line, objs[1])
                self.coord = GeoMathe.axisymmetric_point(point.coord, line.start, line.end)

            case "VerticalPL":
                point = cast(Point, objs[0])
                line = cast(Line, objs[1])
                self.coord = GeoMathe.vertical_point_to_line(point.coord, line.start, line.end)

            case "ParallelPL":
                point = cast(Point, objs[0])
                line = cast(Line, objs[1])
                distance = cast(Number, objs[2])
                self.coord = point.coord + distance * line.unit_direction

            case "InversionPCir":
                point = cast(Point, objs[0])
                circle = cast(Circle, objs[1])
                self.coord = GeoMathe.inversion_point(point.coord, circle.center, circle.radius)

            case "IntersectionLL":
                line1 = cast(Line, objs[0])
                line2 = cast(Line, objs[1])
                regard_infinite = cast(bool, objs[2])
                result = GeoMathe.intersection_line_line(
                    line1.start, line1.end,
                    line2.start, line2.end,
                    type(line1).__name__, type(line2).__name__, # type: ignore
                    regard_infinite
                )
                if result[0] and result[1] is not None:
                    self.coord = result[1]
                elif result[0] and result[1] is None:
                    raise ValueError("Infinites intersections")
                else:
                    raise ValueError("No intersections")
                
            # case "IntersectionLCir":
            #     result = GeoMathe.intersection_line_cir(
            #             objs[0].start, objs[0].end,
            #             objs[1].center, objs[1].radius,
            #             type(objs[0]).__name__ if not objs[2] else "InfinityLine"
            #         )
            #     if len(result) == 0:
            #         raise ValueError("No intersections")
            #     elif len(result) == 1:
            #         self.coord1 = result[0].copy()
            #         self.coord2 = result[0].copy()
            #     else:
            #         self.coord1 = result[0].copy()
            #         self.coord2 = result[1].copy()

            # case "IntersectionCirCir":
            #     result = GeoMathe.intersection_cir_cir(
            #             objs[0].center, objs[0].radius,
            #             objs[1].center, objs[1].radius
            #         )
            #     if result[0] and len(result[1]) == 2:
            #         self.coord1 = result[1][0]
            #         self.coord2 = result[1][1]
            #     elif result[0] and len(result[1]) == 1:
            #         self.coord1 = result[1][0].copy()
            #         self.coord2 = result[1][0].copy()
            #     elif result[0] and len(result[1]) == 0:
            #         raise ValueError("Two circles has infinite intersections")
            #     else:
            #         raise ValueError("Two circles has no intersection")

            case "TranslationPV":
                point = cast(Point, objs[0])
                vector = cast(Vector, objs[1])
                self.coord = point.coord + vector.vec

            case "CentroidPPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                self.coord = (point1.coord + point2.coord + point3.coord) / 3

            case "CircumcenterPPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                _, self.coord = GeoMathe.circumcenter_r_c(
                    point1.coord, point2.coord, point3.coord
                )

            case "IncenterPPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                _, self.coord = GeoMathe.inscribed_r_c(
                    point1.coord, point2.coord, point3.coord
                )

            case "OrthocenterPPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                self.coord = GeoMathe.orthocenter(
                    point1.coord, point2.coord, point3.coord
                )

            case "Cir":
                circle = cast(Circle, objs[0])
                self.coord = circle.center

            # case "2":
            #     if objs[1] == 0:
            #         self.coord = objs[0].coord1
            #     elif objs[1] == 1:
            #         self.coord = objs[0].coord2
            #     else:
            #         raise ValueError("Index of points should be 0 or 1")
                
            # case "2Filter":
            #     if objs[1](objs[0].coord1):
            #         self.coord = objs[0].coord1
            #     elif objs[1](objs[0].coord2):
            #         self.coord = objs[0].coord2
            #     else:
            #         raise ValueError("No point fits condition")
                
            case "RotatePPA":
                point = cast(Point, objs[0])
                center = cast(Point, objs[1])
                angle = cast(Angle, objs[2])
                angle_num = angle.angle if angle.turn == 'Counterclockwise' else (2 * np.pi - angle.angle) # type: ignore
                self.coord = GeoMathe.angle_3p_countclockwise(point.coord, center.coord, angle_num) # type: ignore

            case _:
                raise NotImplementedError(f"Invalid construct type: {self.construct_type}")
