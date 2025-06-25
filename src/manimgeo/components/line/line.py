from __future__ import annotations

from pydantic import Field, model_validator
from typing import TYPE_CHECKING, List, Any, TypeVar, Type
import numpy as np

from ..base import BaseGeometry
from .adapter import LineAdapter
from .args import *

if TYPE_CHECKING:
    from ..point import Point
    from ..vector import Vector

_LineT = TypeVar('_LineT', bound='Line')

class Line(BaseGeometry):
    """
    线类

    建议对 Line 的子类进行实例化，而不是直接实例化 Line
    """

    attrs: List[str] = Field(default=["start", "end", "length", "unit_direction"], description="线对象属性列表", init=False)
    start: np.ndarray = Field(default=np.zeros(2), description="线首坐标", init=False)
    end: np.ndarray = Field(default=np.zeros(2), description="线尾坐标", init=False)
    length: Number = Field(default=0.0, description="线长度", init=False)
    unit_direction: np.ndarray = Field(default=np.zeros(2), description="线单位方向向量", init=False)

    args: LineConstructArgs = Field(discriminator='construct_type', description="线构造参数")
    adapter: LineAdapter = Field(init=False) # adapter 初始化将在 model_post_init 中进行

    @model_validator(mode='before')
    @classmethod
    def set_adapter_before_validation(cls, data: Any) -> Any:
        """在验证前设置 adapter 字段"""
        if isinstance(data, dict) and 'args' in data:
            # 假设 args 已经是 Pydantic 模型或可以被 LineAdapter 接受
            data['adapter'] = LineAdapter(args=data['args'])
        return data

    line_type: Literal["LineSegment", "Ray", "InfinityLine"] = Field(description="线类型，子类会尝试覆盖")

    @property
    def construct_type(self) -> LineConstructType:
        return self.args.construct_type

    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        self.adapter = LineAdapter(args=self.args)
        self.name = self.get_name(self.name)
        # 添加依赖关系
        self._extract_dependencies_from_args(self.args)
        self.update() # 首次计算

    # 构造方法
    
    @classmethod
    def TranslationLV(cls: Type[_LineT], line: LineConcrete, vec: Vector, name: str = "") -> _LineT:
        """
        平移构造线

        - `line`: 原线
        - `vec`: 平移向量
        """
        return cls(
            name=name,
            args=TranslationLVArgs(line=line, vector=vec),
        ) # type: ignore[call-arg]
    
    @classmethod
    def PP(cls: Type[_LineT], start: Point, end: Point, name: str = "") -> _LineT:
        """
        起始点构造线

        - `start`: 起点
        - `end`: 终点
        """
        return cls(
            name=name,
            args=PPArgs(point1=start, point2=end),
        ) # type: ignore[call-arg]
    
    @classmethod
    def PV(cls: Type[_LineT], start: Point, vector: Vector, name: str = "") -> _LineT:
        """
        起点方向构造线

        - `start`: 起点
        - `vector`: 方向向量
        """
        return cls(
            name=name,
            args=PVArgs(start=start, vector=vector),
        ) # type: ignore[call-arg]
    
    @classmethod
    def VerticalPL(cls: Type[_LineT], point: Point, line: LineConcrete, name: str = "") -> _LineT:
        """
        点与线构造垂直线

        - `point`: 垂线经过点
        - `line`: 原线
        """
        return cls(
            name=name,
            args=VerticalPLArgs(point=point, line=line),
        ) # type: ignore[call-arg]
    
    @classmethod
    def ParallelPL(cls: Type[_LineT], point: Point, line: LineConcrete, distance: Number = 0, name: str = "") -> _LineT:
        """
        点与线构造平行线

        - `point`: 平行线经过点
        - `line`: 原线
        - `distance`: 平行线与原线的距离，默认为 0
        """
        return cls(
            name=name,
            args=ParallelPLArgs(point=point, line=line, distance=distance),
        ) # type: ignore[call-arg]
    
class LineSegment(Line):
    line_type: Literal["LineSegment"] = "LineSegment"

class Ray(Line):
    line_type: Literal["Ray"] = "Ray"
    
class InfinityLine(Line):
    line_type: Literal["InfinityLine"] = "InfinityLine"
