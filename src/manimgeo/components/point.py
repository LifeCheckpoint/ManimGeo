from manimgeo.components.base import GeometryAdapter, BaseGeometry
from manimgeo.components.line import LineLike, LineSegment
from manimgeo.utils.utils import GeoUtils
from manimgeo.utils.mathe import GeoMathe

import numpy as np
from typing import Union, Literal
from numbers import Number

class PointAdapter(GeometryAdapter):
    # 目前设计中，两点被看作属于 PointAdapter 适配器
    # 在具体对象中需要区分复制的属性
    coord: np.ndarray
    coord1: np.ndarray
    coord2: np.ndarray

    def __init__(
            self,
            construct_type: Literal[
                "Free", "Constraint", "MidPP", "MidL", "ExtensionPP", 
                "AxisymmetricPL", "VerticalPL", "ParallelPL", "InversionPCir",
                "IntersectionLL", "IntersectionLCir", "IntersectionCirCir"
                ],
            current_geo_obj: BaseGeometry,
            *objs: Union[BaseGeometry, any]
        ):
        """
        Free: 自由点（叶子节点）
        Constraint: 约束点（非叶子节点）
        MidPP: 构造两点中点
        MidL: 构造线段中点
        ExtensionPP: 构造比例延长点
        AxisymmetricPL: 构造轴对称点
        VerticalPL: 构造垂点
        ParallelPL: 构造平行线上一点
        InversionPCir: 构造反演点
        IntersectionLL: 构造两线交点
        IntersectionLCir: 构造线圆交点
        IntersectionCirCir: 构造两圆交点
        """
        super().__init__(construct_type)

        # 添加依赖
        [obj.add_dependent(current_geo_obj) for obj in objs if isinstance(obj, BaseGeometry)]

    def __call__(self, *objs: Union[BaseGeometry, any]):
        # 计算构建
        match self.construct_type:
            case "Free" | "Constraint":
                GeoUtils.check_params(objs, np.ndarray)
                self.coord = objs[0]

            case "MidPP":
                GeoUtils.check_params(objs, Point, Point)
                self.coord = (objs[0].coord + objs[1].coord) / 2

            case "MidL":
                GeoUtils.check_params(objs, LineSegment)
                self.coord = (objs[0].start + objs[0].end) / 2

            case "ExtensionPP":
                # start, through, factor
                GeoUtils.check_params(objs, Point, Point, Number)
                self.coord = objs[0].coord + objs[2]*(objs[1].coord - objs[0].coord)

            case "AxisymmetricPL":
                GeoUtils.check_params(objs, Point, LineLike)
                self.coord = GeoMathe.axisymmetric_point(objs[0].coord, objs[1].start, objs[1].end)

            case "VerticalPL":
                GeoUtils.check_params(objs, Point, LineLike)
                self.coord = GeoMathe.vertical_point_to_line(objs[0].coord, objs[1].start, objs[1].end)

            case "ParallelPL":
                # point, line, absolute_distance
                GeoUtils.check_params(objs, Point, LineLike, Number)
                self.coord = objs[0].coord + objs[2]*GeoMathe.unit_direction_vector(objs[1].start, objs[2].end)

            case "InversionPCir":
                from manimgeo.components.circle import Circle
                GeoUtils.check_params(objs, Point, Circle)
                self.coord = GeoMathe.inversion_point(objs[0].coord, objs[1].center, objs[1].radius)

            case "IntersectionLL":
                # line1, line2, regard_as_infinite
                GeoUtils.check_params(objs, LineLike, LineLike, bool)
                self.coord = GeoMathe.intersection_line_line(
                        objs[0].start, objs[0].end, 
                        objs[1].start, objs[1].end,
                        type(objs[0]).__name__, type(objs[1]).__name__,
                        objs[2]
                    )
                
            case "IntersectionLCir":
                from manimgeo.components.circle import Circle
                # line, circle, regard_as_infinite
                GeoUtils.check_params(objs, LineLike, Circle, bool)
                # TODO

            case "IntersectionCirCir":
                from manimgeo.components.circle import Circle
                GeoUtils.check_params(objs, Circle, Circle)
                intersections = GeoMathe.intersection_cir_cir(
                        objs[0].center, objs[0].radius,
                        objs[1].center, objs[1].radius
                    )
                match len(intersections):
                    case 0:
                        raise ValueError("Two circles has no intersection")
                    case 1:
                        self.coord1 = intersections[0].copy()
                        self.coord2 = intersections[0].copy()
                    case 2:
                        self.coord1 = intersections[0]
                        self.coord2 = intersections[1]
                
            case _:
                raise ValueError(f"Invalid construct type: {self.construct_type}")

class Point(BaseGeometry):
    attrs = ["coord"]
    coord: np.ndarray

    def __init__(
            self,
            construct_type: Literal[
                "Free", "Constraint", "MidPP", "MidL", "ExtensionPP", 
                "AxisymmetricPL", "VerticalPL", "ParallelPL", "InversionPCir",
                "IntersectionLL"
                ], 
            *objs, 
            name: str = ""
        ):
        """通过指定构造方式与对象构造点"""
        super().__init__(GeoUtils.get_name(name, self, construct_type))
        self.objs = objs
        self.adapter = PointAdapter(construct_type, self, *objs)
        self.update()
