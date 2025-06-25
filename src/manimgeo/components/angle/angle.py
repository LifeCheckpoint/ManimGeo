from __future__ import annotations

from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Literal, List, Any

from ..base import BaseGeometry
from .adapter import AngleAdapter
from .args import *

if TYPE_CHECKING:
    from ..point.point import Point
    from ..line.line import Line, LineSegment

class Angle(BaseGeometry):
    attrs: List[str] = Field(default=["angle", "turn"], description="角属性列表", init=False)
    angle: Number = Field(default=0.0, description="角度大小", init=False)
    turn: Literal["Clockwise", "Counterclockwise"] = Field(default="Counterclockwise", description="角方向", init=False)
    args: AngleConstructArgs = Field(discriminator='construct_type', description="角构造参数")

    @model_validator(mode='before')
    @classmethod
    def set_adapter_before_validation(cls, data: Any) -> Any:
        """在验证前设置 adapter 字段"""
        if isinstance(data, dict) and 'args' in data:
            # 假设 args 已经是 Pydantic 模型或可以被 AngleAdapter 接受
            data['adapter'] = AngleAdapter(args=data['args'])
        return data

    @property
    def construct_type(self) -> AngleConstructType:
        return self.args.construct_type

    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        self.adapter = AngleAdapter(args=self.args)
        self.name = self.get_name(self.name)
        # 添加依赖关系
        self._extract_dependencies_from_args(self.args)
        self.update() # 首次计算

    def __add__(self, other: Angle):
        return Angle(
            name=f"{self.name} + {other.name}",
            args=AddAAArgs(angle1=self, angle2=other)
        )

    def __sub__(self, other: Angle):
        return Angle(
            name=f"{self.name} - {other.name}",
            args=SubAAArgs(angle1=self, angle2=other)
        )

    def __mul__(self, other: Number):
        return Angle(
            name=f"{self.name} * {other}",
            args=MulNAArgs(factor=other, angle=self)
        )

    # 构造方法

    @classmethod
    def PPP(cls, start: Point, center: Point, end: Point, name: str = ""):
        """
        通过三点构造角

        - `start`: 角的起始点
        - `center`: 角的中心点
        - `end`: 角的终止点
        """
        return Angle(
            name=name,
            args=PPPArgs(start=start, center=center, end=end)
        )

    @classmethod
    def LL(cls, line1: Line, line2: Line, name: str = ""):
        """
        通过两条线构造角

        - `line1`: 角的一边
        - `line2`: 角的另一边
        """
        return Angle(
            name=name,
            args=LLArgs(line1=line1, line2=line2)
        )

    @classmethod
    def LP(cls, line: LineSegment, point: Point, name: str = ""):
        """
        通过一线一点构造角

        - `line`: 角的始边
        - `point`: 角的另一端点
        """
        return Angle(
            name=name,
            args=LPArgs(line=line, point=point)
        )

    @classmethod
    def N(cls, angle: Number, turn: Literal["Clockwise", "Counterclockwise"] = "Counterclockwise", name: str = ""):
        """
        通过角度构造角

        - `angle`: 角度
        - `turn`: 角的转向
        """
        return Angle(
            name=name,
            args=NArgs(angle=angle, turn=turn)
        )

    @classmethod
    def TurnA(cls, angle: Angle, name: str = ""):
        """
        反转角旋转方向构造角

        注意，反转角实质上表示同一个角，但是方向相反，角度取 2π - 原角度

        - `angle`: 角
        """
        return Angle(
            name=name,
            args=TurnAArgs(angle=angle)
        )
    