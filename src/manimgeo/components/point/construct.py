from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING, Union, Literal
import numpy as np

type Number = Union[float, int]

if TYPE_CHECKING:
    from ..angle import Angle
    from ..circle import Circle
    from ..line import Line, LineSegment
    from ..vector import Vector
    from .point import Point

class FreeArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    construct_type: Literal["Free"] = "Free"
    coord: np.ndarray

class ConstraintArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    construct_type: Literal["Constraint"] = "Constraint"
    coord: np.ndarray

class MidPPArgs(BaseModel):
    construct_type: Literal["MidPP"] = "MidPP"
    point1: Point
    point2: Point

class MidLArgs(BaseModel):
    construct_type: Literal["MidL"] = "MidL"
    line: LineSegment

class ExtensionPPArgs(BaseModel):
    construct_type: Literal["ExtensionPP"] = "ExtensionPP"
    start: Point
    through: Point
    factor: Number

class AxisymmetricPLArgs(BaseModel):
    construct_type: Literal["AxisymmetricPL"] = "AxisymmetricPL"
    point: Point
    line: Line

class VerticalPLArgs(BaseModel):
    construct_type: Literal["VerticalPL"] = "VerticalPL"
    point: Point
    line: Line

class ParallelPLArgs(BaseModel):
    construct_type: Literal["ParallelPL"] = "ParallelPL"
    point: Point
    line: Line
    distance: Number

class InversionPCirArgs(BaseModel):
    construct_type: Literal["InversionPCir"] = "InversionPCir"
    point: Point
    circle: Circle

class IntersectionLLArgs(BaseModel):
    construct_type: Literal["IntersectionLL"] = "IntersectionLL"
    line1: Line
    line2: Line
    regard_infinite: bool = False

class TranslationPVArgs(BaseModel):
    construct_type: Literal["TranslationPV"] = "TranslationPV"
    point: Point
    vector: Vector

class CentroidPPPArgs(BaseModel):
    construct_type: Literal["CentroidPPP"] = "CentroidPPP"
    point1: Point
    point2: Point
    point3: Point

class CircumcenterPPPArgs(BaseModel):
    construct_type: Literal["CircumcenterPPP"] = "CircumcenterPPP"
    point1: Point
    point2: Point
    point3: Point

class IncenterPPPArgs(BaseModel):
    construct_type: Literal["IncenterPPP"] = "IncenterPPP"
    point1: Point
    point2: Point
    point3: Point

class OrthocenterPPPArgs(BaseModel):
    construct_type: Literal["OrthocenterPPP"] = "OrthocenterPPP"
    point1: Point
    point2: Point
    point3: Point

class CirArgs(BaseModel):
    construct_type: Literal["Cir"] = "Cir"
    circle: Circle

class RotatePPAArgs(BaseModel):
    construct_type: Literal["RotatePPA"] = "RotatePPA"
    point: Point
    center: Point
    angle: Angle
    axis: np.ndarray | None = None

# 所有参数模型的联合类型

type PointConstructArgs = Union[
    FreeArgs, ConstraintArgs, MidPPArgs, MidLArgs, ExtensionPPArgs,
    AxisymmetricPLArgs, VerticalPLArgs, ParallelPLArgs, InversionPCirArgs,
    IntersectionLLArgs, TranslationPVArgs, CentroidPPPArgs, CircumcenterPPPArgs,
    IncenterPPPArgs, OrthocenterPPPArgs, CirArgs, RotatePPAArgs
]

PointConstructArgsList = [
    FreeArgs, ConstraintArgs, MidPPArgs, MidLArgs, ExtensionPPArgs,
    AxisymmetricPLArgs, VerticalPLArgs, ParallelPLArgs, InversionPCirArgs,
    IntersectionLLArgs, TranslationPVArgs, CentroidPPPArgs, CircumcenterPPPArgs,
    IncenterPPPArgs, OrthocenterPPPArgs, CirArgs, RotatePPAArgs
]

type PointConstructType = Literal[
    "Free", "Constraint", "MidPP", "MidL", "ExtensionPP",
    "AxisymmetricPL", "VerticalPL", "ParallelPL", "InversionPCir",
    "IntersectionLL", "TranslationPV", "CentroidPPP", "CircumcenterPPP",
    "IncenterPPP", "OrthocenterPPP", "Cir", "RotatePPA"
]