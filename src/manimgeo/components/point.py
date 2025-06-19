from __future__ import annotations

from ..components.base import GeometryAdapter, BaseGeometry
from ..utils.mathe import GeoMathe
from ..utils.utils import GeoUtils
from pydantic import Field
from typing import TYPE_CHECKING, Union, Literal, Any, List, cast
import numpy as np

if TYPE_CHECKING:
    from ..components.angle import Angle
    from ..components.line import Line, LineSegment
    from ..components.vector import Vector

PointConstructType = Literal[
    "Free", # Free Type
    "Constraint", "MidPP", "MidL", "ExtensionPP", 
    "AxisymmetricPL", "VerticalPL", "ParallelPL", "InversionPCir",
    "IntersectionLL", "IntersectionLCir", "IntersectionCirCir",
    "TranslationPV", "CentroidPPP", "CircumcenterPPP", "IncenterPPP",
    "OrthocenterPPP", "Cir", "RotatePPA"
]
Number = Union[float, int]

class PointAdapter(GeometryAdapter):
    coord: np.ndarray = Field(default=np.zeros(2), description="计算点坐标", init=False)
    construct_type: PointConstructType = Field(description="点计算方式")
    objs: List[Union[BaseGeometry, Any]] = Field(description="点适配器依赖的其他对象列表")

    def __call__(self, *objs: Union[BaseGeometry, Any]):
        from ..components.line import Line, LineSegment
        from ..components.circle import Circle
        from ..components.vector import Vector
        from ..components.angle import Angle

        op_type_map = {
            "Free": [np.ndarray], "Constraint": [np.ndarray],
            "MidPP": [Point, Point],
            "MidL": [LineSegment],
            "ExtensionPP": [Point, Point, Number], # start, through, factor
            "AxisymmetricPL": [Point, Line],
            "VerticalPL": [Point, Line],
            "ParallelPL": [Point, Line, Number], # point, line, absolute_distance
            "InversionPCir": [Point, Circle],
            "IntersectionLL": [Line, Line, bool], # line1, line2, regard_as_infinite
            "IntersectionLCir": [Line, Circle, bool], # line, circle, regard_as_infinite
            "IntersectionCirCir": [Circle, Circle],
            "TranslationPV": [Point, Vector],
            "CentroidPPP": [Point, Point, Point],
            "CircumcenterPPP": [Point, Point, Point],
            "IncenterPPP": [Point, Point, Point],
            "OrthocenterPPP": [Point, Point, Point],
            "Cir": [Circle],
            "RotatePPA": [Point, Point, Angle] # point, center, angle
        }
        GeoUtils.check_params_batch(op_type_map, self.construct_type, objs)

        match self.construct_type:
            case "Free" | "Constraint":
                self.coord = cast(np.ndarray, objs[0])

            case "MidPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                self.coord = (point1.coord + point2.coord) / 2

            case "MidL":
                seg_line = cast(LineSegment, objs[0])
                self.coord = (seg_line.start + seg_line.end) / 2

            case "ExtensionPP":
                start = cast(Point, objs[0])
                through = cast(Point, objs[1])
                factor = cast(Number, objs[2])
                self.coord = start.coord + factor * (through.coord - start.coord)

            case "AxisymmetricPL":
                point = cast(Point, objs[0])
                line = cast(Line, objs[1])
                self.coord = GeoMathe.axisymmetric_point(point.coord, line.start, line.end)

            case "VerticalPL":
                point = cast(Point, objs[0])
                line = cast(Line, objs[1])
                self.coord = GeoMathe.vertical_point_to_line(point.coord, line.start, line.end)

            case "ParallelPL":
                point = cast(Point, objs[0])
                line = cast(Line, objs[1])
                distance = cast(Number, objs[2])
                self.coord = point.coord + distance * line.unit_direction

            case "InversionPCir":
                point = cast(Point, objs[0])
                circle = cast(Circle, objs[1])
                self.coord = GeoMathe.inversion_point(point.coord, circle.center, circle.radius)

            case "IntersectionLL":
                line1 = cast(Line, objs[0])
                line2 = cast(Line, objs[1])
                regard_infinite = cast(bool, objs[2])
                result = GeoMathe.intersection_line_line(
                    line1.start, line1.end,
                    line2.start, line2.end,
                    type(line1).__name__, type(line2).__name__, # type: ignore
                    regard_infinite
                )
                if result[0] and result[1] is not None:
                    self.coord = result[1]
                elif result[0] and result[1] is None:
                    raise ValueError("Infinites intersections")
                else:
                    raise ValueError("No intersections")
                
            # case "IntersectionLCir":
            #     result = GeoMathe.intersection_line_cir(
            #             objs[0].start, objs[0].end,
            #             objs[1].center, objs[1].radius,
            #             type(objs[0]).__name__ if not objs[2] else "InfinityLine"
            #         )
            #     if len(result) == 0:
            #         raise ValueError("No intersections")
            #     elif len(result) == 1:
            #         self.coord1 = result[0].copy()
            #         self.coord2 = result[0].copy()
            #     else:
            #         self.coord1 = result[0].copy()
            #         self.coord2 = result[1].copy()

            # case "IntersectionCirCir":
            #     result = GeoMathe.intersection_cir_cir(
            #             objs[0].center, objs[0].radius,
            #             objs[1].center, objs[1].radius
            #         )
            #     if result[0] and len(result[1]) == 2:
            #         self.coord1 = result[1][0]
            #         self.coord2 = result[1][1]
            #     elif result[0] and len(result[1]) == 1:
            #         self.coord1 = result[1][0].copy()
            #         self.coord2 = result[1][0].copy()
            #     elif result[0] and len(result[1]) == 0:
            #         raise ValueError("Two circles has infinite intersections")
            #     else:
            #         raise ValueError("Two circles has no intersection")

            case "TranslationPV":
                point = cast(Point, objs[0])
                vector = cast(Vector, objs[1])
                self.coord = point.coord + vector.vec

            case "CentroidPPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                self.coord = (point1.coord + point2.coord + point3.coord) / 3

            case "CircumcenterPPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                _, self.coord = GeoMathe.circumcenter_r_c(
                    point1.coord, point2.coord, point3.coord
                )

            case "IncenterPPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                _, self.coord = GeoMathe.inscribed_r_c(
                    point1.coord, point2.coord, point3.coord
                )

            case "OrthocenterPPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                self.coord = GeoMathe.orthocenter(
                    point1.coord, point2.coord, point3.coord
                )

            case "Cir":
                circle = cast(Circle, objs[0])
                self.coord = circle.center

            # case "2":
            #     if objs[1] == 0:
            #         self.coord = objs[0].coord1
            #     elif objs[1] == 1:
            #         self.coord = objs[0].coord2
            #     else:
            #         raise ValueError("Index of points should be 0 or 1")
                
            # case "2Filter":
            #     if objs[1](objs[0].coord1):
            #         self.coord = objs[0].coord1
            #     elif objs[1](objs[0].coord2):
            #         self.coord = objs[0].coord2
            #     else:
            #         raise ValueError("No point fits condition")
                
            case "RotatePPA":
                point = cast(Point, objs[0])
                center = cast(Point, objs[1])
                angle = cast(Angle, objs[2])
                angle_num = angle.angle if angle.turn == 'Counterclockwise' else (2 * np.pi - angle.angle) # type: ignore
                self.coord = GeoMathe.angle_3p_countclockwise(point.coord, center.coord, angle_num) # type: ignore

            case _:
                raise NotImplementedError(f"Invalid construct type: {self.construct_type}")

