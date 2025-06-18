from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING, Union, Literal
import numpy as np

from ..components.base import GeometryAdapter, BaseGeometry
from ..utils.utils import GeoUtils
from ..utils.mathe import GeoMathe

if TYPE_CHECKING:
    from ..components.point import Point
    from ..components.line import Line, LineSegment

AngleConstructType = Literal[
    "PPP", "LL", "LP", "N",
    "TurnA", "AddAA", "SubAA", "MulNA"
]

class AngleAdapter(GeometryAdapter):
    angle: Number
    turn: Literal["Clockwise", "Counterclockwise"]

    def __init__(
            self,
            construct_type: AngleConstructType,
            current_geo_obj: Union["Angle"],
            *objs: Union[BaseGeometry, any]
        ):
        """
        PPP: 三点构造角
        LL: 两线构造角
        LP: 线与一点构造角
        N: （数值）构造角
        TurnA: 角方向反转构造角
        AddAA: 相加构造角
        SubAA: 相减构造角
        MulNA: 数乘构造角
        """
        super().__init__(construct_type)

        [obj.add_dependent(current_geo_obj) for obj in objs if isinstance(obj, BaseGeometry)]

    def __call__(self, *objs: Union[BaseGeometry, any]):
        from ..components.point import Point
        from ..components.line import LineSegment
        
        op_type_map = {
            "PPP": [Point, Point, Point], # start, center, end
            "LL": [Line, Line],
            "LP": [Line, Point],
            "N": [Number, str],
            "TurnA": [Angle],
            "AddAA": [Angle, Angle],
            "SubAA": [Angle, Angle],
            "MulNA": [Angle, Angle]
        }
        GeoUtils.check_params_batch(op_type_map, self.construct_type, objs)
        
        match self.construct_type:
            case "PPP":
                self.angle = GeoMathe.angle_3p_countclockwise(objs[0].coord, objs[1].coord, objs[2].coord)
                self.turn = "Counterclockwise"

            case "LL":
                if not np.allclose(objs[0].start, objs[1].start):
                    raise ValueError("Cannot generate angle from two lines without same start points")
                self.angle = GeoMathe.angle_3p_countclockwise(objs[0].end, objs[0].start, objs[1].end)
                self.turn = "Counterclockwise"

            case "LP":
                self.angle = GeoMathe.angle_3p_countclockwise(objs[0].end, objs[0].start, objs[1].coord)
                self.turn = "Counterclockwise"

            case "N":
                self.angle = objs[0]
                self.turn = objs[1]
            
            case "TurnA":
                self.angle = 2*np.pi - objs[0].angle
                self.turn = "Counterclockwise" if objs[0].turn == "Clockwise" else "Clockwise"

            case "AddAA":
                an0 = objs[0].angle if objs[0].turn == "Counterclockwise" else 2 * np.pi - objs[0].angle
                an1 = objs[1].angle if objs[1].turn == "Counterclockwise" else 2 * np.pi - objs[1].angle
                self.angle = (an0 + an1) % (2 * np.pi)
                self.turn = "Counterclockwise"

            case "SubAA":
                an0 = objs[0].angle if objs[0].turn == "Counterclockwise" else 2 * np.pi - objs[0].angle
                an1 = objs[1].angle if objs[1].turn == "Counterclockwise" else 2 * np.pi - objs[1].angle
                self.angle = (an0 - an1) % (2 * np.pi)
                self.turn = "Counterclockwise"

            case "MulNA":
                self.angle = (objs[0] * objs[1].angle) % (2 * np.pi)
                self.turn = objs[1].turn

            case _:
                raise ValueError(f"Invalid constructing method: {self.construct_type}")
            
class Angle(BaseGeometry):
    attrs = ["angle", "turn"]
    angle: Number
    turn: Literal["Clockwise", "Counterclockwise"]

    def __init__(self, construct_type: AngleConstructType, *objs, name: str = ""):
        """通过指定构造方式与对象构造线"""
        super().__init__(GeoUtils.get_name(name, self, construct_type))
        self.objs = objs
        self.adapter = AngleAdapter(construct_type, self, *objs)
        self.update()

    def __add__(self, other: Angle):
        return Angle("AddAA", self, other, name=f"{self.name} + {other.name}")
    
    def __sub__(self, other: Angle):
        return Angle("SubAA", self, other, name=f"{self.name} - {other.name}")
    
    def __mul__(self, other: Number):
        return Angle("MulNA", other, self, name=f"{other} * {self.name}")

# Constructing Methods

def AnglePPP(start: Point, center: Point, end: Point, name: str = ""):
    """
    ## 通过三点构造角

    `start`: 角的起始点
    `center`: 角的中心点
    `end`: 角的终止点
    """
    return Angle("PPP", start, center, end, name=name)

def AngleLL(line1: Line, line2: Line, name: str = ""):
    """
    ## 通过两线构造角

    `line1`: 角的一边
    `line2`: 角的另一边
    """
    return Angle("LL", line1, line2, name=name)

def AngleLP(line: Line, point: Point, name: str = ""):
    """
    ## 通过一线一点构造角

    `line`: 角的始边
    `point`: 角的另一端点
    """
    return Angle("LP", line, point, name=name)

def AngleN(angle: Number, turn: Literal["Clockwise", "Counterclockwise"] = "Counterclockwise", name: str = ""):
    """
    ## 通过角度构造角

    `angle`: 角度
    `turn`: 角的转向
    """
    return Angle("N", angle, turn, name=name)

def AngleTurnA(angle: Angle, name: str = ""):
    """
    ## 反转角旋转方向构造角

    `angle`: 角
    """
    return Angle("TurnA", angle, name=name)
