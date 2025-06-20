from __future__ import annotations

from pydantic import BaseModel
from typing import TYPE_CHECKING, Union, Literal

type Number = Union[float, int]

if TYPE_CHECKING:
    from ..point import Point
    from ..line import LineSegment
    from ..vector import Vector
    from .circle import Circle

class PRArgs(BaseModel):
    construct_type: Literal["PR"] = "PR"
    center: Point
    radius: Number

class PPArgs(BaseModel):
    construct_type: Literal["PP"] = "PP"
    center: Point
    point: Point

class LArgs(BaseModel):
    construct_type: Literal["L"] = "L"
    radius_segment: LineSegment

class PPPArgs(BaseModel):
    construct_type: Literal["PPP"] = "PPP"
    point1: Point
    point2: Point
    point3: Point

class TranslationCirVArgs(BaseModel):
    construct_type: Literal["TranslationCirV"] = "TranslationCirV"
    circle: Circle
    vector: Vector

class InverseCirCirArgs(BaseModel):
    construct_type: Literal["InverseCirCir"] = "InverseCirCir"
    circle: Circle
    base_circle: Circle

class InscribePPPArgs(BaseModel):
    construct_type: Literal["InscribePPP"] = "InscribePPP"
    point1: Point
    point2: Point
    point3: Point

# 所有参数模型的联合类型
type CircleConstructArgs = Union[
    PRArgs, PPArgs, LArgs, PPPArgs, TranslationCirVArgs,
    InverseCirCirArgs, InscribePPPArgs
]

type CircleConstructType = Literal[
    "PR", "PP", "L", "PPP", "TranslationCirV",
    "InverseCirCir", "InscribePPP"
]