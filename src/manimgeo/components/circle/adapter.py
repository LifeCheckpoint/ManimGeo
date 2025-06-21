from __future__ import annotations

from ...math import (
    circumcenter_r_c,
    inscribed_r_c,
    inverse_circle,
)
from ..base import GeometryAdapter
from .construct import *
from pydantic import Field
from typing import cast
import numpy as np

class CircleAdapter(GeometryAdapter[CircleConstructArgs]):
    center: np.ndarray = Field(default=np.zeros(3), description="计算圆心坐标", init=False)
    radius: Number = Field(default=0.0, description="计算圆半径", init=False)
    area: Number = Field(default=0.0, description="计算圆面积", init=False)
    circumference: Number = Field(default=0.0, description="计算圆周长", init=False)

    def __call__(self):
        """根据 self.args 执行具体计算"""

        match self.construct_type:
            case "PR":
                args = cast(PRArgs, self.args)
                self.center = args.center.coord.copy()
                self.radius = args.radius

            case "PP":
                args = cast(PPArgs, self.args)
                self.center = args.center.coord.copy()
                self.radius = np.linalg.norm(args.point.coord - args.center.coord) # type: ignore

            case "L":
                args = cast(LArgs, self.args)
                start = args.radius_segment.start.copy()
                end = args.radius_segment.end.copy()
                self.center = start
                self.radius = np.linalg.norm(end - start) # type: ignore

            case "PPP":
                args = cast(PPPArgs, self.args)
                self.radius, self.center = circumcenter_r_c(
                    args.point1.coord, args.point2.coord, args.point3.coord
                )

            case "TranslationCirV":
                args = cast(TranslationCirVArgs, self.args)
                self.center = args.circle.center + args.vector.vec
                self.radius = args.circle.radius

            case "InverseCirCir":
                args = cast(InverseCirCirArgs, self.args)
                # TODO
                self.center, self.radius, _ = inverse_circle(
                    args.circle.center, args.circle.radius, None,
                    args.base_circle.center, args.base_circle.radius, None
                )

            case "InscribePPP":
                args = cast(InscribePPPArgs, self.args)
                self.radius, self.center = inscribed_r_c(args.point1.coord, args.point2.coord, args.point3.coord)

            case _:
                raise NotImplementedError(f"Invalid constructing method: {self.construct_type}")

        self.area = np.pi * self.radius ** 2
        self.circumference = 2 * np.pi * self.radius
