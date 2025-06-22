from __future__ import annotations

from ..base import ArgsModelBase
from typing import TYPE_CHECKING, Union, Literal, Optional

type Number = Union[float, int]

if TYPE_CHECKING:
    from ..point import Point
    from ..line import LineSegment
    from ..vector import Vector
    from .circle import Circle

class CNRArgs(ArgsModelBase):
    construct_type: Literal["CNR"] = "CNR"
    center: Point
    normal: Vector
    radius: Number

class PRArgs(ArgsModelBase):
    construct_type: Literal["PR"] = "PR"
    center: Point
    radius: Number
    normal: Optional[Vector] = None

class PPArgs(ArgsModelBase):
    construct_type: Literal["PP"] = "PP"
    center: Point
    point: Point
    normal: Optional[Vector] = None

class LArgs(ArgsModelBase):
    construct_type: Literal["L"] = "L"
    radius_segment: LineSegment
    normal: Optional[Vector] = None

class PPPArgs(ArgsModelBase):
    construct_type: Literal["PPP"] = "PPP"
    point1: Point
    point2: Point
    point3: Point

class TranslationCirVArgs(ArgsModelBase):
    construct_type: Literal["TranslationCirV"] = "TranslationCirV"
    circle: Circle
    vector: Vector

class InverseCirCirArgs(ArgsModelBase):
    construct_type: Literal["InverseCirCir"] = "InverseCirCir"
    circle: Circle
    base_circle: Circle

class InscribePPPArgs(ArgsModelBase):
    construct_type: Literal["InscribePPP"] = "InscribePPP"
    point1: Point
    point2: Point
    point3: Point

# 所有参数模型的联合类型
type CircleConstructArgs = Union[
    CNRArgs, PRArgs, PPArgs, LArgs, PPPArgs, TranslationCirVArgs,
    InverseCirCirArgs, InscribePPPArgs
]

CircleConstructArgsList = [
    CNRArgs, PRArgs, PPArgs, LArgs, PPPArgs, TranslationCirVArgs,
    InverseCirCirArgs, InscribePPPArgs
]

type CircleConstructType = Literal[
    "CNR", "PR", "PP", "L", "PPP", "TranslationCirV",
    "InverseCirCir", "InscribePPP"
]