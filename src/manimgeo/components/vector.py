from manimgeo.components.base import ParamLike, LineLike, PointLike, BaseGeometry
from typing import Union, TypeVar
from abc import ABC
import types

import numpy as np

class VectorLike(BaseGeometry, ABC):
    """向量"""
    _vector: np.ndarray

    def __init__(self, vector: np.ndarray, name: str = ""):
        super().__init__(name if name is not "" else f"Vector@{id(self)}")
        self._vector = vector

    @property
    def vec(self) -> np.ndarray:
        """向量"""
        return self._vector
    
    @vec.setter
    def vec(self, value: np.ndarray, name: str = ""):
        super().__init__(name if name is not "" else f"VectorParam@{id(self)}")
        self.board_update_msg()
        self._vector = value

    def _recalculate(self):
        ...

class VectorParam(VectorLike):
    """定值向量参数"""
    _vector: np.ndarray

    

    def __init__(self, vector: np.ndarray, name: str = ""):
        super().__init__(name if name is not "" else f"VectorParam@{id(self)}")
        self._vector = vector

    def _recalculate(self):
        # 定值向量本身不受参数影响，只需要更新依赖
        pass

from manimgeo.components.lines import LineSegmentPP
class VectorPP(VectorLike):
    """向量（两点）"""

    @property
    def vector(self) -> np.ndarray:
        """向量"""
        return self.end.coord - self.start.coord

    def __init__(self, start: PointLike, end: PointLike, name: str = ""):
        super().__init__(start, end, name if name is not "" else f"VectorPP@{id(self)}")

    def _recalculate(self):
        pass

from manimgeo.components.points import ConstraintPoint
from manimgeo.components.lines import LineSegmentPP, RayPP, InfinityLinePP
def TransposeByVec(obj: BaseGeometry, vector: Union[VectorParam, VectorPP], name: str = "") -> BaseGeometry:
    """对任意几何对象的平移"""
    name = name if name is not "" else f"Transpose_{obj.name}"
    if isinstance(obj, PointLike):
        transpose_obj = ConstraintPoint(np.zeros(2), name)
    elif isinstance(obj, LineSegmentPP, RayPP, InfinityLinePP):
        transpose_obj = obj.__class__()

    obj.add_dependent(transpose_obj)

    # 重绑定类内更新方法
    def _recalculate(self):
        if isinstance(self, PointLike):
            self.coord

    # transpose_obj._recalculate = 
        
