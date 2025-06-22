from __future__ import annotations

from pydantic import ConfigDict
from ..base import BaseModelN
from typing import TYPE_CHECKING, Union, Literal
import numpy as np

type Number = Union[float, int]

if TYPE_CHECKING:
    from ..point import Point
    from ..line import LineSegment
    from .vector import Vector

class PPArgs(BaseModelN):
    construct_type: Literal["PP"] = "PP"
    start: Point
    end: Point

class LArgs(BaseModelN):
    construct_type: Literal["L"] = "L"
    line: LineSegment

class NArgs(BaseModelN):
    construct_type: Literal["N"] = "N"
    vec: np.ndarray

class NPPArgs(BaseModelN):
    construct_type: Literal["NPP"] = "NPP"
    start: np.ndarray
    end: np.ndarray

class NNormDirectionArgs(BaseModelN):
    construct_type: Literal["NNormDirection"] = "NNormDirection"
    norm: Number
    direction: np.ndarray

class AddVVArgs(BaseModelN):
    construct_type: Literal["AddVV"] = "AddVV"
    vec1: Vector
    vec2: Vector

class SubVVArgs(BaseModelN):
    construct_type: Literal["SubVV"] = "SubVV"
    vec1: Vector
    vec2: Vector

class MulNVArgs(BaseModelN):
    construct_type: Literal["MulNV"] = "MulNV"
    factor: Number
    vec: Vector

# 所有参数模型的联合类型
type VectorConstructArgs = Union[
    PPArgs, LArgs, NArgs, NPPArgs, NNormDirectionArgs,
    AddVVArgs, SubVVArgs, MulNVArgs
]

VectorConstructArgsList = [
    PPArgs, LArgs, NArgs, NPPArgs, NNormDirectionArgs,
    AddVVArgs, SubVVArgs, MulNVArgs
]

type VectorConstructType = Literal[
    "PP", "L", "N", "NPP", "NNormDirection",
    "AddVV", "SubVV", "MulNV"
]