from ..components.circle import Circle

class Point(BaseGeometry):
    """
    点对象，允许如下构造：
    - `Free`: 自由点（叶子节点）
    - `Constraint`: 约束点（非叶子节点）
    - `MidPP`: 构造两点中点
    - `MidL`: 构造线段中点
    - `ExtensionPP`: 构造比例延长点
    - `AxisymmetricPL`: 构造轴对称点
    - `VerticalPL`: 构造垂点
    - `ParallelPL`: 构造平行线上一点
    - `InversionPCir`: 构造反演点
    - `IntersectionLL`: 构造两线交点
    - `IntersectionLCir`: 构造线圆交点
    - `IntersectionCirCir`: 构造两圆交点
    - `TranslationPV`: 构造平移点
    - `CentroidPPP`: 构造重心
    - `CircumcenterPPP`: 构造外心
    - `IncenterPPP`: 构造内心
    - `OrthocenterPPP`: 构造垂心
    - `Cir`: 构造圆心
    - `RotatePPA`: 两点旋转角构建旋转点
    """
    attrs: List[str] = Field(default=["coord"], description="点属性列表", init=False)
    coord: np.ndarray = Field(default_factory=lambda: np.zeros(2), description="点坐标", init=False)
    
    construct_type: PointConstructType = Field(description="点构造方式")
    adapter: PointAdapter = Field(description="点适配器", init=False)

    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        self.adapter = PointAdapter(
            construct_type=self.construct_type,
            objs=self.objs,
        )
        self.name = GeoUtils.get_name(self.name, self, self.adapter.construct_type)

        # 为上游对象添加依赖关系
        for obj in self.objs:
            if isinstance(obj, BaseGeometry):
                obj.add_dependent(self)

        self.update()

    # 叶子节点开洞更新
    def set_coord(self, coord: np.ndarray):
        """
        ## 更新 `PointFree` 坐标

        坐标设置仅对于 Free 构造有效，其他构造类型将抛出 ValueError
        """
        if self.adapter.construct_type not in ["Free"]:
            raise ValueError("Cannot set coord of non-leaf node")
        
        self.update(coord)

    # 构造方法
    @staticmethod
    def Free(coord: np.ndarray, name: str = "") -> Point:
        """
        构造自由点（叶子节点）

        `coord`: 点坐标
        """
        return Point(
            name=name,
            construct_type="Free",
            objs=[coord]
        )
    
    @staticmethod
    def Constraint(coord: np.ndarray, name: str = "") -> Point:
        """
        构造约束点（非叶子节点）

        `coord`: 初始坐标（被后续依赖更新覆盖）
        """
        return Point(
            name=name,
            construct_type="Constraint",
            objs=[coord]
        )

    @staticmethod
    def MidPP(point1: Point, point2: Point, name: str = "") -> Point:
        """
        构造两点中点

        `point1`: 第一个点  
        `point2`: 第二个点
        """
        return Point(
            name=name,
            construct_type="MidPP",
            objs=[point1, point2]
        )

    @staticmethod
    def MidL(line: LineSegment, name: str = "") -> Point:
        """
        构造线段中点

        `line`: 线段对象
        """
        return Point(
            name=name,
            construct_type="MidL",
            objs=[line]
        )
    
    @staticmethod
    def ExtensionPP(start: Point, through: Point, factor: Number, name: str = "") -> Point:
        """
        构造比例延长（位似）点

        `start`: 起点  
        `through`: 经过点  
        `factor`: 延长比例, 1 为恒等延长
        """
        return Point(
            name=name,
            construct_type="ExtensionPP",
            objs=[start, through, factor]
        )
    
    @staticmethod
    def AxisymmetricPL(point: Point, line: Line, name: str = "") -> Point:
        """
        构造轴对称点

        `point`: 原始点  
        `line`: 对称轴线
        """
        return Point(
            name=name,
            construct_type="AxisymmetricPL",
            objs=[point, line]
        )
    
    @staticmethod
    def VerticalPL(point: Point, line: Line, name: str = "") -> Point:
        """
        构造垂足点

        `point`: 原始基准点  
        `line`: 目标直线
        """
        return Point(
            name=name,
            construct_type="VerticalPL",
            objs=[point, line]
        )
    
    @staticmethod
    def ParallelPL(point: Point, line: Line, distance: Number, name: str = "") -> Point:
        """
        构造平行线上一点

        `point`: 基准点  
        `line`: 平行基准线  
        `distance`: 沿平行方向的绝对距离
        """
        return Point(
            name=name,
            construct_type="ParallelPL",
            objs=[point, line, distance]
        )

    @staticmethod
    def InversionPCir(point: Point, circle: Circle, name: str = "") -> Point:
        """
        构造反演点

        `point`: 原始点  
        `circle`: 反演基准圆
        """
        return Point(
            name=name,
            construct_type="InversionPCir",
            objs=[point, circle]
        )
    
    @staticmethod
    def IntersectionLL(line1: Line, line2: Line, regard_infinite: bool = False, name: str = "") -> Point:
        """
        构造两线交点

        `line1`: 第一条线  
        `line2`: 第二条线  
        `regard_infinite`: 是否视为无限长直线
        """
        return Point(
            name=name,
            construct_type="IntersectionLL",
            objs=[line1, line2, regard_infinite]
        )
    
    @staticmethod
    def TranslationPV(point: Point, vector: Vector, name: str = "") -> Point:
        """
        构造平移点

        `point`: 原始点  
        `vector`: 平移向量
        """
        return Point(
            name=name,
            construct_type="TranslationPV",
            objs=[point, vector]
        )
    
    @staticmethod
    def CentroidPPP(point1: Point, point2: Point, point3: Point) -> Point:
        """
        构造三角形重心

        `point1`: 第一个顶点  
        `point2`: 第二个顶点  
        `point3`: 第三个顶点
        """
        return Point(
            name=GeoUtils.get_name("", point1, "CentroidPPP"),
            construct_type="CentroidPPP",
            objs=[point1, point2, point3]
        )

    @staticmethod
    def CircumcenterPPP(point1: Point, point2: Point, point3: Point, name: str = "") -> Point:
        """
        构造三角形外心

        `point1`: 第一个顶点  
        `point2`: 第二个顶点  
        `point3`: 第三个顶点
        """
        return Point(
            name=name,
            construct_type="CircumcenterPPP",
            objs=[point1, point2, point3]
        )
    
    @staticmethod
    def IncenterPPP(point1: Point, point2: Point, point3: Point, name: str = "") -> Point:
        """
        构造三角形内心

        `point1`: 第一个顶点  
        `point2`: 第二个顶点  
        `point3`: 第三个顶点
        """
        return Point(
            name=name,
            construct_type="IncenterPPP",
            objs=[point1, point2, point3]
        )
    
    @staticmethod
    def OrthocenterPPP(point1: Point, point2: Point, point3: Point, name: str = "") -> Point:
        """
        构造三角形垂心

        `point1`: 第一个顶点  
        `point2`: 第二个顶点  
        `point3`: 第三个顶点
        """
        return Point(
            name=name,
            construct_type="OrthocenterPPP",
            objs=[point1, point2, point3]
        )
    
    @staticmethod
    def Cir(circle: Circle, name: str = "") -> Point:
        """
        构造圆心

        `circle`: 圆对象
        """
        return Point(
            name=name,
            construct_type="Cir",
            objs=[circle]
        )
    
    @staticmethod
    def RotatePPA(point: Point, center: Point, angle: Angle, name: str = "") -> Point:
        """
        构造旋转点

        `point`: 原始点  
        `center`: 旋转中心  
        `angle`: 旋转角度
        """
        return Point(
            name=name,
            construct_type="RotatePPA",
            objs=[point, center, angle]
        )


    
