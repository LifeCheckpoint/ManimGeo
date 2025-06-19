from __future__ import annotations

from ...utils.mathe import GeoMathe
from ...utils.utils import GeoUtils
from ..base import GeometryAdapter, BaseGeometry
from .construct import CircleConstructType, Number
from pydantic import Field
from typing import TYPE_CHECKING, List, Union, Any, cast
import numpy as np

if TYPE_CHECKING:
    from ..point import Point
    from ..vector import Vector
    from ..line import LineSegment
    from .circle import Circle

class CircleAdapter(GeometryAdapter):
    center: np.ndarray = Field(default=np.zeros(2), description="计算圆心坐标")
    radius: Number = Field(default=0.0, description="计算圆半径")
    area: Number = Field(default=0.0, description="计算圆面积")
    circumference: Number = Field(default=0.0, description="计算圆周长")
    construct_type: CircleConstructType = Field(description="圆计算方式")
    objs: List[Union[BaseGeometry, Any]] = Field(description="圆适配器依赖的其他对象列表")

    def __call__(self, *objs: Union[BaseGeometry, Any]):

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
                self.center = cast(Point, objs[0]).coord.copy()
                self.radius = cast(Number, objs[1])

            case "PP":
                center = cast(Point, objs[0])
                point = cast(Point, objs[1])
                self.center = center.coord.copy()
                self.radius = np.linalg.norm(point.coord - center.coord) # type: ignore

            case "L":
                start = cast(LineSegment, objs[0]).start.copy()
                end = cast(LineSegment, objs[0]).end.copy()
                self.center = start
                self.radius = np.linalg.norm(end - start) # type: ignore

            case "PPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                self.radius, self.center = GeoMathe.circumcenter_r_c(
                    point1.coord, point2.coord, point3.coord
                )

            case "TranslationCirV":
                circle = cast(Circle, objs[0])
                vec = cast(Vector, objs[1])
                self.center = circle.center + vec.vec
                self.radius = circle.radius

            case "InverseCirCir":
                circle = cast(Circle, objs[0])
                base_circle = cast(Circle, objs[1])
                self.center, self.radius = GeoMathe.inverse_circle(circle.center, circle.radius, base_circle.center, base_circle.radius)

            case "InscribePPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                self.radius, self.center = GeoMathe.inscribed_r_c(point1.coord, point2.coord, point3.coord)

            case _:
                raise NotImplementedError(f"Invalid constructing method: {self.construct_type}")

        self.area = np.pi * self.radius ** 2
        self.circumference = 2 * np.pi * self.radius
