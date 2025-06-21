from __future__ import annotations

from ...math import (
    circumcenter,
    inscribed,
    inverse_circle,
    plane_get_ABCD, # 新增
)
from ..base import GeometryAdapter
from .construct import *
from pydantic import Field
from typing import cast
import numpy as np

class CircleAdapter(GeometryAdapter[CircleConstructArgs]):
    center: np.ndarray = Field(default=np.zeros(3), description="计算圆心坐标", init=False)
    radius: Number = Field(default=0.0, description="计算圆半径", init=False)
    normal: np.ndarray = Field(default=np.array([0.0, 0.0, 1.0]), description="计算圆所在平面的法向量", init=False) # 新增
    area: Number = Field(default=0.0, description="计算圆面积", init=False)
    circumference: Number = Field(default=0.0, description="计算圆周长", init=False)

    def __call__(self):
        """根据 self.args 执行具体计算"""

        match self.construct_type:
            case "CNR":
                args = cast(CNRArgs, self.args)
                self.center = args.center.coord.copy()
                self.radius = args.radius
                self.normal = args.normal.vec / np.linalg.norm(args.normal.vec) # 归一化

            case "PR":
                args = cast(PRArgs, self.args)
                self.center = args.center.coord.copy()
                self.radius = args.radius
                if args.normal:
                    self.normal = args.normal.vec / np.linalg.norm(args.normal.vec)
                else:
                    self.normal = np.array([0.0, 0.0, 1.0]) # 默认 XY 平面

            case "PP":
                args = cast(PPArgs, self.args)
                self.center = args.center.coord.copy()
                self.radius = np.linalg.norm(args.point.coord - args.center.coord) # type: ignore
                if args.normal:
                    self.normal = args.normal.vec / np.linalg.norm(args.normal.vec)
                else:
                    self.normal = np.array([0.0, 0.0, 1.0]) # 默认 XY 平面

            case "L":
                args = cast(LArgs, self.args)
                start = args.radius_segment.start.copy()
                end = args.radius_segment.end.copy()
                self.center = start
                self.radius = np.linalg.norm(end - start) # type: ignore
                if args.normal:
                    self.normal = args.normal.vec / np.linalg.norm(args.normal.vec)
                else:
                    self.normal = np.array([0.0, 0.0, 1.0]) # 默认 XY 平面

            case "PPP":
                args = cast(PPPArgs, self.args)
                self.radius, self.center = circumcenter(
                    args.point1.coord, args.point2.coord, args.point3.coord
                )
                A, B, C = plane_get_ABCD(args.point1.coord, args.point2.coord, args.point3.coord)
                normal_vec = np.array([A, B, C])
                self.normal = normal_vec / np.linalg.norm(normal_vec) # 归一化

            case "TranslationCirV":
                args = cast(TranslationCirVArgs, self.args)
                self.center = args.circle.center + args.vector.vec
                self.radius = args.circle.radius
                self.normal = args.circle.normal # 继承原圆法向量

            case "InverseCirCir":
                args = cast(InverseCirCirArgs, self.args)
                self.center, self.radius, self.normal = inverse_circle( # 修改
                    args.circle.center, args.circle.radius, args.circle.normal, # 修改
                    args.base_circle.center, args.base_circle.radius, args.base_circle.normal # 修改
                )

            case "InscribePPP":
                args = cast(InscribePPPArgs, self.args)
                self.radius, self.center = inscribed(args.point1.coord, args.point2.coord, args.point3.coord)
                A, B, C = plane_get_ABCD(args.point1.coord, args.point2.coord, args.point3.coord)
                normal_vec = np.array([A, B, C])
                self.normal = normal_vec / np.linalg.norm(normal_vec) # 归一化

            case _:
                raise NotImplementedError(f"Invalid constructing method: {self.construct_type}")

        self.area = np.pi * self.radius ** 2
        self.circumference = 2 * np.pi * self.radius
