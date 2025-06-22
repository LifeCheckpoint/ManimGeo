from __future__ import annotations

from pydantic import Field
from typing import cast
import numpy as np

from ...math import (
    axisymmetric_point,
    vertical_point_to_line,
    inversion_point,
    intersection_line_line,
    circumcenter,
    inscribed,
    orthocenter,
    point_3p_countclockwise
)
from ..base import GeometryAdapter
from .construct import *

class PointAdapter(GeometryAdapter[PointConstructArgs]):
    coord: np.ndarray = Field(default_factory=lambda: np.zeros(3), description="计算点坐标", init=False)
    
    def __call__(self):
        """根据 self.args 执行具体计算"""

        match self.construct_type:
            case "Free":
                args = cast(FreeArgs, self.args)
                self.coord = args.coord

            case "Constraint":
                args = cast(ConstraintArgs, self.args)
                self.coord = args.coord

            case "MidPP":
                args = cast(MidPPArgs, self.args)
                self.coord = (args.point1.coord + args.point2.coord) / 2

            case "MidL":
                args = cast(MidLArgs, self.args)
                self.coord = (args.line.start + args.line.end) / 2

            case "ExtensionPP":
                args = cast(ExtensionPPArgs, self.args)
                self.coord = args.start.coord + args.factor * (args.through.coord - args.start.coord)

            case "AxisymmetricPL":
                args = cast(AxisymmetricPLArgs, self.args)
                self.coord = axisymmetric_point(args.point.coord, args.line.start, args.line.end)

            case "VerticalPL":
                args = cast(VerticalPLArgs, self.args)
                self.coord = vertical_point_to_line(args.point.coord, args.line.start, args.line.end)

            case "ParallelPL":
                args = cast(ParallelPLArgs, self.args)
                self.coord = args.point.coord + args.distance * args.line.unit_direction

            case "InversionPCir":
                args = cast(InversionPCirArgs, self.args)
                self.coord = inversion_point(args.point.coord, args.circle.center, args.circle.radius)

            case "IntersectionLL":
                args = cast(IntersectionLLArgs, self.args)
                result = intersection_line_line(
                    args.line1.start, args.line1.end,
                    args.line2.start, args.line2.end,
                    args.line1.line_type, args.line2.line_type,
                    args.regard_infinite
                )
                if result is None:
                    raise ValueError(f"两线无交点: {args.line1.name}, {args.line2.name}")
                else:
                    self.coord = result
                
            case "TranslationPV":
                args = cast(TranslationPVArgs, self.args)
                self.coord = args.point.coord + args.vector.vec

            case "CentroidPPP":
                args = cast(CentroidPPPArgs, self.args)
                self.coord = (args.point1.coord + args.point2.coord + args.point3.coord) / 3

            case "CircumcenterPPP":
                args = cast(CircumcenterPPPArgs, self.args)
                _, self.coord = circumcenter(
                    args.point1.coord, args.point2.coord, args.point3.coord
                )

            case "IncenterPPP":
                args = cast(IncenterPPPArgs, self.args)
                _, self.coord = inscribed(
                    args.point1.coord, args.point2.coord, args.point3.coord
                )

            case "OrthocenterPPP":
                args = cast(OrthocenterPPPArgs, self.args)
                self.coord = orthocenter(
                    args.point1.coord, args.point2.coord, args.point3.coord
                )

            case "Cir":
                args = cast(CirArgs, self.args)
                self.coord = args.circle.center

            case "RotatePPA":
                args = cast(RotatePPAArgs, self.args)
                angle_num = args.angle.angle if args.angle.turn == 'Counterclockwise' else (2 * np.pi - args.angle.angle)
                self.coord = point_3p_countclockwise(
                    args.point.coord, args.center.coord, angle_num, args.axis
                )

            case _:
                raise NotImplementedError(f"Invalid construct type: {self.construct_type}")
