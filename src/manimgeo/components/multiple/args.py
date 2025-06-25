from __future__ import annotations

from ..base import ArgsModelBase
from typing import TYPE_CHECKING, Union, Literal, List, Callable, Container

type Number = Union[float, int]

if TYPE_CHECKING:
    from .multiple import MultipleComponents

from ..base import BaseGeometry

class MultipleArgs(ArgsModelBase):
    construct_type: Literal["Multiple"] = "Multiple"
    geometry_objects: List[BaseGeometry]

class FilteredMultipleArgs(MultipleArgs):
    """
    通过指定过滤器过滤，从而在保持依赖的同时构建新 MultipleComponents
    """
    construct_type: Literal["FilteredMultiple"] = "FilteredMultiple"
    filter_func: Callable[[List[BaseGeometry]], List[bool]]
    geometry_objects: List[BaseGeometry]

class FilteredMultipleMonoArgs(ArgsModelBase):
    """
    通过指定过滤器过滤，从而在保持依赖的同时构建新 MultipleComponents 

    不考虑多个对象的相对关系的前提下，该构造方式相较而言更快一些
    """
    construct_type: Literal["FilteredMultipleMono"] = "FilteredMultipleMono"
    filter_func: Callable[[BaseGeometry], bool]
    geometry_objects: List[BaseGeometry]

class UnionArgs(ArgsModelBase):
    """
    并集
    """
    construct_type: Literal["Union"] = "Union"
    multiples: Container[MultipleComponents]

class IntersectionArgs(ArgsModelBase):
    """
    交集
    """
    construct_type: Literal["Intersection"] = "Intersection"
    multiples: Container[MultipleComponents]

type MultipleConstructArgs = Union[
    MultipleArgs, FilteredMultipleArgs, FilteredMultipleMonoArgs,
    UnionArgs, IntersectionArgs,
]

MultipleConstructArgsList = [
    MultipleConstructArgs, FilteredMultipleArgs, FilteredMultipleMonoArgs,
    UnionArgs, IntersectionArgs,
]

type MultipleConstructType = Literal[
    "Multiple", "FilteredMultiple", "FilteredMultipleMono",
    "Union", "Intersection",
]