from __future__ import annotations

from ..base import ArgsModelBase
from typing import Union, Literal, List

type Number = Union[float, int]

from ..base import BaseGeometry

class MultipleArgs(ArgsModelBase):
    construct_type: Literal["Multiple"] = "Multiple"
    geometry_objects: List[BaseGeometry]

type MultipleConstructArgs = MultipleArgs

MultipleConstructArgsList = [MultipleConstructArgs]

type MultipleConstructType = Literal["Multiple"]