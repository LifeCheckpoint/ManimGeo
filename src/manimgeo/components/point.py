from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING, Union, Literal, Any
import numpy as np

from manimgeo.components.base import GeometryAdapter, BaseGeometry
from manimgeo.utils.utils import GeoUtils
from manimgeo.utils.mathe import GeoMathe

if TYPE_CHECKING:
    from manimgeo.components.line import Line, LineSegment
    from manimgeo.components.vector import Vector

PointConstructType = Literal[
    "Free", "Constraint", "MidPP", "MidL", "ExtensionPP", 
    "AxisymmetricPL", "VerticalPL", "ParallelPL", "InversionPCir",
    "IntersectionLL", "IntersectionLCir", "IntersectionCirCir",
    "TranslationPV"
]

class PointAdapter(GeometryAdapter):
    # 目前设计中，两点被看作属于 PointAdapter 适配器
    # 在具体对象中需要区分复制的属性
    coord: np.ndarray
    coord1: np.ndarray
    coord2: np.ndarray

    def __init__(
            self,
            construct_type: PointConstructType,
            current_geo_obj: Union["Point", "Points2"],
            *objs: Union[BaseGeometry, Any]
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
        TranslationPV: 构造平移点
        """
        super().__init__(construct_type)

        # 添加依赖
        [obj.add_dependent(current_geo_obj) for obj in objs if isinstance(obj, BaseGeometry)]

    def __call__(self, *objs: Union[BaseGeometry, Any]):
        from manimgeo.components.line import Line, LineSegment

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
                GeoUtils.check_params(objs, Point, Line)
                self.coord = GeoMathe.axisymmetric_point(objs[0].coord, objs[1].start, objs[1].end)

            case "VerticalPL":
                GeoUtils.check_params(objs, Point, Line)
                self.coord = GeoMathe.vertical_point_to_line(objs[0].coord, objs[1].start, objs[1].end)

            case "ParallelPL":
                # point, line, absolute_distance
                GeoUtils.check_params(objs, Point, Line, Number)
                self.coord = objs[0].coord + objs[2]*objs[1].unit_direction

            case "InversionPCir":
                GeoUtils.check_params(objs, Point, Circle)
                self.coord = GeoMathe.inversion_point(objs[0].coord, objs[1].center, objs[1].radius)

            case "IntersectionLL":
                # line1, line2, regard_as_infinite
                GeoUtils.check_params(objs, Line, Line, bool)
                result = GeoMathe.intersection_line_line(
                        objs[0].start, objs[0].end, 
                        objs[1].start, objs[1].end,
                        type(objs[0]).__name__, type(objs[1]).__name__,
                        objs[2]
                    )
                if result[0] and result[1] is not None:
                    self.coord = result[1]
                elif result[0] and result[1] is None:
                    raise ValueError("Infinites intersections")
                else:
                    raise ValueError("No intersections")
                
            case "IntersectionLCir":
                # line, circle, regard_as_infinite
                GeoUtils.check_params(objs, Line, Circle, bool)
                # TODO

            case "IntersectionCirCir":
                GeoUtils.check_params(objs, Circle, Circle)
                result = GeoMathe.intersection_cir_cir(
                        objs[0].center, objs[0].radius,
                        objs[1].center, objs[1].radius
                    )
                if result[0] and len(result[1]) == 2:
                    self.coord1 = result[1][0]
                    self.coord2 = result[1][1]
                elif result[0] and len(result[1]) == 1:
                    self.coord1 = result[1][0].copy()
                    self.coord2 = result[1][0].copy()
                elif result[0] and len(result[1]) == 0:
                    raise ValueError("Two circles has infinite intersections")
                else:
                    raise ValueError("Two circles has no intersection")

            case "TranslationPV":
                GeoUtils.check_params(objs, Point, Vector)
                self.coord = objs[0].coord + objs[1].vec

            case _:
                raise ValueError(f"Invalid construct type: {self.construct_type}")

class Point(BaseGeometry):
    attrs = ["coord"]
    coord: np.ndarray

    def __init__(self, construct_type: PointConstructType, *objs, name: str = ""):
        """通过指定构造方式与对象构造点"""
        super().__init__(GeoUtils.get_name(name, self, construct_type))
        self.objs = objs
        self.adapter = PointAdapter(construct_type, self, *objs)
        self.update()

    # 叶子节点开洞更新
    def set_coord(self, coord: np.ndarray):
        """
        ## 更新 `PointFree` 坐标

        坐标设置仅对于 Free 构造有效，其他构造类型将抛出 ValueError
        """
        if self.adapter.construct_type not in {"Free"}:
            raise ValueError("Cannot set coord of non-leaf node")
        
        self.update_by(coord)

class Points2(BaseGeometry):
    attrs = ["coord1", "coord2"]
    coord1: np.ndarray
    coord2: np.ndarray

    def __init__(
            self,
            construct_type: Literal[
                "IntersectionLCir", "IntersectionCirCir"
                ], 
            *objs, 
            name: str = ""
        ):
        """通过指定构造方式与对象构造两个交点"""
        super().__init__(GeoUtils.get_name(name, self, construct_type))
        self.objs = objs
        self.adapter = PointAdapter(construct_type, self, *objs)
        self.update()

# Constructing Methods

from manimgeo.components.circle import Circle

# 单点构造

def PointFree(coord: np.ndarray, name: str = ""):
    """
    ## 构造自由点（叶子节点）

    `coord`: 点坐标
    """
    return Point("Free", coord, name=name)

def PointConstraint(coord: np.ndarray, name: str = ""):
    """
    ## 构造约束点（非叶子节点）
    
    `coord`: 初始坐标（被后续依赖更新覆盖）
    """
    return Point("Constraint", coord, name=name)

def PointMidPP(point1: Point, point2: Point, name: str = ""):
    """
    ## 构造两点中点
    
    `point1`: 第一个点  
    `point2`: 第二个点
    """
    return Point("MidPP", point1, point2, name=name)

def PointMidL(line: LineSegment, name: str = ""):
    """
    ## 构造线段中点
    
    `line`: 线段对象
    """
    return Point("MidL", line, name=name)

def PointExtensionPP(start: Point, through: Point, factor: Number, name: str = ""):
    """
    ## 构造比例延长（位似）点
    
    `start`: 起点  
    `through`: 经过点  
    `factor`: 延长比例, 1 为恒等延长
    """
    return Point("ExtensionPP", start, through, factor, name=name)

def PointAxisymmetricPL(point: Point, line: Line, name: str = ""):
    """
    ## 构造轴对称点
    
    `point`: 原始点  
    `line`: 对称轴线
    """
    return Point("AxisymmetricPL", point, line, name=name)

def PointVerticalPL(point: Point, line: Line, name: str = ""):
    """
    ## 构造垂足点
    
    `point`: 原始基准点
    `line`: 目标直线
    """
    return Point("VerticalPL", point, line, name=name)

def PointParallelPL(point: Point, line: Line, distance: Number, name: str = ""):
    """
    ## 构造平行线上一点
    
    `point`: 基准点
    `line`: 平行基准线
    `distance`: 沿平行方向的绝对距离
    """
    return Point("ParallelPL", point, line, distance, name=name)

def PointInversionPCir(point: Point, circle: Circle, name: str = ""):
    """
    ## 构造反演点
    
    `point`: 原始点  
    `circle`: 反演基准圆
    """
    return Point("InversionPCir", point, circle, name=name)

def PointIntersectionLL(line1: Line, line2: Line, regard_infinite: bool = False, name: str = ""):
    """
    ## 构造两线交点
    
    `line1`: 第一条线  
    `line2`: 第二条线  
    `regard_infinite`: 是否视为无限长直线
    """
    return Point("IntersectionLL", line1, line2, regard_infinite, name=name)

# 双点构造

def Points2IntersectionLCir(line: Line, circle: Circle, regard_infinite: bool = False, name: str = ""):
    """
    ## 构造线与圆的交点对
    
    `line`: 直线/线段  
    `circle`: 圆  
    `regard_infinite`: 是否视为无限长直线
    """
    return Points2("IntersectionLCir", line, circle, regard_infinite, name=name)

def Points2IntersectionCirCir(circle1: Circle, circle2: Circle, name: str = ""):
    """
    ## 构造两圆交点对
    
    `circle1`: 第一个圆  
    `circle2`: 第二个圆
    """
    return Points2("IntersectionCirCir", circle1, circle2, name=name)

def PointTranslationPV(point: Point, vector: Vector, name: str = ""):
    """
    ## 构造平移点

    `point`: 原始点
    `vector`: 平移向量
    """
    return Point("TranslationPV", point, vector, name=name)