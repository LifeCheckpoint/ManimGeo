from __future__ import annotations

from .base_pydantic import BaseModelN
from pydantic import Field
from typing import List, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .base_geometry import BaseGeometry

# 适配器的泛型参数模型
class ArgsModelBase(BaseModelN):
    """适配器参数模型基类"""
    construct_type: str = Field(description="适配器计算方法类型")
    
    def _get_deps(self) -> List[BaseGeometry]:
        """
        获取参数模型声明的依赖几何对象列表

        例如，参数模型有可能包含多个 `BaseGeometry` 对象：

        ```python
        class SomeConstruct(BaseModelN):
            construct_type: Literal["PPPO"] = "PPPO"
            start: Point
            center: Point
            end: Point
            other: List[BaseGeometry]
        ```

        默认情况下，该方法会遍历适配器的所有字段，检查是否为
         - `BaseGeometry` 或其子类实例
         - `List`，并包含 `BaseGeometry` 实例，

        并返回这些对象。如果需要实现更复杂的依赖关系提取逻辑，子类需要重写此方法以返回其依赖的几何对象
        """
        dep_objects: List[BaseGeometry] = []

        for field_name, field_info in self.__class__.model_fields.items():
            field_value = getattr(self, field_name)
            
            # 基本几何对象
            if isinstance(field_value, BaseGeometry):
                dep_objects.append(field_value)

            # 列表类型依赖
            elif isinstance(field_value, List):
                for item in field_value:
                    if isinstance(item, BaseGeometry):
                        dep_objects.append(item)

        return dep_objects

_ArgsModelT = TypeVar('_ArgsModelT', bound=ArgsModelBase)