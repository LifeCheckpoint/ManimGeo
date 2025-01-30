from __future__ import annotations

from typing import List, Union

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

    def __init__(self, name: str = "") -> None:
        self.name = name # 名称
        self.dependents = [] # 依赖对象列表
    
    def add_dependent(self, obj: BaseGeometry):
        """添加依赖对象"""
        self.dependents.append(obj)

    def board_update_msg(self):
        """向所有依赖项发出更新信号"""
        for dep in self.dependents:
            dep.update()

    def update(self):
        """执行当前对象的更新"""
        # 重新向适配器注入对象
        self.adapter(*self.objs)
        # 将参数从适配器绑定到几何对象
        self.adapter.bind_attributes(self, self.attrs)
        # 向下游广播更新信息
        self.board_update_msg()

    def update_by(self, *new_objs):
        """开洞更新，用于叶子节点"""
        # 重新向适配器注入对象
        self.adapter(*new_objs)
        self.objs = new_objs
        # 将参数从适配器绑定到几何对象
        self.adapter.bind_attributes(self, self.attrs)
        # 向下游广播更新信息
        self.board_update_msg()