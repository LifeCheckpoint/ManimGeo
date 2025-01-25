from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, List, Tuple
import numpy as np

@runtime_checkable
class DependentObject(Protocol):
    """依赖更新协议"""
    def update(self) -> None:
        ...
    
    def add_dependent(self, obj: 'DependentObject') -> None:
        """
        在 add_dependent 中添加依赖关系时， obj1.add_dependent(obj2) 会使 obj2 依赖于 obj1，即 obj2 随着 obj1 的变化而更新。
        """

class BaseGeometry(DependentObject):
    """几何对象基类"""
    def __init__(self, name: str = "") -> None:
        self._name = name # 名称
        self.dependents: list[DependentObject] = [] # 依赖对象列表

        """懒更新的对象数据"""
        self.ret_updated = True # 返回值 lazy tag
        self.ret_data = None # 返回值
    
    @property
    def name(self) -> str:
        """返回几何对象的名称"""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    def add_dependent(self, obj: DependentObject):
        """添加依赖对象"""
        self.dependents.append(obj)

    def update(self):
        """向更新所有依赖项发出更新信号"""
        self.ret_updated = True  # 标记返回值失效
        for dep in self.dependents:
            dep.update()

class PointLike(BaseGeometry, ABC):
    """点类型协议"""
    ret_data: np.ndarray

    def __init__(self, name: str = ""):
        super().__init__(name)
        self.ret_data = np.zeros(2)

    @property
    def coord(self) -> np.ndarray:
        """点坐标"""
        if self.ret_updated:
            self._recalculate()
            self.ret_updated = False
        return self.ret_data.copy()
    
    @coord.setter
    def coord(self, value: np.ndarray):
        self.update()
        self.ret_data = value.copy()

    @abstractmethod
    def _recalculate(self):
        """重新计算"""
        ...

