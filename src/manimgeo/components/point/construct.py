from typing import Union, Literal

PointConstructType = Literal[
    "Free", # Free Type
    "Constraint", "MidPP", "MidL", "ExtensionPP", 
    "AxisymmetricPL", "VerticalPL", "ParallelPL", "InversionPCir",
    "IntersectionLL", "IntersectionLCir", "IntersectionCirCir",
    "TranslationPV", "CentroidPPP", "CircumcenterPPP", "IncenterPPP",
    "OrthocenterPPP", "Cir", "RotatePPA"
]
Number = Union[float, int]