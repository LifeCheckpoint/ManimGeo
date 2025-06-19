from typing import Union, Literal

AngleConstructType = Literal[
    "PPP", "LL", "LP", "N",
    "TurnA", "AddAA", "SubAA", "MulNA"
]
Number = Union[int, float]