# 双点构造

# def PointIntersectionLCir(
#         line: Line, 
#         circle: Circle, 
#         filter: Optional[Callable[[np.ndarray], bool]] = None, 
#         regard_infinite: bool = False, 
#         name: str = ""
#     ) -> Union[List[Point], Point]:
#     """
#     ## 构造线与圆的交点对
    
#     `line`: 直线/线段  
#     `circle`: 圆  
#     `filter`: 返回交点坐标须满足的条件，如果提供则返回第一个满足条件的单点对象
#     `regard_infinite`: 是否视为无限长直线
#     """
#     points2 = Points2("IntersectionLCir", line, circle, regard_infinite, name=name)
#     if filter == None:
#         return PointOfPoints2List(points2, name=name)
#     else:
#         return PointOfPoints2Fit(points2, filter, name=name)

# def PointIntersectionCirCir(circle1: Circle, circle2: Circle, filter: Optional[Callable[[np.ndarray], bool]] = None, name: str = ""):
#     """
#     ## 构造两圆交点对
    
#     `circle1`: 第一个圆  
#     `circle2`: 第二个圆
#     `filter`: 返回交点坐标须满足的条件，如果提供则返回第一个满足条件的单点对象
#     """
#     points2 = Points2("IntersectionCirCir", circle1, circle2, name=name)
#     if filter == None:
#         return PointOfPoints2List(points2, name=name)
#     else:
#         return PointOfPoints2Fit(points2, filter, name=name)

# def PointOfPoints2(points2: Points2, index: Literal[0, 1], name: str = ""):
#     """
#     ## 获取两点中的单点对象

#     `points2`: 两点组合对象
#     `index`: 两点中的其中一点索引
#     """
#     return Point("2", points2, index, name=name)

# def PointOfPoints2List(points2: Points2, name: str = ""):
#     """
#     ## 获取两点中的单点对象列表

#     `points2`: 两点组合对象
#     """
#     return [PointOfPoints2(points2, 0, name), PointOfPoints2(points2, 1, name)]

# def PointOfPoints2Fit(points2: Points2, filter: Callable[[np.ndarray], bool], name: str = ""):
#     """
#     ## 获得两点中符合条件的第一个单点对象

#     `points2`: 两点组合对象
#     `filter`: 给定点坐标，返回是否符合条件
#     """
#     return Point("2Filter", points2, filter, name=name)