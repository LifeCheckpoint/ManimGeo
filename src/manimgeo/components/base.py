from __future__ import annotations

from typing import List, Union, Optional, Sequence
from ..utils import GeoUtils
import traceback

class GeometryAdapter:
    """几何对象参数适配器基类"""
    construct_type: str

    def __init__(self, construct_type: str):
        """通过指定构造方式初始化适配器"""
        self.construct_type = construct_type

    def bind_attributes(self, target: BaseGeometry, attrs: List[str]):
        """将指定的参数从适配器绑定到几何对象"""
        for attr in attrs:
            if hasattr(self, attr):
                setattr(target, attr, getattr(self, attr))
            else:
                raise AttributeError(f"Adapter missing required attribute: {attr}")

    def __call__(self, *objs):
        """根据 construct_type 计算参数"""
        ...

class BaseGeometry():
    """几何对象基类"""
    name: str
    attrs: List[str]
    adapter: GeometryAdapter
    objs: List[Union[BaseGeometry, any]]
    dependents: List[BaseGeometry]
    on_error: bool = False

    def __init__(self, name: str = "") -> None:
        self.name = name # 名称
        self.dependents = [] # 依赖对象列表
    
    def add_dependent(self, obj: BaseGeometry):
        """添加依赖对象"""
        self.dependents.append(obj)

    def remove_dependent(self, obj: BaseGeometry):
        """删除依赖对象"""
        self.dependents.remove(obj)

    def board_update_msg(self, on_error: bool = False):
        """向所有依赖项发出更新信号"""
        for dep in self.dependents:
            dep.update()
            dep.on_error = on_error

    def update(self, *new_objs: Optional[Union[BaseGeometry, any]]):
        """执行当前对象的更新"""

        if len(new_objs) != 0:
            self.objs = new_objs
        
        try:
            # 重新向适配器注入对象
            self.adapter(*self.objs)
            # 将参数从适配器绑定到几何对象
            self.adapter.bind_attributes(self, self.attrs)
            
        except AttributeError as e:
            if GeoUtils.GEO_PRINT_EXC:
                print(f"An error was occured at parent node. {self.name} ({type(self).__name__}) cannot be calculate")
        except Exception as e:
            if GeoUtils.GEO_PRINT_EXC:
                print(f"During calculating, an error occured at object {self.name} ({type(self).__name__})")
                traceback.print_exception(e)

            # 传播更新消息并标记错误
            self.board_update_msg(True)
            self.on_error = True
            return

        # 向下游广播更新信息
        self.board_update_msg()