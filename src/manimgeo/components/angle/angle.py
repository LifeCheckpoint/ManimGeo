from __future__ import annotations

from ...utils.utils import GeoUtils
from ..base import BaseGeometry
from .adapter import AngleAdapter
from .construct import AngleConstructType, Number
from pydantic import Field
from typing import TYPE_CHECKING, Literal, List, Any

if TYPE_CHECKING:
    from ..point.point import Point
    from ..line.line import Line, LineSegment

class Angle(BaseGeometry):
    """
    角对象，允许如下构造：
    - `PPP`: 三点构造角
    - `LL`: 两线构造角
    - `LP`: 线与一点构造角
    - `N`: （数值）构造角
    - `TurnA`: 角方向反转构造角
    - `AddAA`: 相加构造角
    - `SubAA`: 相减构造角
    - `MulNA`: 数乘构造角
    """
    attrs: List[str] = Field(default=["angle", "turn"], description="角属性列表", init=False)
    angle: Number = Field(default=0.0, description="角度大小", init=False)
    turn: Literal["Clockwise", "Counterclockwise"] = Field(default="Counterclockwise", description="角方向", init=False)

    construct_type: AngleConstructType = Field(description="角构造方式")
    adapter: AngleAdapter = Field(description="角适配器", init=False)

    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        self.adapter = AngleAdapter(
            construct_type=self.construct_type,
            objs=self.objs,
        )
        self.name = GeoUtils.get_name(self.name, self, self.adapter.construct_type)

        # 为上游对象添加依赖关系
        for obj in self.objs:
            if isinstance(obj, BaseGeometry):
                obj.add_dependent(self)

        self.update()

    def __add__(self, other: Angle):
        return Angle(
            name=f"{self.name} + {other.name}",
            construct_type="AddAA",
            objs=[self, other]
        )
    
    def __sub__(self, other: Angle):
        return Angle(
            name=f"{self.name} - {other.name}",
            construct_type="SubAA",
            objs=[self, other]
        )
    
    def __mul__(self, other: Number):
        return Angle(
            name=f"{self.name} * {other}",
            construct_type="MulNA",
            objs=[self, other]
        )
    
    # 构造方法

    @staticmethod
    def PPP(start: Point, center: Point, end: Point, name: str = ""):
        """
        ## 通过三点构造角

        `start`: 角的起始点
        `center`: 角的中心点
        `end`: 角的终止点
        """
        return Angle(
            name=name,
            construct_type="PPP",
            objs=[start, center, end]
        )

    @staticmethod
    def LL(line1: Line, line2: Line, name: str = ""):
        """
        ## 通过两条线构造角

        `line1`: 角的一边
        `line2`: 角的另一边
        """
        return Angle(
            name=name,
            construct_type="LL",
            objs=[line1, line2]
        )
    
    @staticmethod
    def LP(line: LineSegment, point: Point, name: str = ""):
        """
        ## 通过一线一点构造角

        `line`: 角的始边
        `point`: 角的另一端点
        """
        return Angle(
            name=name,
            construct_type="LP",
            objs=[line, point]
        )
    
    @staticmethod
    def N(angle: Number, turn: Literal["Clockwise", "Counterclockwise"] = "Counterclockwise", name: str = ""):
        """
        ## 通过角度构造角

        `angle`: 角度
        `turn`: 角的转向
        """
        return Angle(
            name=name,
            construct_type="N",
            objs=[angle, turn]
        )
    
    @staticmethod
    def TurnA(angle: Angle, name: str = ""):
        """
        ## 反转角旋转方向构造角

        `angle`: 角
        """
        return Angle(
            name=name,
            construct_type="TurnA",
            objs=[angle]
        )
    