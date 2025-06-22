from __future__ import annotations

from ..base import ArgsModelBase
from typing import TYPE_CHECKING, Union, Literal, List
from typing_extensions import deprecated
import numpy as np

type Number = Union[float, int]

from .intersections import ConcreteIntType
from ..base import BaseGeometry

if TYPE_CHECKING:
    from ..angle import Angle
    from ..circle import Circle
    from ..line import Line, LineSegment
    from ..vector import Vector
    from .point import Point

class FreeArgs(ArgsModelBase):
    construct_type: Literal["Free"] = "Free"
    coord: np.ndarray

class ConstraintArgs(ArgsModelBase):
    construct_type: Literal["Constraint"] = "Constraint"
    coord: np.ndarray

class MidPPArgs(ArgsModelBase):
    construct_type: Literal["MidPP"] = "MidPP"
    point1: Point
    point2: Point

class MidLArgs(ArgsModelBase):
    construct_type: Literal["MidL"] = "MidL"
    line: LineSegment

class ExtensionPPArgs(ArgsModelBase):
    construct_type: Literal["ExtensionPP"] = "ExtensionPP"
    start: Point
    through: Point
    factor: Number

class AxisymmetricPLArgs(ArgsModelBase):
    construct_type: Literal["AxisymmetricPL"] = "AxisymmetricPL"
    point: Point
    line: Line

class VerticalPLArgs(ArgsModelBase):
    construct_type: Literal["VerticalPL"] = "VerticalPL"
    point: Point
    line: Line

class ParallelPLArgs(ArgsModelBase):
    construct_type: Literal["ParallelPL"] = "ParallelPL"
    point: Point
    line: Line
    distance: Number

class InversionPCirArgs(ArgsModelBase):
    construct_type: Literal["InversionPCir"] = "InversionPCir"
    point: Point
    circle: Circle

@deprecated("求交点由通用参数模型 IntersectionsArgs 接管")
class IntersectionLLArgs(ArgsModelBase):
    construct_type: Literal["IntersectionLL"] = "IntersectionLL"
    line1: Line
    line2: Line
    regard_infinite: bool = False

class IntersectionsArgs(ArgsModelBase):
    construct_type: Literal["Intersections"] = "Intersections"
    int_type: ConcreteIntType

    def _get_deps(self):
        """
        交点参数模型的依赖对象来源于 int_type
        """
        dep_objects: List[BaseGeometry] = []
        for field_name, field_info in self.int_type.__class__.model_fields.items():
            field_value = getattr(self.int_type, field_name)
            if isinstance(field_value, BaseGeometry):
                dep_objects.append(field_value)

        return dep_objects

class TranslationPVArgs(ArgsModelBase):
    construct_type: Literal["TranslationPV"] = "TranslationPV"
    point: Point
    vector: Vector

class CentroidPPPArgs(ArgsModelBase):
    construct_type: Literal["CentroidPPP"] = "CentroidPPP"
    point1: Point
    point2: Point
    point3: Point

class CircumcenterPPPArgs(ArgsModelBase):
    construct_type: Literal["CircumcenterPPP"] = "CircumcenterPPP"
    point1: Point
    point2: Point
    point3: Point

class IncenterPPPArgs(ArgsModelBase):
    construct_type: Literal["IncenterPPP"] = "IncenterPPP"
    point1: Point
    point2: Point
    point3: Point

class OrthocenterPPPArgs(ArgsModelBase):
    construct_type: Literal["OrthocenterPPP"] = "OrthocenterPPP"
    point1: Point
    point2: Point
    point3: Point

class CirArgs(ArgsModelBase):
    construct_type: Literal["Cir"] = "Cir"
    circle: Circle

class RotatePPAArgs(ArgsModelBase):
    construct_type: Literal["RotatePPA"] = "RotatePPA"
    point: Point
    center: Point
    angle: Angle
    axis: np.ndarray | None = None

# 所有参数模型的联合类型

type PointConstructArgs = Union[
    FreeArgs, ConstraintArgs, MidPPArgs, MidLArgs, ExtensionPPArgs,
    AxisymmetricPLArgs, VerticalPLArgs, ParallelPLArgs, InversionPCirArgs,
    IntersectionLLArgs, IntersectionsArgs, TranslationPVArgs, CentroidPPPArgs, CircumcenterPPPArgs,
    IncenterPPPArgs, OrthocenterPPPArgs, CirArgs, RotatePPAArgs
]

PointConstructArgsList = [
    FreeArgs, ConstraintArgs, MidPPArgs, MidLArgs, ExtensionPPArgs,
    AxisymmetricPLArgs, VerticalPLArgs, ParallelPLArgs, InversionPCirArgs,
    IntersectionLLArgs, IntersectionsArgs, TranslationPVArgs, CentroidPPPArgs, CircumcenterPPPArgs,
    IncenterPPPArgs, OrthocenterPPPArgs, CirArgs, RotatePPAArgs
]

type PointConstructType = Literal[
    "Free", "Constraint", "MidPP", "MidL", "ExtensionPP",
    "AxisymmetricPL", "VerticalPL", "ParallelPL", "InversionPCir",
    "IntersectionLL", "Intersections", "TranslationPV", "CentroidPPP", "CircumcenterPPP",
    "IncenterPPP", "OrthocenterPPP", "Cir", "RotatePPA"
]