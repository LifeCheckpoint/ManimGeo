from manimgeo.components.base import PointLike, LineLike
from manimgeo.utils.utils import GeoUtils

from typing import List, overload, Optional, Union
import numpy as np

class FreePoint(PointLike):
    """自由点类型（叶子节点）"""
    def __init__(self, coord: np.ndarray, name: str = ""):
        super().__init__(name)
        self.coord = coord

    def _recalculate(self):
        pass

class ImplicitPoint(PointLike):
    """隐式点类型（非叶子节点）"""
    def __init__(self, coord: np.ndarray, name: str = ""):
        super().__init__(name)
        self.coord = coord

    def _recalculate(self):
        pass

class MidPoint(PointLike):
    """中点类型（构造点）"""
    @overload
    def __init__(self, line: LineLike, name: str = ""):
        """构造线段的中点"""
        ...
    
    @overload
    def __init__(self, start: PointLike, end: PointLike, name: str = ""):
        """构造两点的中点"""
        ...
    
    def __init__(self, line_or_start: Union[LineLike, PointLike], end: Optional[PointLike] = None, name: str = ""):
        super().__init__(name)
        from manimgeo.components.lines import LineSegment  # 延迟导入

        if isinstance(line_or_start, LineSegment) and end is None:
            line = line_or_start
            self.start = line.start
            self.end = line.end
            parents = [self.start, self.end]
        elif end is not None and isinstance(line_or_start, PointLike):
            self.start = line_or_start
            self.end = end
            parents = [self.start, self.end]
        else:
            raise ValueError("Invalid input arguments")

        for parent in parents:
            parent.add_dependent(self)

    def _recalculate(self):
        self.coord = (self.start.coord + self.end.coord) / 2

class ExtensionPoint(PointLike):
    """延长点类型"""
    def __init__(self, start: PointLike, end: PointLike, factor: float = 2.0, name: str = ""):
        super().__init__(name)
        self.factor = factor
        self.start = start
        self.end = end
        
        self.start.add_dependent(self)
        self.end.add_dependent(self)

    def _recalculate(self):
        self.coord = self.start.coord + self.factor*(self.end.coord - self.start.coord)

class IntersectionPoint(PointLike):
    """交点"""
    def __init__(self, line1: LineLike, line2: LineLike, name: str = ""):
        super().__init__(name)
        self.line1 = line1
        self.line2 = line2
        
        self.line1.add_dependent(self)
        self.line2.add_dependent(self)

    def _recalculate(self):
        has_intersection, res = LineLike.find_intersection(self.line1, self.line2)
        if has_intersection:
            self.coord = res[0]
        else:
            raise ValueError("No intersection found")