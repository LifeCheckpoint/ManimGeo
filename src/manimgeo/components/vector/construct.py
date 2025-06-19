from typing import Union, Literal

VectorConstructType = Literal[
    "PP", "L", "N", "NPP", "NNormDirection",
    "AddVV", "SubVV", "MulNV"
]
Number = Union[int, float]