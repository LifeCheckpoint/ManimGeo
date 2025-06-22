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



# 多线条

# class Lines2(BaseGeometry):
#     attrs = ["start1", "end1", "start2", "end2"]
#     start1: np.ndarray
#     end1: np.ndarray
#     start2: np.ndarray
#     end2: np.ndarray

#     line_type: str

#     def __init__(self, construct_type: LineConstructType, line_type: str, *objs, name: str = ""):
#         """通过指定构造方式与对象构造线对"""
#         super().__init__(GeoUtils.get_name(name, self, construct_type))
#         self.line_type = line_type
#         self.objs = objs
#         self.adapter = LineAdapter(construct_type, self, *objs)
#         self.update()

# class LineSegments2(Lines2):
#     def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
#         """通过指定构造方式与对象构造线段对"""
#         super().__init__(construct_type, "LineSegment", *objs, name=name)

# class Rays2(Lines2):
#     def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
#         """通过指定构造方式与对象构造射线对"""
#         super().__init__(construct_type, "Ray", *objs, name=name)

# class InfinityLines2(Lines2):
#     def __init__(self, construct_type: LineConstructType, *objs, name: str = ""):
#         """通过指定构造方式与对象构造直线对"""
#         super().__init__(construct_type, "InfinityLine", *objs, name=name)

# Constructing Methods

# def Lines2TangentsCirP(circle: Circle, point: Point, name: str = ""):
#     """
#     过一点构造圆切线

#     `circle`: 圆
#     `point`: 圆外或圆上一点
#     """
#     return InfinityLines2("TangentsCirP", circle, point, name=name)

# def Lines2TangentsOutCirCir(
#         circle1: Circle, circle2: Circle, 
#         filter: Optional[Callable[[np.ndarray, np.ndarray], bool]] = None, 
#         name: str = ""
#     ) -> Union[List[InfinityLine], InfinityLine]:
#     """
#     构造两圆外切线

#     `circle1`: 圆1
#     `circle2`: 圆2
#     `filter`: 返回线始终点须满足的条件，如果提供则返回第一个满足条件的单线对象
#     """
#     lines2 = InfinityLines2("TangentsOutCirCir", circle1, circle2, name=name)
#     if filter == None:
#         return LineOfLines2List(lines2, name=name)
#     else:
#         return LineOfLines2Fit(lines2, filter, name=name)

# def Lines2TangentsInCirCir(
#         circle1: Circle, circle2: Circle, 
#         filter: Optional[Callable[[np.ndarray, np.ndarray], bool]] = None, 
#         name: str = ""
#     ) -> Union[List[InfinityLine], InfinityLine]:
#     """
#     构造两圆内切线

#     `circle1`: 圆1
#     `circle2`: 圆2
#     `filter`: 返回线始终点须满足的条件，如果提供则返回第一个满足条件的单线对象
#     """
#     lines2 = InfinityLines2("TangentsInCirCir", circle1, circle2, name=name)
#     if filter == None:
#         return LineOfLines2List(lines2, name=name)
#     else:
#         return LineOfLines2Fit(lines2, filter, name=name)

# def LineOfLines2(lines2: Lines2, index: Literal[0, 1], name: str = "") -> Line:
#     """
#     获取两条线中的单线对象

#     `lines2`: 两线组合对象
#     `index`: 两线中的其中一线索引
#     """
#     line_map = {
#         LineSegments2: LineSegment,
#         Rays2: Ray,
#         InfinityLines2: InfinityLine
#     }
#     return line_map[lines2.__class__]("2", lines2, index, name=name)

# def LineOfLines2List(lines2: Lines2, name: str = "") -> List[Line, Line]:
#     """
#     获取两线中的单线对象列表

#     `lines2`: 两线组合对象
#     """
#     return [LineOfLines2(lines2, 0, name), LineOfLines2(lines2, 1, name)]

# def LineOfLines2Fit(lines2: Lines2, filter: Callable[[np.ndarray, np.ndarray], bool], name: str = ""):
#     """
#     获得两点中符合条件的第一个单点对象

#     `points2`: 两点组合对象
#     `filter`: 给定点坐标，返回是否符合条件
#     """
#     line_map = {
#         LineSegments2: LineSegment,
#         Rays2: Ray,
#         InfinityLines2: InfinityLine
#     }
#     return line_map[lines2.__class__]("2Filter", lines2, filter, name=name)