class LineLike(BaseGeometry, ABC):
    """线类型协议"""
    ret_data: tuple[np.ndarray, np.ndarray]

    def __init__(self, name: str = ""):
        super().__init__(name)
        self.ret_data = (np.zeros(2), np.zeros(2))

    @property
    def direction(self) -> np.ndarray:
        """单位方向向量"""
        if self.ret_updated:
            self._recalculate()
            self.ret_updated = False
        return self.ret_data[0].copy()
    
    @property
    def base_point(self) -> np.ndarray:
        """基点坐标"""
        if self.ret_updated:
            self._recalculate()
            self.ret_updated = False
        return self.ret_data[1].copy()
    
    @direction.setter
    def direction(self, value: np.ndarray):
        self.update()
        self.ret_data = (value.copy(), self.ret_data[1].copy())

    @base_point.setter
    def base_point(self, value: np.ndarray):
        self.update()
        self.ret_data = (self.ret_data[0].copy(), value.copy())
    
    def check_range(self, t, epsilon=1e-7) -> bool:
        """线对象参数范围检查"""
        from manimgeo.components.lines import LineSegment, Ray, InfinityLine
        if isinstance(self, LineSegment):
            return -epsilon <= t <= 1 + epsilon
        elif isinstance(self, Ray):
            return t >= -epsilon
        elif isinstance(self, InfinityLine):
            return True
        return False
    
    def is_point_on_line(self, point, epsilon=1e-7) -> bool:
        line_dir = self._though - self._start
        if np.allclose(line_dir, np.zeros_like(line_dir), atol=epsilon):
            return np.allclose(point, self._start, atol=epsilon) and self.check_range(0)
        
        vec = point - self._start
        cross = np.cross(vec, line_dir)
        if not np.isclose(cross, 0, atol=epsilon):
            return False
        
        t = np.dot(vec, line_dir) / np.dot(line_dir, line_dir)
        return self.check_range(t)
    
    @staticmethod
    def find_intersection(line1: LineLike, line2: LineLike, infinty: bool = False) -> Tuple[bool, List[np.ndarray]]:
        """
        计算两条线的交点
        对于单个交点，返回值为 (has_intersection, [intesection_point])
        对于无穷多交点，返回值为端点  (has_intersection, [intesection_points])
        """
        from manimgeo.components.lines import LineSegment, Ray, InfinityLine
        epsilon = 1e-7
        points = []

        p1: np.ndarray = line1._start.coord
        p2: np.ndarray = line1._through.coord
        q1: np.ndarray = line2._start.coord
        q2: np.ndarray = line2._through.coord

        u = p2 - p1
        v = q2 - q1
        diff = q1 - p1

        cross = np.cross(u, v)
        sqrlen_u = np.dot(u, u)
        sqrlen_v = np.dot(v, v)

        # 处理退化的线
        line1_degenerate = np.allclose(u, 0, atol=epsilon)
        line2_degenerate = np.allclose(v, 0, atol=epsilon)

        # 双点退化情况
        if line1_degenerate and line2_degenerate:
            if np.allclose(p1, q1, atol=epsilon):
                return True, [p1.copy()]
            return False, []

        # 单线退化处理
        if infinty and (line1_degenerate or line2_degenerate):
            return (False, [])
        
        if line1_degenerate:
            on_line = line2.is_point_on_line(p1, epsilon)
            return (on_line, [p1.copy()]) if on_line else (False, [])
        if line2_degenerate:
            on_line = line1.is_point_on_line(q1, epsilon)
            return (on_line, [q1.copy()]) if on_line else (False, [])

        # 非平行情况处理
        if abs(cross) > epsilon * np.sqrt(sqrlen_u * sqrlen_v):
            w = q1 - p1
            t = np.cross(w, v) / cross
            s = -np.cross(u, w) / cross

            if (line1.check_range(t) and line2.check_range(s)) or infinty:
                intersection = p1 + t * u
                return True, [intersection]
            return False, []

        # 平行情况处理
        if not np.isclose(np.cross(diff, u), 0, atol=epsilon):
            return False, []

        # 共线时的投影参数计算
        def get_projection(line: LineLike, ref_line: LineLike) -> Tuple[float, float]:
            ref_dir = ref_line._through - ref_line._start
            sqrlen_ref = np.dot(ref_dir, ref_dir)
            if sqrlen_ref < epsilon:
                return (0.0, 0.0) if np.allclose(line._start, ref_line._start, atol=epsilon) else (np.nan, np.nan)

            vec_start = line._start - ref_line._start
            vec_end = line._through - ref_line._start
            t_start = np.dot(vec_start, ref_dir) / sqrlen_ref
            t_end = np.dot(vec_end, ref_dir) / sqrlen_ref

            if isinstance(line, LineSegment):
                return sorted([t_start, t_end])
            elif isinstance(line, Ray):
                dir_dot = np.dot(line._through - line._start, ref_dir)
                return (t_start, np.inf) if dir_dot > 0 else (-np.inf, t_start)
            else:  # InfinityLine
                return (-np.inf, np.inf)

        # 获取两条线在参考线上的投影范围
        ref_line = line1
        line1_t = (0.0, 1.0) if isinstance(line1, LineSegment) else \
                 (0.0, np.inf) if isinstance(line1, Ray) else \
                 (-np.inf, np.inf)

        line2_t = get_projection(line2, ref_line)
        if np.isnan(line2_t[0]):
            return False, []

        # 计算有效重叠区间
        lower = max(line1_t[0], line2_t[0])
        upper = min(line1_t[1], line2_t[1])
        if lower > upper + epsilon:
            return False, []

        # 生成交点坐标
        if abs(lower - upper) < epsilon:  # 单点接触
            point = ref_line._start + lower * (ref_line._through - ref_line._start)
            return True, [point]
        else:  # 区间重叠
            points = []
            for t in [lower, upper]:
                if not np.isinf(t):
                    points.append(ref_line._start + t * (ref_line._through - ref_line._start))
            return True, points

    @abstractmethod
    def parametric(self, t: float) -> np.ndarray:
        """参数方程"""
        ...

    @abstractmethod
    def _recalculate(self):
        """重新计算"""
        ...

class ParametricGeometry(BaseGeometry, ABC):
    """参数几何图形对象"""
    def __init__(self, name: str = ""):
        super().__init__(name)
        self.ret_data = None

    @property
    def data(self) -> np.ndarray:
        if self.ret_updated:
            self._recalculate()
            self.ret_updated = False
        return self.ret_data
    
    @data.setter
    def data(self, value: np.ndarray):
        self.update()
        self.ret_data = value

    @abstractmethod
    def parametric(self, t: float) -> np.ndarray:
        """参数方程"""
        ...

    @abstractmethod
    def _recalculate(self):
        """重新计算"""
        ...