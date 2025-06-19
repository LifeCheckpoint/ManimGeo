from __future__ import annotations

from .adapter import CircleAdapter
from .construct import CircleConstructType, Number
from ..base import BaseGeometry
from ...utils.utils import GeoUtils
from pydantic import Field
from typing import TYPE_CHECKING, List, Any
import numpy as np

if TYPE_CHECKING:
    from ..point.point import Point
    from ..line.line import LineSegment
    from ..vector.vector import Vector

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
