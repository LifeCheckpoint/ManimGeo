from manimgeo.components.base import ParamLike, LineLike, PointLike
from typing import Union

import numpy as np

class VectorParam(ParamLike):
    """向量参数"""
    _vector: np.ndarray

    @property
    def vector(self) -> np.ndarray:
        """向量"""
        return self._vector
    
    @vector.setter
    def vector(self, value: np.ndarray, name: str = ""):
        super().__init__(name if name is not "" else f"Vector@{id(self)}")
        self.update()
        self._vector = value

    def _recalculate(self):
        # 定值向量本身不受参数影响，只需要更新依赖
        pass