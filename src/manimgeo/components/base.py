from __future__ import annotations

from typing import List, Tuple, Union

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
            dep.board_update_msg()

    def update(self):
        """执行当前对象的更新"""
        # 重新向适配器注入对象
        self.adapter(*self.objs)
        # 将参数从适配器绑定到几何对象
        self.adapter.bind_attributes(self, self.attrs)
        # 向下游广播更新信息
        self.board_update_msg()

# class LineLike(BaseGeometry, ABC):
#     """
#     ## 线类型

#     线类型具有 `_start` 和 `_end` 属性，表示线的起点和终点（或途径点），在此之上派生不同的几何构造。
#     """
#     _start: PointLike
#     _end: PointLike

#     def __init__(self, name: str = ""):
#         super().__init__(name)

#     @property
#     def start(self) -> PointLike:
#         """起点点"""
#         if self.ret_updated:
#             self._recalculate()
#             self.ret_updated = False
#         return self._start
    
#     @property
#     def end(self) -> PointLike:
#         """终点点"""
#         if self.ret_updated:
#             self._recalculate()
#             self.ret_updated = False
#         return self._end
    
#     @start.setter
#     def start(self, value: PointLike):
#         self.board_update_msg()
#         self._start = value

#     @end.setter
#     def end(self, value: PointLike):
#         self.board_update_msg()
#         self._end = value
    
#     def check_range(self, t: Union[int, float], epsilon: float=1e-7) -> bool:
#         """
#         线对象参数范围检查

#         不同线型具有的参数范围不同，通过 `check_range` 方法进行检查。
#         """
#         from manimgeo.components.lines import LineSegmentPP, RayPP, InfinityLinePP
#         if isinstance(self, LineSegmentPP):
#             return -epsilon <= t <= 1 + epsilon
#         elif isinstance(self, RayPP):
#             return t >= -epsilon
#         elif isinstance(self, InfinityLinePP):
#             return True
#         return False
    
#     def is_point_on_line(self, point: Union[PointLike, np.ndarray], epsilon: float=1e-7) -> bool:
#         """
#         判断点是否在线上
#         """
#         if isinstance(point, PointLike):
#             point = point.coord

#         line_dir = self._end - self._start
#         if np.allclose(line_dir, np.zeros_like(line_dir), atol=epsilon):
#             return np.allclose(point, self._start, atol=epsilon) and self.check_range(0)
        
#         vec = point - self._start
#         cross = np.cross(vec, line_dir)
#         if not np.isclose(cross, 0, atol=epsilon):
#             return False
        
#         t = np.dot(vec, line_dir) / np.dot(line_dir, line_dir)
#         return self.check_range(t)
    
    

#     def parametric(self, t: float) -> np.ndarray:
#         """参数方程"""
#         if not self.check_range(t):
#             raise ValueError("Invalid parameter t")
#         return self.start.coord + t*(self.end.coord - self.start.coord)

#     @abstractmethod
#     def _recalculate(self):
#         """重新计算"""
#         ...

