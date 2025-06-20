from __future__ import annotations

from ...utils.mathe import GeoMathe
from pydantic import Field
from typing import cast
import numpy as np

from ..base import GeometryAdapter
from .construct import *

class VectorAdapter(GeometryAdapter[VectorConstructArgs]): # 继承 GeometryAdapter 并指定参数模型类型
    vec: np.ndarray = Field(default=np.zeros(2), description="计算向量坐标", init=False)
    norm: Number = Field(default=0.0, description="计算向量模长", init=False)
    unit_direction: np.ndarray = Field(default=np.zeros(2), description="计算向量单位方向", init=False)

    def __call__(self):
        """根据 self.args 执行具体计算"""

        match self.construct_type:
            case "PP":
                args = cast(PPArgs, self.args)
                self.vec = args.end.coord - args.start.coord

            case "L":
                args = cast(LArgs, self.args)
                self.vec = args.line.end - args.line.start

            case "N":
                args = cast(NArgs, self.args)
                self.vec = args.vec.copy()

            case "NPP":
                args = cast(NPPArgs, self.args)
                self.vec = args.end - args.start

            case "NNormDirection":
                args = cast(NNormDirectionArgs, self.args)
                self.vec = args.norm * GeoMathe.unit_direction_vector(np.zeros_like(args.direction), args.direction)

            case "AddVV":
                args = cast(AddVVArgs, self.args)
                self.vec = args.vec1.vec + args.vec2.vec

            case "SubVV":
                args = cast(SubVVArgs, self.args)
                self.vec = args.vec1.vec - args.vec2.vec

            case "MulNV":
                args = cast(MulNVArgs, self.args)
                self.vec = args.factor * args.vec.vec

            case _:
                raise NotImplementedError(f"Invalid constructing method: {self.construct_type}")

        self.norm = float(np.linalg.norm(self.vec))
        # 避免除以零
        if self.norm > 1e-9:
            self.unit_direction = self.vec / self.norm
        else:
            self.unit_direction = np.zeros(2)
