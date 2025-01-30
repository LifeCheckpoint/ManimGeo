from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING, Union, Literal
import numpy as np

from manimgeo.components.base import GeometryAdapter, BaseGeometry
from manimgeo.utils.utils import GeoUtils
from manimgeo.utils.mathe import GeoMathe

if TYPE_CHECKING:
    from manimgeo.components.point import Point
    from manimgeo.components.line import LineSegment

VectorConstructType = Literal["PP", "L", "N", "NPP", "NNormDirection"]

class VectorAdapter(GeometryAdapter):
    vec: np.array
    norm: Number
    unit_direction: np.array

    def __init__(
            self,
            construct_type: VectorConstructType,
            current_geo_obj: Union["Vector"],
            *objs: Union[BaseGeometry, any]
        ):
        """
        PP: 两点构建向量
        L: 线段构建向量
        N: （数值）构建向量
        NPP: 两点（数值）构建向量
        NNormDirection: 模长方向（数值）构建向量
        """
        super().__init__(construct_type)

        [obj.add_dependent(current_geo_obj) for obj in objs if isinstance(obj, BaseGeometry)]

    def __call__(self, *objs: Union[BaseGeometry, any]):
        from manimgeo.components.point import Point
        from manimgeo.components.line import LineSegment
        
        match self.construct_type:
            case "PP":
                GeoUtils.check_params(objs, Point, Point)
                self.vec = objs[1].coord - objs[0].coord
            
            case "L":
                GeoUtils.check_params(objs, LineSegment)
                self.vec = objs[0].end - objs[0].end

            case "N":
                GeoUtils.check_params(objs, np.ndarray)
                self.vec = objs[0].copy()

            case "NPP":
                GeoUtils.check_params(objs, np.ndarray, np.ndarray)
                self.vec = objs[1] - objs[0]

            case "NNormDirection":
                GeoUtils.check_params(objs, Number, np.ndarray)
                self.vec = objs[0] * GeoMathe.unit_direction_vector(np.zeros_like(objs[1]), objs[1])

            case _:
                raise ValueError(f"Invalid constructing method: {self.construct_type}")
            
        self.norm = np.linalg.norm(self.vec)
        self.unit_direction = self.vec / self.norm

class Vector(BaseGeometry):
    attrs = ["vec", "norm", "unit_direction"]
    vec: np.array
    norm: Number
    unit_direction: np.array

    def __init__(self, construct_type: VectorConstructType, *objs, name: str = ""):
        """通过指定构造方式与对象构造向量"""
        super().__init__(GeoUtils.get_name(name, self, construct_type))
        self.objs = objs
        self.adapter = VectorAdapter(construct_type, self, *objs)
        self.update()

# Construction Methods

def VectorPP(start: Point, end: Point, name: str = ""):
    """
    ## 通过两点构造向量

    `start`: 起点
    `end`: 终点
    """
    return Vector("PP", start, end, name=name)

def VectorL(line: LineSegment, name: str = ""):
    """
    ## 通过线段构造向量

    `line`: 线段
    """
    return Vector("L", line, name=name)

def VectorN(vec: np.ndarray, name: str = ""):
    """
    ## （数值）构造向量

    `vec`: 向量数值
    """
    return Vector("N", vec, name=name)

def VectorNPP(start: np.ndarray, end: np.ndarray, name: str = ""):
    """
    ## 通过两点（数值）构造向量

    `start`: 起点
    `end`: 终点
    """
    return Vector("NPP", start, end, name=name)

def VectorNNormDirection(norm: Number, direction: np.ndarray, name: str = ""):
    """
    ## 通过模长与方向构造向量

    `norm`: 模长
    `direction`: 方向
    """
    return Vector("NNormDirection", norm, direction, name=name)