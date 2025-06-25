"""
MultipleComponents 多对象类
"""

from __future__ import annotations

from pydantic import Field, model_validator
from typing import TYPE_CHECKING, Any, List, Callable

from ..base import BaseGeometry
from .adapter import MultipleAdapter
from .args import *

if TYPE_CHECKING:
    pass

class MultipleComponents(BaseGeometry):
    attrs: List[str] = Field(default=["geometry_objects"], description="多个几何对象组成的列表", init=False)
    geometry_objects: List[BaseGeometry] = Field(default_factory=list, description="多个几何对象", init=False)
    args: MultipleConstructArgs = Field(discriminator='construct_type', description="多几何对象构造参数")

    @model_validator(mode='before')
    @classmethod
    def set_adapter_before_validation(cls, data: Any) -> Any:
        """在验证前设置 adapter 字段"""
        if isinstance(data, dict) and 'args' in data:
            data['adapter'] = MultipleAdapter(args=data['args'])
        return data
    
    @property
    def construct_type(self) -> MultipleConstructType:
        return self.args.construct_type
    
    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        # 实例化 MultipleAdapter，传入 MultipleArgs
        self.adapter = MultipleAdapter(args=self.args)
        self.name = self.get_name(self.name)
        # 添加依赖关系
        self._extract_dependencies_from_args(self.args)
        self.update()

    # 构造方法

    @classmethod
    def Multiple(cls, geometry_objects: List[BaseGeometry], name: str = "") -> MultipleComponents:
        """
        构造多个几何对象组成的列表

        `geometry_objects`: 需要组合的几何对象列表
        """
        return MultipleComponents(
            name=name,
            args=MultipleArgs(geometry_objects=geometry_objects)
        )
    
    @classmethod
    def FilteredMultiple(cls, geometry_objects: List[BaseGeometry], filter_func: Callable[[List[BaseGeometry]], List[bool]], name: str = "") -> MultipleComponents:
        """
        构造多个几何对象组成的列表，并根据过滤函数筛选

        `geometry_objects`: 需要组合的几何对象列表
        `filter_func`: 过滤函数，接受一个几何对象列表，并返回一个布尔值列表
        """
        return MultipleComponents(
            name=name,
            args=FilteredMultipleArgs(geometry_objects=geometry_objects, filter_func=filter_func)
        )
    
    @classmethod
    def FilteredMultipleMono(cls, geometry_objects: List[BaseGeometry], filter_func: Callable[[BaseGeometry], bool], name: str = "") -> MultipleComponents:
        """
        构造多个几何对象组成的列表，并根据单个过滤函数筛选

        `geometry_objects`: 需要组合的几何对象列表
        `filter_func`: 单个过滤函数，接受一个几何对象，并返回一个布尔值
        """
        return MultipleComponents(
            name=name,
            args=FilteredMultipleMonoArgs(geometry_objects=geometry_objects, filter_func=filter_func)
        )