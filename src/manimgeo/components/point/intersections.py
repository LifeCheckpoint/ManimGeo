from __future__ import annotations

import numpy as np
from pydantic import Field, ConfigDict
from ..base import BaseModelN
from typing import TYPE_CHECKING, Union, List, Callable, cast
from ...math import (
    intersection_line_line,
)

if TYPE_CHECKING:
    from ..base import BaseGeometry
    from ..line import LineSegment, Ray, InfinityLine
    from ..circle import Circle
    from .point import Point
    type ConcreteLine = Union[LineSegment, Ray, InfinityLine]

# Type of intersections
class IntType:
    class LL(BaseModelN):
        line1: ConcreteLine
        line2: ConcreteLine
        as_infinity: bool

    class LCir(BaseModelN):
        line: ConcreteLine
        circle: Circle
        as_infinity: bool

    class CirCir(BaseModelN):
        circle1: Circle
        circle2: Circle

    type ConcreteIntType = Union[LL, LCir, CirCir]

# Result of calculation
def always_true(point: np.ndarray) -> bool: return True
class IntResults(BaseModelN):
    int_type: IntType.ConcreteIntType
    num_results: int
    result_points: List[np.ndarray]
    filter: Callable[[np.ndarray], bool] = Field(default=always_true)

    def filt(self, filter: Callable[[np.ndarray], bool]) -> IntResults:
        """
        根据给定的过滤函数筛选结果点

        - `filter`: 一个函数，接受一个 Point 对象并返回布尔值，表示该点是否满足条件

        Returns: 新结果对象
        """
        filtered_points = [p for p in self.result_points if filter(p)]
        return IntResults(
            int_type=self.int_type,
            num_results=len(filtered_points),
            result_points=filtered_points,
            filter=filter    
        )

# Calculation
class PointIntersections(BaseModelN):
    int_type: IntType.ConcreteIntType

    def __call__(self) -> IntResults:
        """
        计算交点
        """

        match self.int_type.__class__:
            case IntType.LL:
                self.int_type = cast(IntType.LL, self.int_type)
                result = intersection_line_line(
                    self.int_type.line1.start, self.int_type.line1.end,
                    self.int_type.line2.start, self.int_type.line2.end,
                    self.int_type.line1.line_type, self.int_type.line2.line_type,
                    as_infinty=self.int_type.as_infinity
                )

                if result is None:
                    return IntResults(
                        int_type=self.int_type,
                        num_results=0,
                        result_points=[]
                    )
                else:
                    return IntResults(
                        int_type=self.int_type,
                        num_results=1,
                        result_points=[result],
                    )

            case IntType.LCir:
                # TODO
                raise NotImplementedError
            
            case IntType.CirCir:
                # TODO
                raise NotImplementedError
            
            case _:
                raise ValueError(f"未知的交点类型: {self.int_type.__class__}")
