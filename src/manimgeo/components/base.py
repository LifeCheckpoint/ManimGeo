from __future__ import annotations

from ..utils import GeoUtils
from pydantic import BaseModel, Field
from typing import List, Union, Optional, Any
import logging

logger = logging.getLogger(__name__)

class GeometryAdapter(BaseModel):
    """几何对象参数适配器基类"""
    construct_type: str = Field(description="适配器计算构造方式")

    def bind_attributes(self, target: BaseGeometry, attrs: List[str]):
        """将适配器计算得到的参数绑定到几何对象"""
        for attr in attrs:
            if hasattr(self, attr):
                setattr(target, attr, getattr(self, attr))
            else:
                raise AttributeError(f"适配器缺少属性: {attr}")

    def __call__(self, *objs: Union[BaseGeometry, Any]):
        """根据 construct_type 规定的计算方法计算具体参数"""
        ...

class BaseGeometry(BaseModel):
    """几何对象基类"""
    name: str = Field(description="几何对象名称")
    attrs: List[str] = Field(default_factory=list, description="几何对象属性列表")
    adapter: GeometryAdapter = Field(description="几何对象参数适配器")
    objs: List[Union[BaseGeometry, Any]] = Field(default_factory=list, description="几何对象依赖的其他对象列表")
    dependents: List[BaseGeometry] = Field(default_factory=list, description="依赖于当前几何对象的其他几何对象列表")
    on_error: bool = Field(default=False, description="是否在更新过程中发生错误")

    def add_dependent(self, obj: BaseGeometry):
        """
        添加上游依赖对象
        
        - `obj`: 上游依赖对象
        """
        self.dependents.append(obj)

    def remove_dependent(self, obj: BaseGeometry):
        """
        删除上游依赖对象
        
        - `obj`: 需要删除的上游依赖对象
        """
        self.dependents.remove(obj)

    def board_update_msg(self, on_error: bool = False):
        """
        向所有依赖项发出更新信号
        
        - `on_error`: 是否在更新过程中发生错误，默认为 False
        """
        for dep in self.dependents:
            dep.update()
            dep.on_error = on_error

    def update(self, *new_objs: Optional[Union[BaseGeometry, Any]]):
        """
        执行当前对象的更新
        
        - `new_objs`: 如果在当前阶段引入了新的计算上游，则通过 `new_objs` 传入上游对象
        """

        if len(new_objs) != 0:
            self.objs = new_objs
        
        try:
            # 重新向适配器注入对象，适配器计算相关属性
            self.adapter(*self.objs)
            # 将参数从适配器绑定到几何对象
            self.adapter.bind_attributes(self, self.attrs)
            
        except Exception:
            if GeoUtils.GEO_PRINT_EXC:
                logger.warning(f"上游节点 {self.name} ({type(self).__name__}) 计算失败", exc_info=True)

            # 传播更新消息并标记错误
            self.board_update_msg(True)
            self.on_error = True
            return

        # 向下游广播更新信息
        self.board_update_msg()