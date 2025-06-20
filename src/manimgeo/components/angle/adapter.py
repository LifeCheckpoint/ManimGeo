from __future__ import annotations

from ...utils.mathe import GeoMathe
from pydantic import Field
from typing import Literal, cast
import numpy as np

from ..base import GeometryAdapter
from .construct import *

class AngleAdapter(GeometryAdapter[AngleConstructArgs]): # 继承 GeometryAdapter 并指定参数模型类型
    angle: Number = Field(default=0.0, description="计算角度", init=False)
    turn: Literal["Clockwise", "Counterclockwise"] = Field(default="Counterclockwise", description="角度计算方向", init=False)

    def __call__(self):
        """根据 self.args 执行具体计算"""

        match self.construct_type:
            case "PPP":
                args = cast(PPPArgs, self.args)
                self.angle = GeoMathe.angle_3p_countclockwise(args.start.coord, args.center.coord, args.end.coord)
                self.turn = "Counterclockwise"

            case "LL":
                args = cast(LLArgs, self.args)
                if not np.allclose(args.line1.start, args.line2.start):
                    raise ValueError("无法从起始点不等的两条线构造角")
                self.angle = GeoMathe.angle_3p_countclockwise(args.line1.end, args.line1.start, args.line2.end)
                self.turn = "Counterclockwise"

            case "LP":
                args = cast(LPArgs, self.args)
                self.angle = GeoMathe.angle_3p_countclockwise(args.line.end, args.line.start, args.point.coord)
                self.turn = "Counterclockwise"

            case "N":
                args = cast(NArgs, self.args)
                if args.turn not in ["Clockwise", "Counterclockwise"]:
                    raise ValueError("角度方向必须为 'Clockwise' 或 'Counterclockwise'")
                self.angle = args.angle
                self.turn = args.turn

            case "TurnA":
                args = cast(TurnAArgs, self.args)
                self.angle = 2 * np.pi - args.angle.angle
                self.turn = "Counterclockwise" if args.angle.turn == "Clockwise" else "Clockwise"

            case "AddAA":
                args = cast(AddAAArgs, self.args)
                an0 = args.angle1.angle if args.angle1.turn == "Counterclockwise" else 2 * np.pi - args.angle1.angle
                an1 = args.angle2.angle if args.angle2.turn == "Counterclockwise" else 2 * np.pi - args.angle2.angle
                self.angle = (an0 + an1) % (2 * np.pi)
                self.turn = "Counterclockwise"

            case "SubAA":
                args = cast(SubAAArgs, self.args)
                an0 = args.angle1.angle if args.angle1.turn == "Counterclockwise" else 2 * np.pi - args.angle1.angle
                an1 = args.angle2.angle if args.angle2.turn == "Counterclockwise" else 2 * np.pi - args.angle2.angle
                self.angle = (an0 - an1) % (2 * np.pi)
                self.turn = "Counterclockwise"

            case "MulNA":
                args = cast(MulNAArgs, self.args)
                self.angle = (args.factor * args.angle.angle) % (2 * np.pi)
                self.turn = args.angle.turn

            case _:
                raise NotImplementedError(f"Invalid constructing method: {self.construct_type}")