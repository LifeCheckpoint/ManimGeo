from __future__ import annotations

from ...utils.mathe import GeoMathe
from ...utils.utils import GeoUtils
from ..base import GeometryAdapter, BaseGeometry
from .construct import VectorConstructType, Number
from pydantic import Field
from typing import TYPE_CHECKING, Union, Any, List, cast
import numpy as np

if TYPE_CHECKING:
    from ..point.point import Point
    from ..line.line import LineSegment

class VectorAdapter(GeometryAdapter):
    vec: np.ndarray = Field(default=np.zeros(2), description="计算向量坐标", init=False)
    norm: Number = Field(default=0.0, description="计算向量模长", init=False)
    unit_direction: np.ndarray = Field(default=np.zeros(2), description="计算向量单位方向", init=False)

    construct_type: VectorConstructType = Field(description="向量计算方式")
    objs: List[Union[BaseGeometry, Any]] = Field(description="向量适配器依赖的其他对象列表")

    def __call__(self, *objs: Union[BaseGeometry, Any]):
        from ..point.point import Point
        from ..line.line import LineSegment
        from .vector import Vector

        op_type_map = {
            "PP": [Point, Point],
            "L": [LineSegment],
            "N": [np.ndarray],
            "NPP": [np.ndarray, np.ndarray],
            "NNormDirection": [Number, np.ndarray],
            "AddVV": [Vector, Vector],
            "SubVV": [Vector, Vector],
            "MulNV": [Number, Vector]
        }
        GeoUtils.check_params_batch(op_type_map, self.construct_type, objs)
        
        match self.construct_type:
            case "PP":
                start = cast(Point, objs[0])
                end = cast(Point, objs[1])
                self.vec = end.coord - start.coord
            
            case "L":
                line = cast(LineSegment, objs[0])
                self.vec = line.end - line.end

            case "N":
                self.vec = cast(np.ndarray, objs[0]).copy()

            case "NPP":
                array1 = cast(np.ndarray, objs[0])
                array2 = cast(np.ndarray, objs[1])
                self.vec = array2 - array1

            case "NNormDirection":
                length = cast(Number, objs[0])
                direction = cast(np.ndarray, objs[1])
                self.vec = length * GeoMathe.unit_direction_vector(np.zeros_like(direction), direction)

            case "AddVV":
                vec1 = cast(Vector, objs[0])
                vec2 = cast(Vector, objs[1])
                self.vec = vec1.vec + vec2.vec

            case "SubVV":
                vec1 = cast(Vector, objs[0])
                vec2 = cast(Vector, objs[1])
                self.vec = vec1.vec - vec2.vec

            case "MulNV":
                factor = cast(Number, objs[0])
                vec = cast(Vector, objs[1])
                self.vec = factor * vec.vec

            case _:
                raise NotImplementedError(f"Invalid constructing method: {self.construct_type}")
            
        self.norm = float(np.linalg.norm(self.vec))
        self.unit_direction = self.vec / self.norm

