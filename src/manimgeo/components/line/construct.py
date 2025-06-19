from typing import Union, Literal

LineConstructType = Literal[
    "PP", "PV", "TranslationLV", "VerticalPL", "ParallelPL",
    # "TangentsCirP", "TangentsOutCirCir", "TangentsInCirCir",
]
Number = Union[float, int]