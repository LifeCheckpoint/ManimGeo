from manimgeo.components.base import PointLike, LineLike
from manimgeo.utils.utils import GeoUtils

import numpy as np

class LineSegmentPP(LineLike):
    """线段类型（两点）"""
    def __init__(self, start: PointLike, end: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"LineSegment@{id(self)}")

        if np.allclose(start.coord, end.coord):
            raise ValueError(f"For line {self.name}, Points {start.name} and {end.name} causing degenerating")
        
        self.start = start
        self.end = end

        # 线段依赖端点
        self.start.add_dependent(self)
        self.end.add_dependent(self)

    def _recalculate(self):
        # 几何依赖自动更新，无需重算
        pass

class RayPP(LineLike):
    """射线类型（两点）"""
    def __init__(self, start: PointLike, end: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"RayPP@{id(self)}")

        if np.allclose(start.coord, end.coord):
            raise ValueError(f"For line {self.name}, Points {start.name} and {end.name} causing degenerating")
        
        self.start = start
        self.end = end

        # 线段依赖端点
        self.start.add_dependent(self)
        self.end.add_dependent(self)

    def _recalculate(self):
        # 几何依赖自动更新，无需重算
        pass

class InfinityLinePP(LineLike):
    """直线类型（两点）"""
    
    def __init__(self, start: PointLike, end: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"InfinityLinePP@{id(self)}")

        if np.allclose(start.coord, end.coord):
            raise ValueError(f"For line {self.name}, Points {start.name} and {end.name} causing degenerating")

        self.start = start
        self.end = end

        # 无穷直线依赖端点
        self.start.add_dependent(self)
        self.end.add_dependent(self)

    def _recalculate(self):
        # 几何依赖自动更新，无需重算
        pass
