from ..components.base import GeometryAdapter, BaseGeometry
from .angle import Angle
from .circle import Circle
from .line import Line, LineSegment, Ray, InfinityLine
from .point import Point
from .vector import Vector

# 在所有组件导入后进行模型重建
Angle.model_rebuild()
Circle.model_rebuild()
Line.model_rebuild()
LineSegment.model_rebuild()
Ray.model_rebuild()
InfinityLine.model_rebuild()
Point.model_rebuild()
Vector.model_rebuild()