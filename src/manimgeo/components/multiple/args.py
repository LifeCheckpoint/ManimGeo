from __future__ import annotations

from ..base import ArgsModelBase
from typing import Union, Literal, List, Callable

type Number = Union[float, int]

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

type MultipleConstructArgs = Union[
    MultipleArgs, FilteredMultipleArgs, FilteredMultipleMonoArgs
]

MultipleConstructArgsList = [
    MultipleConstructArgs, FilteredMultipleArgs, FilteredMultipleMonoArgs
]

type MultipleConstructType = Literal[
    "Multiple", "FilteredMultiple", "FilteredMultipleMono"
]