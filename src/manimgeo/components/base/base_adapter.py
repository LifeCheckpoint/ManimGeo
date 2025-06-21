from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from typing import TYPE_CHECKING, List, TypeVar, Generic

if TYPE_CHECKING:
    from .base_geometry import BaseGeometry

# 适配器的泛型参数模型
ArgsModel = TypeVar('ArgsModel', bound=BaseModel)

class GeometryAdapter(BaseModel, Generic[ArgsModel]):
    """几何对象参数适配器基类"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # 适配器直接持有参数模型
    args: ArgsModel = Field(description="适配器依赖的参数模型")

    @property
    def construct_type(self) -> str:
        # 所有 ArgsModel 都需要有一个 construct_type 字段
        return getattr(self.args, 'construct_type', 'Unknown')
    
    def __repr__(self):
        # 原始 BaseModel 的 __repr__ 方法开销巨大，改为简化输出
        return f"{self.__class__.__name__}(args={self.args})"
    
    def bind_attributes(self, target: "BaseGeometry", attrs: List[str]):
        """
        将适配器计算得到的参数绑定到几何对象

        - `target`: 目标几何对象
        - `attrs`: 需要绑定的属性列表
        """
        for attr in attrs:
            if hasattr(self, attr):
                setattr(target, attr, getattr(self, attr))
            else:
                # 如果 target 期望某个属性而适配器没有，则抛出异常
                raise AttributeError(f"适配器 '{self.__class__.__name__}' 缺少属性: '{attr}'，无法绑定到目标对象 '{target.name}'")

    def __call__(self):
        """根据 construct_type 规定的计算方法计算具体参数"""
        raise NotImplementedError("子类须实现 __call__ 以执行具体计算")
