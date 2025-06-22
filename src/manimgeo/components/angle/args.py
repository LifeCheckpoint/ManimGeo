from __future__ import annotations
from ..base import ArgsModelBase
from typing import TYPE_CHECKING, Union, Literal

type Number = Union[float, int]

if TYPE_CHECKING:
    from ..point import Point
    from ..line import Line, LineSegment
    from .angle import Angle

class PPPArgs(ArgsModelBase):
    construct_type: Literal["PPP"] = "PPP"
    start: Point
    center: Point
    end: Point

class LLArgs(ArgsModelBase):
    construct_type: Literal["LL"] = "LL"
    line1: Line
    line2: Line

class LPArgs(ArgsModelBase):
    construct_type: Literal["LP"] = "LP"
    line: LineSegment
    point: Point

class NArgs(ArgsModelBase):
    construct_type: Literal["N"] = "N"
    angle: Number
    turn: Literal["Clockwise", "Counterclockwise"]

class TurnAArgs(ArgsModelBase):
    construct_type: Literal["TurnA"] = "TurnA"
    angle: Angle

class AddAAArgs(ArgsModelBase):
    construct_type: Literal["AddAA"] = "AddAA"
    angle1: Angle
    angle2: Angle

class SubAAArgs(ArgsModelBase):
    construct_type: Literal["SubAA"] = "SubAA"
    angle1: Angle
    angle2: Angle

class MulNAArgs(ArgsModelBase):
    construct_type: Literal["MulNA"] = "MulNA"
    factor: Number
    angle: Angle

# 所有参数模型的联合类型
type AngleConstructArgs = Union[
    PPPArgs, LLArgs, LPArgs, NArgs,
    TurnAArgs, AddAAArgs, SubAAArgs, MulNAArgs
]

AngleConstructArgsList = [
    PPPArgs, LLArgs, LPArgs, NArgs,
    TurnAArgs, AddAAArgs, SubAAArgs, MulNAArgs
]

type AngleConstructType = Literal[
    "PPP", "LL", "LP", "N",
    "TurnA", "AddAA", "SubAA", "MulNA"
]