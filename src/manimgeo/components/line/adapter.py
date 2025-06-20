from __future__ import annotations

from ...math import (
    close,
    is_point_on_line,
    vertical_point_to_line,
    vertical_line_unit_direction,
)
from pydantic import Field
from typing import cast
import numpy as np

from ..base import GeometryAdapter
from .construct import *

class LineAdapter(GeometryAdapter[LineConstructArgs]): # 继承 GeometryAdapter 并指定参数模型类型
    start: np.ndarray = Field(default=np.zeros(2), description="计算线首坐标", init=False)
    end: np.ndarray = Field(default=np.zeros(2), description="计算线尾坐标", init=False)
    length: Number = Field(default=0.0, description="计算线长度", init=False)

    unit_direction: np.ndarray = Field(default=np.zeros(2), description="计算线单位方向向量", init=False)

    def __call__(self):
        """根据 self.args 执行具体计算"""

        match self.construct_type:
            case "PP":
                args = cast(PPArgs, self.args)
                self.start = args.point1.coord
                self.end = args.point2.coord

            case "PV":
                args = cast(PVArgs, self.args)
                self.start = args.start.coord
                self.end = args.start.coord + args.vector.vec

            case "TranslationLV":
                args = cast(TranslationLVArgs, self.args)
                self.start = args.line.start + args.vector.vec
                self.end = args.line.end + args.vector.vec

            case "VerticalPL":
                args = cast(VerticalPLArgs, self.args)
                if not is_point_on_line(args.point.coord, args.line.start, args.line.end):
                    self.start = vertical_point_to_line(args.point.coord, args.line.start, args.line.end)
                    self.end = args.point.coord
                else:
                    direction = vertical_line_unit_direction(args.line.start, args.line.end)
                    self.start = args.point.coord
                    self.end = self.start + direction

            case "ParallelPL":
                args = cast(ParallelPLArgs, self.args)
                self.start = args.point.coord
                self.end = args.point.coord + (args.line.end - args.line.start) # 这里的计算可能需要根据 distance 调整

            # 暂时忽略注释掉的多线构造方式
            # case "TangentsCirP":
            #     args = cast(TangentsCirPArgs, self.args)
            #     # ... 计算逻辑 ...
            #     pass # Placeholder

            # case "TangentsOutCirCir":
            #     args = cast(TangentsOutCirCirArgs, self.args)
            #     # ... 计算逻辑 ...
            #     pass # Placeholder

            # case "TangentsInCirCir":
            #     args = cast(TangentsInCirCirArgs, self.args)
            #     # ... 计算逻辑 ...
            #     pass # Placeholder

            case _:
                raise NotImplementedError(f"不支持的直线构造方法: {self.construct_type}")

        self.length = float(np.linalg.norm(self.end - self.start))
        if not close(self.length, 0):
            self.unit_direction = (self.end - self.start) / self.length
        else:
            self.unit_direction = np.zeros(2)