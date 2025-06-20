from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict, ValidationError
from typing import List, Optional, Any, TypeVar, Generic
import logging

# 日志
logger = logging.getLogger(__name__)

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

    def bind_attributes(self, target: BaseGeometry, attrs: List[str]):
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

class BaseGeometry(BaseModel):
    """几何对象基类"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str = Field(description="几何对象名称")
    attrs: List[str] = Field(default_factory=list, description="几何对象属性列表", init=False)
    
    adapter: GeometryAdapter[Any] = Field(description="几何对象参数适配器", init=False)
    dependencies: List[BaseGeometry] = Field(default_factory=list, description="当前几何对象直接依赖的其他几何对象列表", init=False)
    dependents: List[BaseGeometry] = Field(default_factory=list, description="依赖于当前几何对象的其他几何对象列表", init=False)
    on_error: bool = Field(default=False, description="是否在更新过程中发生错误", init=False)

    def get_name(self, default_name: str):
        """以统一方式设置几何对象名称"""
        if default_name != "":
            return default_name
        else:
            return f"{type(self).__name__}[{self.adapter.construct_type}]@{id(self) % 100000}"

    def add_dependent(self, obj: BaseGeometry):
        """
        添加依赖于当前对象的下游对象
        
        - `obj`: 下游依赖对象
        """
        if obj not in self.dependents:
            self.dependents.append(obj)

    def remove_dependent(self, obj: Optional[BaseGeometry]):
        """
        移除依赖于当前对象的下游对象
        
        - `obj`: 需要移除的下游依赖对象，如果为 None 则移除所有依赖
        """
        if obj is None:
            self.dependents.clear()
        else:
            if obj in self.dependents:
                self.dependents.remove(obj)

    def _add_dependency(self, obj: BaseGeometry):
        """
        添加当前对象直接依赖的上游几何对象

        - `obj`: 上游依赖对象
        """
        if obj not in self.dependencies:
            self.dependencies.append(obj)
            obj.add_dependent(self) # 同时将当前对象添加到上游的 dependents 列表中

    def _remove_dependency(self, obj: Optional[BaseGeometry]):
        """
        移除当前对象直接依赖的上游几何对象

        - `obj`: 需要移除的上游依赖对象，如果为 None 则移除所有依赖
        """
        if obj is None:
            for dep in self.dependencies:
                dep.remove_dependent(self)
            self.dependencies.clear()
        else:
            if obj in self.dependencies:
                self.dependencies.remove(obj)
                obj.remove_dependent(self)

    def board_update_msg(self, on_error: bool = False):
        """
        向所有下游依赖项发出更新信号
        
        - `on_error`: 是否在更新过程中发生错误，默认为 False
        """
        for dep in self.dependents:
            dep.update() # 递归更新下游
            dep.on_error = on_error

    def update(self, new_args_model: Optional[BaseModel] = None):
        """
        执行当前对象的更新
        
        - `new_args_model`: 如果需要更新构造参数，则传入新的 Pydantic 参数模型实例。如果传入，会尝试替换 adapter.args
        """
        if new_args_model:
            try:
                # 检查传入的模型类型是否与当前适配器期望的 args 类型兼容
                # 简化的检查，更严格的检查可能需要比较 TypeVar ArgsModel
                if not isinstance(new_args_model, type(self.adapter.args)):
                    raise TypeError(f"传入的参数模型类型 {type(new_args_model).__name__} 与当前适配器期望的类型 {type(self.adapter.args).__name__} 不匹配。")
                
                self.adapter.args = new_args_model
            
            except (TypeError, ValidationError) as e:
                logger.error(f"更新对象 {self.name} 的参数失败: {e}")
                self.board_update_msg(True)
                self.on_error = True
                return
            
            except Exception as e:
                logger.error(f"更新对象 {self.name} 的参数时发生未知错误: {e}")
                self.board_update_msg(True)
                self.on_error = True
                return
        
        try:
            # 调用适配器进行计算
            self.adapter()
            # 将参数从适配器绑定到几何对象
            self.adapter.bind_attributes(self, self.attrs)
            
        except Exception as e:
            logger.warning(f"节点 {self.name} ({type(self).__name__}) 计算失败", exc_info=True)
            
            # 传播更新消息并标记错误
            self.board_update_msg(True)
            self.on_error = True
            return
        
        # 成功更新，清除错误标记
        self.on_error = False
        # 向下游广播更新信息
        self.board_update_msg()
