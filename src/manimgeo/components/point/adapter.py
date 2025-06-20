from __future__ import annotations

from ...utils.mathe import GeoMathe
from pydantic import Field
from typing import cast
import numpy as np

# 基类与参数模型
from ..base import GeometryAdapter
from .construct import *

class PointAdapter(GeometryAdapter[PointConstructArgs]):
    coord: np.ndarray = Field(default_factory=lambda: np.zeros(2), description="计算点坐标", init=False)
    
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
                self.coord = GeoMathe.axisymmetric_point(args.point.coord, args.line.start, args.line.end)

            case "VerticalPL":
                args = cast(VerticalPLArgs, self.args)
                self.coord = GeoMathe.vertical_point_to_line(args.point.coord, args.line.start, args.line.end)

            case "ParallelPL":
                args = cast(ParallelPLArgs, self.args)
                self.coord = args.point.coord + args.distance * args.line.unit_direction

            case "InversionPCir":
                args = cast(InversionPCirArgs, self.args)
                self.coord = GeoMathe.inversion_point(args.point.coord, args.circle.center, args.circle.radius)

            case "IntersectionLL":
                args = cast(IntersectionLLArgs, self.args)
                result = GeoMathe.intersection_line_line(
                    args.line1.start, args.line1.end,
                    args.line2.start, args.line2.end,
                    type(args.line1).__name__, type(args.line2).__name__, # type: ignore
                    args.regard_infinite
                )
                if result[0] and result[1] is not None:
                    self.coord = result[1]
                elif result[0] and result[1] is None:
                    raise ValueError("Infinites intersections")
                else:
                    raise ValueError("No intersections")
                
            case "TranslationPV":
                args = cast(TranslationPVArgs, self.args)
                self.coord = args.point.coord + args.vector.vec

            case "CentroidPPP":
                args = cast(CentroidPPPArgs, self.args)
                self.coord = (args.point1.coord + args.point2.coord + args.point3.coord) / 3

            case "CircumcenterPPP":
                args = cast(CircumcenterPPPArgs, self.args)
                _, self.coord = GeoMathe.circumcenter_r_c(
                    args.point1.coord, args.point2.coord, args.point3.coord
                )

            case "IncenterPPP":
                args = cast(IncenterPPPArgs, self.args)
                _, self.coord = GeoMathe.inscribed_r_c(
                    args.point1.coord, args.point2.coord, args.point3.coord
                )

            case "OrthocenterPPP":
                args = cast(OrthocenterPPPArgs, self.args)
                self.coord = GeoMathe.orthocenter(
                    args.point1.coord, args.point2.coord, args.point3.coord
                )

            case "Cir":
                args = cast(CirArgs, self.args)
                self.coord = args.circle.center

            case "RotatePPA":
                args = cast(RotatePPAArgs, self.args)
                angle_num = args.angle.angle if args.angle.turn == 'Counterclockwise' else (2 * np.pi - args.angle.angle) # type: ignore
                self.coord = GeoMathe.angle_3p_countclockwise(args.point.coord, args.center.coord, angle_num) # type: ignore

            case _:
                raise NotImplementedError(f"Invalid construct type: {self.construct_type}")
