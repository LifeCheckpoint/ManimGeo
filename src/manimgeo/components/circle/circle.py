from __future__ import annotations

from ..base import GeometryAdapter, BaseGeometry
from ...utils.mathe import GeoMathe
from ...utils.utils import GeoUtils
from pydantic import Field
from typing import TYPE_CHECKING, List, Union, Literal, Any, cast
import numpy as np

if TYPE_CHECKING:
    from ..point.point import Point
    from ..line.line import LineSegment
    from ..vector.vector import Vector

CircleConstructType = Literal[
    "PR", "PP", "L", "PPP", "TranslationCirV",
    "InverseCirCir", "InscribePPP"
]
Number = Union[float, int]

class CircleAdapter(GeometryAdapter):
    center: np.ndarray = Field(default=np.zeros(2), description="计算圆心坐标")
    radius: Number = Field(default=0.0, description="计算圆半径")
    area: Number = Field(default=0.0, description="计算圆面积")
    circumference: Number = Field(default=0.0, description="计算圆周长")
    construct_type: CircleConstructType = Field(description="圆计算方式")
    objs: List[Union[BaseGeometry, Any]] = Field(description="圆适配器依赖的其他对象列表")

    def __call__(self, *objs: Union[BaseGeometry, Any]):
        from ..point.point import Point
        from ..line.line import LineSegment
        from ..vector.vector import Vector

        op_type_map = {
            "PR": [Point, Number],
            "PP": [Point, Point],
            "L": [LineSegment],
            "PPP": [Point, Point, Point],
            "TranslationCirV": [Circle, Vector],
            "InverseCirCir": [Circle, Circle],
            "InscribePPP": [Point, Point, Point]
        }
        GeoUtils.check_params_batch(op_type_map, self.construct_type, objs)

        match self.construct_type:
            case "PR":
                self.center = cast(Point, objs[0]).coord.copy()
                self.radius = cast(Number, objs[1])

            case "PP":
                center = cast(Point, objs[0])
                point = cast(Point, objs[1])
                self.center = center.coord.copy()
                self.radius = np.linalg.norm(point.coord - center.coord) # type: ignore

            case "L":
                start = cast(LineSegment, objs[0]).start.copy()
                end = cast(LineSegment, objs[0]).end.copy()
                self.center = start
                self.radius = np.linalg.norm(end - start) # type: ignore

            case "PPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                self.radius, self.center = GeoMathe.circumcenter_r_c(
                    point1.coord, point2.coord, point3.coord
                )

            case "TranslationCirV":
                circle = cast(Circle, objs[0])
                vec = cast(Vector, objs[1])
                self.center = circle.center + vec.vec
                self.radius = circle.radius

            case "InverseCirCir":
                circle = cast(Circle, objs[0])
                base_circle = cast(Circle, objs[1])
                self.center, self.radius = GeoMathe.inverse_circle(circle.center, circle.radius, base_circle.center, base_circle.radius)

            case "InscribePPP":
                point1 = cast(Point, objs[0])
                point2 = cast(Point, objs[1])
                point3 = cast(Point, objs[2])
                self.radius, self.center = GeoMathe.inscribed_r_c(point1.coord, point2.coord, point3.coord)

            case _:
                raise NotImplementedError(f"Invalid constructing method: {self.construct_type}")

        self.area = np.pi * self.radius ** 2
        self.circumference = 2 * np.pi * self.radius

class Circle(BaseGeometry):
    """
    圆对象，允许如下构造：
    - `PR`: 通过中心点与半径构造圆
    - `PP`: 通过中心点与圆上一点构造圆
    - `L`: 通过半径线段构造圆
    - `PPP`: 通过圆上三点构造圆
    - `TranslationCirV`: 通过平移向量平移原始圆构造新圆
    - `InverseCirCir`: 通过反演圆构造新圆
    - `InscribePPP`: 通过三点构造内切圆
    """
    attrs: List[str] = Field(default=["center", "radius", "area", "circumference"], description="圆属性列表", init=False)
    center: np.ndarray = Field(default=np.zeros(2), description="圆心坐标")
    radius: Number = Field(default=0.0, description="圆半径")
    area: Number = Field(default=0.0, description="圆面积")
    circumference: Number = Field(default=0.0, description="圆周长")

    construct_type: CircleConstructType = Field(description="圆构造方式")
    adapter: CircleAdapter = Field(description="圆适配器", init=False)

    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        self.adapter = CircleAdapter(
            construct_type=self.construct_type,
            objs=self.objs,
        )
        self.name = GeoUtils.get_name(self.name, self, self.adapter.construct_type)

        # 为上游对象添加依赖关系
        for obj in self.objs:
            if isinstance(obj, BaseGeometry):
                obj.add_dependent(self)

        self.update()

    # 构造方法
    @staticmethod
    def PR(center: Point, radius: Number, name: str = "") -> Circle:
        """
        ## 中心与半径构造圆

        `center`: 中心点
        `radius`: 数值半径
        """
        return Circle(
            name=name,
            construct_type="PR",
            objs=[center, radius],
        )
    
    @staticmethod
    def PP(center: Point, point: Point, name: str = "") -> Circle:
        """
        ## 中心与圆上一点构造圆

        `center`: 圆心
        `point`: 圆上一点
        """
        return Circle(
            name=name,
            construct_type="PP",
            objs=[center, point],
        )
    
    @staticmethod
    def L(radius_segment: LineSegment, name: str = "") -> Circle:
        """
        ## 半径线段构造圆

        `radius_segment`: 半径线段
        """
        return Circle(
            name=name,
            construct_type="L",
            objs=[radius_segment],
        )
    
    @staticmethod
    def PPP(point1: Point, point2: Point, point3: Point, name: str = "") -> Circle:
        """
        ## 圆上三点构造圆

        `point1`: 圆上一点
        `point2`: 圆上一点
        `point3`: 圆上一点
        """
        return Circle(
            name=name,
            construct_type="PPP",
            objs=[point1, point2, point3],
        )

    @staticmethod
    def TranslationCirV(circle: Circle, vec: Vector, name: str = "") -> Circle:
        """
        ## 平移构造圆

        `circle`: 原始圆
        `vec`: 平移向量
        """
        return Circle(
            name=name,
            construct_type="TranslationCirV",
            objs=[circle, vec],
        )
    
    @staticmethod
    def InverseCirCir(circle: Circle, base_circle: Circle, name: str = "") -> Circle:
        """
        ## 构造反演圆

        `circle`: 将要进行反演的圆
        `base_circle`: 基圆
        """
        return Circle(
            name=name,
            construct_type="InverseCirCir",
            objs=[circle, base_circle],
        )
    
    @staticmethod
    def InscribePPP(point1: Point, point2: Point, point3: Point, name: str = "") -> Circle:
        """
        ## 三点内切圆

        `point1`: 第一个点
        `point2`: 第二个点
        `point3`: 第三个点
        """
        return Circle(
            name=name,
            construct_type="InscribePPP",
            objs=[point1, point2, point3],
        )
