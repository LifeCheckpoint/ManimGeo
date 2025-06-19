from __future__ import annotations

from ...utils.utils import GeoUtils
from ..base import BaseGeometry
from .adapter import VectorAdapter
from .construct import VectorConstructType, Number
from pydantic import Field
from typing import TYPE_CHECKING, List, Any
import numpy as np

if TYPE_CHECKING:
    from ..line import LineSegment
    from ..point import Point

class Vector(BaseGeometry):
    """
    向量对象，允许如下构造：
    - `PP`: 两点构建向量
    - `L`: 线段构建向量
    - `N`: （数值）构建向量
    - `NPP`: 两点（数值）构建向量
    - `NNormDirection`: 模长方向（数值）构建向量
    - `AddVV`: 向量加法
    - `SubVV`: 向量减法
    - `MulNV`: 数乘向量
    """
    attrs: List[str] = Field(default=["vec", "norm", "unit_direction"], description="向量属性列表")
    vec: np.ndarray = Field(default=np.zeros(2), description="向量坐标", init=False)
    norm: Number = Field(default=0.0, description="向量模长", init=False)
    unit_direction: np.ndarray = Field(default=np.zeros(2), description="向量单位方向", init=False)

    construct_type: VectorConstructType = Field(description="向量构造方式")
    adapter: VectorAdapter = Field(description="向量适配器", init=False)

    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        self.adapter = VectorAdapter(
            construct_type=self.construct_type,
            objs=self.objs,
        )
        self.name = GeoUtils.get_name(self.name, self, self.adapter.construct_type)

        # 为上游对象添加依赖关系
        for obj in self.objs:
            if isinstance(obj, BaseGeometry):
                obj.add_dependent(self)

        self.update()

    def __add__(self, other: Vector):
        return Vector(
            name=f"{self.name} + {other.name}",
            construct_type="AddVV",
            objs=[self, other],
        )
    
    def __sub__(self, other: Vector):
        return Vector(
            name=f"{self.name} - {other.name}",
            construct_type="SubVV",
            objs=[self, other],
        )
    
    def __mul__(self, other: Number):
        return Vector(
            name=f"{other} * {self.name}",
            construct_type="MulNV",
            objs=[other, self],
        )
    
    # 构造方法
    @staticmethod
    def PP(start: Point, end: Point, name: str = ""):
        """
        通过两点构造向量

        `start`: 起点
        `end`: 终点
        """
        return Vector(
            name=name,
            construct_type="PP",
            objs=[start, end]
        )
    
    @staticmethod
    def L(line: LineSegment, name: str = ""):
        """
        通过线段构造向量

        `line`: 线段
        """
        return Vector(
            name=name,
            construct_type="L",
            objs=[line]
        )
    
    @staticmethod
    def N(vec: np.ndarray, name: str = ""):
        """
        （数值）构造向量

        `vec`: 向量数值
        """
        return Vector(
            name=name,
            construct_type="N",
            objs=[vec]
        )
    
    @staticmethod
    def NPP(start: np.ndarray, end: np.ndarray, name: str = ""):
        """
        通过两点（数值）构造向量

        `start`: 起点
        `end`: 终点
        """
        return Vector(
            name=name,
            construct_type="NPP",
            objs=[start, end]
        )
    
    @staticmethod
    def NNormDirection(norm: Number, direction: np.ndarray, name: str = ""):
        """
        通过模长与方向构造向量

        `norm`: 模长
        `direction`: 方向
        """
        return Vector(
            name=name,
            construct_type="NNormDirection",
            objs=[norm, direction]
        )
    