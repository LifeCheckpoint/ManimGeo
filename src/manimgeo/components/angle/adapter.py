from __future__ import annotations

from .construct import AngleConstructType, Number
from ...utils.mathe import GeoMathe
from ...utils.utils import GeoUtils
from ..base import GeometryAdapter, BaseGeometry
from pydantic import Field
from typing import TYPE_CHECKING, Union, Literal, Any, cast
import numpy as np

if TYPE_CHECKING:
    from ..point.point import Point
    from ..point.point import Point
    from ..line.line import Line, LineSegment
    from .angle import Angle

class AngleAdapter(GeometryAdapter):
    angle: Number = Field(default=0.0, description="计算角度", init=False)
    turn: Literal["Clockwise", "Counterclockwise"] = Field(default="Counterclockwise", description="角度计算方向", init=False)

    construct_type: AngleConstructType = Field(description="角计算方式")
    objs: list[Union[BaseGeometry, Any]] = Field(description="角适配器依赖的其他对象列表")

    def __call__(self, *objs: Union[BaseGeometry, Any]):
        op_type_map = {
            "PPP": [Point, Point, Point], # start, center, end
            "LL": [Line, Line],
            "LP": [Line, Point],
            "N": [Number, str],
            "TurnA": [Angle],
            "AddAA": [Angle, Angle],
            "SubAA": [Angle, Angle],
            "MulNA": [Angle, Angle]
        }
        GeoUtils.check_params_batch(op_type_map, self.construct_type, objs)
        
        match self.construct_type:
            case "PPP":
                start = cast(Point, objs[0])
                center = cast(Point, objs[1])
                end = cast(Point, objs[2])
                self.angle = GeoMathe.angle_3p_countclockwise(start.coord, center.coord, end.coord)
                self.turn = "Counterclockwise"

            case "LL":
                line1 = cast(Line, objs[0])
                line2 = cast(Line, objs[1])
                if not np.allclose(line1.start, line2.start):
                    raise ValueError("无法从起始点不等的两条线构造角")
                self.angle = GeoMathe.angle_3p_countclockwise(line1.end, line1.start, line2.end)
                self.turn = "Counterclockwise"

            case "LP":
                line = cast(LineSegment, objs[0])
                point = cast(Point, objs[1])
                self.angle = GeoMathe.angle_3p_countclockwise(line.end, line.start, point.coord)
                self.turn = "Counterclockwise"

            case "N":
                angle = cast(Number, objs[0])
                turn = cast(Literal["Clockwise", "Counterclockwise"], objs[1])
                if turn not in ["Clockwise", "Counterclockwise"]:
                    raise ValueError("角度方向必须为 'Clockwise' 或 'Counterclockwise'")
                self.angle = angle
                self.turn = turn
            
            case "TurnA":
                angle = cast(Angle, objs[0])
                self.angle = 2 * np.pi - angle.angle
                self.turn = "Counterclockwise" if angle.turn == "Clockwise" else "Clockwise"

            case "AddAA":
                angle1 = cast(Angle, objs[0])
                angle2 = cast(Angle, objs[1])
                an0 = angle1.angle if angle1.turn == "Counterclockwise" else 2 * np.pi - angle1.angle
                an1 = angle2.angle if angle2.turn == "Counterclockwise" else 2 * np.pi - angle2.angle
                self.angle = (an0 + an1) % (2 * np.pi)
                self.turn = "Counterclockwise"

            case "SubAA":
                angle1 = cast(Angle, objs[0])
                angle2 = cast(Angle, objs[1])
                an0 = angle1.angle if angle1.turn == "Counterclockwise" else 2 * np.pi - angle1.angle
                an1 = angle2.angle if angle2.turn == "Counterclockwise" else 2 * np.pi - angle2.angle
                self.angle = (an0 - an1) % (2 * np.pi)
                self.turn = "Counterclockwise"

            case "MulNA":
                factor = cast(Number, objs[0])
                angle = cast(Angle, objs[1])
                self.angle = (factor * angle.angle) % (2 * np.pi)
                self.turn = angle.turn

            case _:
                raise NotImplementedError(f"Invalid constructing method: {self.construct_type}")
            