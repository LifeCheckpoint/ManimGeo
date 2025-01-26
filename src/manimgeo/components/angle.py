from manimgeo.components.base import ParamLike, LineLike, PointLike
from typing import Union

# 使用弧度

class BaseAngle(ParamLike):
    """角度基类"""
    _angle: float

    @property
    def angle(self) -> float:
        """角度"""
        return self._angle
    
    @angle.setter
    def angle(self, value: float, name: str = ""):
        super().__init__(name)
        self.update()
        self._angle = value

    def _recalculate(self):
        # 定值角度本身不受参数影响，只需要更新依赖
        pass

class AngleLP(BaseAngle):
    """线段和基点类型角度"""
    line: LineLike
    base_point: PointLike

    def __init__(self, angle: Union[int, float], line: LineLike, base_point: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"AngleLP@{id(self)}")
        self._angle = angle
        self.line = line
        self.line.add_dependent(self)
        self.base_point = base_point
        self.base_point.add_dependent(self)

class AngleLL(BaseAngle):
    """两线段类型角度"""
    line1: LineLike
    line2: LineLike

    def __init__(self, angle: Union[int, float], line1: LineLike, line2: LineLike, name: str = ""):
        super().__init__(name if name is not "" else f"AngleLL@{id(self)}")
        self._angle = angle
        self.line1 = line1
        self.line2 = line2
        self.line1.add_dependent(self)
        self.line2.add_dependent(self)

class AnglePP(BaseAngle):
    """两点类型角度"""
    point1: PointLike
    point2: PointLike
    
    def __init__(self, angle: Union[int, float], point1: PointLike, point2: PointLike, name: str = ""):
        super().__init__(name if name is not "" else f"AnglePP@{id(self)}")
        self._angle = angle
        self.point1 = point1
        self.point2 = point2
        self.point1.add_dependent(self)
        self.point2.add_dependent(self)
