from ..components.base import GeometryAdapter, BaseGeometry
from .angle import Angle, AngleAdapter, AngleConstructArgsList
from .circle import Circle, CircleAdapter, CircleConstructArgsList
from .line import Line, LineSegment, Ray, InfinityLine, LineAdapter, LineConstructArgsList
from .point import Point, PointAdapter, PointConstructArgsList
from .vector import Vector, VectorAdapter, VectorConstructArgsList

# 在所有组件导入后进行模型重建

# 重建几何对象
Angle.model_rebuild()
Circle.model_rebuild()
Line.model_rebuild()
LineSegment.model_rebuild()
Ray.model_rebuild()
InfinityLine.model_rebuild()
Point.model_rebuild()
Vector.model_rebuild()

# 重建适配器
GeometryAdapter.model_rebuild()
AngleAdapter.model_rebuild()
CircleAdapter.model_rebuild()
LineAdapter.model_rebuild()
PointAdapter.model_rebuild()
VectorAdapter.model_rebuild()

# 重建所有组合方法
construct_arg_list = AngleConstructArgsList + CircleConstructArgsList + LineConstructArgsList + PointConstructArgsList + VectorConstructArgsList
for construct_args in construct_arg_list:
    if hasattr(construct_args, 'model_rebuild'):
        construct_args.model_rebuild()