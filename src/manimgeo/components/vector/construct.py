from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING, Union, Literal
import numpy as np

type Number = Union[float, int]

if TYPE_CHECKING:
    from ..point import Point
    from ..line import LineSegment
    from .vector import Vector

class PPArgs(BaseModel):
    construct_type: Literal["PP"] = "PP"
    start: Point
    end: Point

class LArgs(BaseModel):
    construct_type: Literal["L"] = "L"
    line: LineSegment

class NArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    construct_type: Literal["N"] = "N"
    vec: np.ndarray

class NPPArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    construct_type: Literal["NPP"] = "NPP"
    start: np.ndarray
    end: np.ndarray

class NNormDirectionArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    construct_type: Literal["NNormDirection"] = "NNormDirection"
    norm: Number
    direction: np.ndarray

class AddVVArgs(BaseModel):
    construct_type: Literal["AddVV"] = "AddVV"
    vec1: Vector
    vec2: Vector

class SubVVArgs(BaseModel):
    construct_type: Literal["SubVV"] = "SubVV"
    vec1: Vector
    vec2: Vector

class MulNVArgs(BaseModel):
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