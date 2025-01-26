from manimgeo.components.base import ParamLike, LineLike, PointLike
from typing import Union

import numpy as np

class VectorParam(ParamLike):
    """定值向量参数"""
    _vector: np.ndarray

    @property
    def vector(self) -> np.ndarray:
        """向量"""
        return self._vector
    
    @vector.setter
    def vector(self, value: np.ndarray, name: str = ""):
        super().__init__(name if name is not "" else f"VectorParam@{id(self)}")
        self.update()
        self._vector = value

    def _recalculate(self):
        # 定值向量本身不受参数影响，只需要更新依赖
        pass

from manimgeo.components.lines import LineSegmentPP
class VectorPP(LineSegmentPP):
    """向量（两点）"""

    @property
    def vector(self) -> np.ndarray:
        """向量"""
        return self.end.coord - self.start.coord

    def __init__(self, start: PointLike, end: PointLike, name: str = ""):
        super().__init__(start, end, name if name is not "" else f"VectorPP@{id(self)}")

    def _recalculate(self):
        pass