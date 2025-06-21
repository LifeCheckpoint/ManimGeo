from __future__ import annotations

from pydantic import Field, model_validator
from typing import TYPE_CHECKING, List, Any, Optional
import numpy as np

from ..base import BaseGeometry
from .adapter import CircleAdapter
from .construct import *
from ...math.vectors import get_two_vector_from_normal

if TYPE_CHECKING:
    from ..line import LineSegment
    from ..point import Point
    from ..vector import Vector

class Circle(BaseGeometry):
    attrs: List[str] = Field(default=["center", "radius", "normal", "area", "circumference"], description="圆属性列表", init=False)
    center: np.ndarray = Field(default=np.zeros(2), description="圆心坐标", init=False)
    radius: Number = Field(default=0.0, description="圆半径", init=False)
    normal: np.ndarray = Field(default=np.array([0.0, 0.0, 1.0]), description="圆所在平面的法向量", init=False)
    area: Number = Field(default=0.0, description="圆面积", init=False)
    circumference: Number = Field(default=0.0, description="圆周长", init=False)

    args: CircleConstructArgs = Field(discriminator='construct_type', description="圆构造参数")

    @model_validator(mode='before')
    @classmethod
    def set_adapter_before_validation(cls, data: Any) -> Any:
        """在验证前设置 adapter 字段"""
        if isinstance(data, dict) and 'args' in data:
            # 假设 args 已经是 Pydantic 模型或可以被 CircleAdapter 接受
            data['adapter'] = CircleAdapter(args=data['args'])
        return data

    @property
    def construct_type(self) -> CircleConstructType:
        return self.args.construct_type

    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        self.adapter = CircleAdapter(args=self.args)
        self.name = self.get_name(self.name)

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

    def get_point_at_angle(self, angle: Number) -> np.ndarray:
        """
        根据角度参数生成圆上的点。

        - `angle`: 角度参数，单位为弧度。

        Returns: `np.ndarray`, 圆上的点坐标。
        """
        # 获取圆所在平面的两个正交基向量 u 和 v
        u, v = get_two_vector_from_normal(self.normal)

        # 使用参数方程计算圆上的点
        point_on_circle = (
            self.center
            + self.radius * np.cos(angle) * u
            + self.radius * np.sin(angle) * v
        )
        return point_on_circle

    # 构造方法
    
    @classmethod
    def CNR(cls, center: Point, normal: Vector, radius: Number, name: str = "") -> Circle:
        """
        中心、法向量与半径构造圆

        - `center`: 中心点
        - `normal`: 圆所在平面的法向量
        - `radius`: 数值半径
        """
        return Circle(
            name=name,
            args=CNRArgs(center=center, normal=normal, radius=radius),
        )

    @classmethod
    def PR(cls, center: Point, radius: Number, normal: Optional[Vector] = None, name: str = "") -> Circle:
        """
        中心与半径构造圆

        - `center`: 中心点
        - `radius`: 数值半径
        - `normal`: 可选，圆所在平面的法向量，默认为 [0,0,1]
        """
        return Circle(
            name=name,
            args=PRArgs(center=center, radius=radius, normal=normal),
        )

    @classmethod
    def PP(cls, center: Point, point: Point, normal: Optional[Vector] = None, name: str = "") -> Circle:
        """
        中心与圆上一点构造圆

        - `center`: 圆心
        - `point`: 圆上一点
        - `normal`: 可选，圆所在平面的法向量，默认为 [0,0,1]
        """
        return Circle(
            name=name,
            args=PPArgs(center=center, point=point, normal=normal),
        )

    @classmethod
    def L(cls, radius_segment: LineSegment, normal: Optional[Vector] = None, name: str = "") -> Circle:
        """
        半径线段构造圆

        - `radius_segment`: 半径线段
        - `normal`: 可选，圆所在平面的法向量，默认为 [0,0,1]
        """
        return Circle(
            name=name,
            args=LArgs(radius_segment=radius_segment, normal=normal),
        )

    @classmethod
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
