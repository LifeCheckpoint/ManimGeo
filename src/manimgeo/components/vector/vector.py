from __future__ import annotations

from ...utils.utils import GeoUtils
from pydantic import Field, validate_call
from typing import TYPE_CHECKING, List, Any
import numpy as np

from ..base import BaseGeometry
from .adapter import VectorAdapter
from .construct import *

if TYPE_CHECKING:
    from ..line import LineSegment
    from ..point import Point

class Vector(BaseGeometry):
    attrs: List[str] = Field(default=["vec", "norm", "unit_direction"], description="向量属性列表", init=False)
    vec: np.ndarray = Field(default=np.zeros(2), description="向量坐标", init=False)
    norm: Number = Field(default=0.0, description="向量模长", init=False)
    unit_direction: np.ndarray = Field(default=np.zeros(2), description="向量单位方向", init=False)

    args: VectorConstructArgs = Field(discriminator='construct_type', description="向量构造参数")

    @property
    def construct_type(self) -> VectorConstructType:
        return self.args.construct_type

    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        self.adapter = VectorAdapter(args=self.args)
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

    def __add__(self, other: Vector):
        return Vector(
            name=f"{self.name} + {other.name}",
            args=AddVVArgs(vec1=self, vec2=other),
        )

    def __sub__(self, other: Vector):
        return Vector(
            name=f"{self.name} - {other.name}",
            args=SubVVArgs(vec1=self, vec2=other),
        )

    def __mul__(self, other: Number):
        return Vector(
            name=f"{other} * {self.name}",
            args=MulNVArgs(factor=other, vec=self),
        )

    # 构造方法
    @staticmethod
    @validate_call
    def PP(start: Point, end: Point, name: str = ""):
        """
        通过两点构造向量

        `start`: 起点
        `end`: 终点
        """
        return Vector(
            name=name,
            args=PPArgs(start=start, end=end)
        )

    @staticmethod
    @validate_call
    def L(line: LineSegment, name: str = ""):
        """
        通过线段构造向量

        `line`: 线段
        """
        return Vector(
            name=name,
            args=LArgs(line=line)
        )

    @staticmethod
    @validate_call
    def N(vec: np.ndarray, name: str = ""):
        """
        （数值）构造向量

        `vec`: 向量数值
        """
        return Vector(
            name=name,
            args=NArgs(vec=vec)
        )

    @staticmethod
    @validate_call
    def NPP(start: np.ndarray, end: np.ndarray, name: str = ""):
        """
        通过两点（数值）构造向量

        `start`: 起点
        `end`: 终点
        """
        return Vector(
            name=name,
            args=NPPArgs(start=start, end=end)
        )

    @staticmethod
    @validate_call
    def NNormDirection(norm: Number, direction: np.ndarray, name: str = ""):
        """
        通过模长与方向构造向量

        `norm`: 模长
        `direction`: 方向
        """
        return Vector(
            name=name,
            args=NNormDirectionArgs(norm=norm, direction=direction)
        )