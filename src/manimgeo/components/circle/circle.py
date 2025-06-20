from __future__ import annotations

from ...utils.utils import GeoUtils
from pydantic import Field, validate_call
from typing import TYPE_CHECKING, List, Any
import numpy as np

from ..base import BaseGeometry
from .adapter import CircleAdapter
from .construct import *

if TYPE_CHECKING:
    from ..line import LineSegment
    from ..point import Point
    from ..vector import Vector

class Circle(BaseGeometry):
    attrs: List[str] = Field(default=["center", "radius", "area", "circumference"], description="圆属性列表", init=False)
    center: np.ndarray = Field(default=np.zeros(2), description="圆心坐标", init=False)
    radius: Number = Field(default=0.0, description="圆半径", init=False)
    area: Number = Field(default=0.0, description="圆面积", init=False)
    circumference: Number = Field(default=0.0, description="圆周长", init=False)

    args: CircleConstructArgs = Field(discriminator='construct_type', description="圆构造参数")

    @property
    def construct_type(self) -> CircleConstructType:
        return self.args.construct_type

    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        self.adapter = CircleAdapter(args=self.args)
        self.name = GeoUtils.get_name(self.name, self, self.adapter.construct_type)

        # 遍历 args 模型中的所有 BaseGeometry 实例，并添加到 _dependencies
        # 普通类型将被忽略
        for field_name, field_info in self.args.__class__.model_fields.items():
            field_value = getattr(self.args, field_name)

            # 基本几何对象
            if isinstance(field_value, BaseGeometry):
                self._add_dependency(field_value)

            # 列表类型依赖 (extended)
            elif isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, BaseGeometry):
                        self._add_dependency(item)

            # 可拓展

        self.update() # 首次计算

    # 构造方法
    
    @classmethod
    @validate_call
    def PR(cls, center: Point, radius: Number, name: str = "") -> Circle:
        """
        中心与半径构造圆

        - `center`: 中心点
        - `radius`: 数值半径
        """
        return Circle(
            name=name,
            args=PRArgs(center=center, radius=radius),
        )

    @classmethod
    @validate_call
    def PP(cls, center: Point, point: Point, name: str = "") -> Circle:
        """
        中心与圆上一点构造圆

        - `center`: 圆心
        - `point`: 圆上一点
        """
        return Circle(
            name=name,
            args=PPArgs(center=center, point=point),
        )

    @classmethod
    @validate_call
    def L(cls, radius_segment: LineSegment, name: str = "") -> Circle:
        """
        半径线段构造圆

        - `radius_segment`: 半径线段
        """
        return Circle(
            name=name,
            args=LArgs(radius_segment=radius_segment),
        )

    @classmethod
    @validate_call
    def PPP(cls, point1: Point, point2: Point, point3: Point, name: str = "") -> Circle:
        """
        圆上三点构造圆

        - `point1`: 圆上一点
        - `point2`: 圆上一点
        - `point3`: 圆上一点
        """
        return Circle(
            name=name,
            args=PPPArgs(point1=point1, point2=point2, point3=point3),
        )

    @classmethod
    @validate_call
    def TranslationCirV(cls, circle: Circle, vec: Vector, name: str = "") -> Circle:
        """
        平移构造圆

        - `circle`: 原始圆
        - `vec`: 平移向量
        """
        return Circle(
            name=name,
            args=TranslationCirVArgs(circle=circle, vector=vec),
        )

    @classmethod
    @validate_call
    def InverseCirCir(cls, circle: Circle, base_circle: Circle, name: str = "") -> Circle:
        """
        构造反演圆

        - `circle`: 将要进行反演的圆
        - `base_circle`: 基圆
        """
        return Circle(
            name=name,
            args=InverseCirCirArgs(circle=circle, base_circle=base_circle),
        )

    @classmethod
    @validate_call
    def InscribePPP(cls, point1: Point, point2: Point, point3: Point, name: str = "") -> Circle:
        """
        三点内切圆

        - `point1`: 第一个点
        - `point2`: 第二个点
        - `point3`: 第三个点
        """
        return Circle(
            name=name,
            args=InscribePPPArgs(point1=point1, point2=point2, point3=point3),
        )