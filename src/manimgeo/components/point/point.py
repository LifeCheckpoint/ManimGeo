from __future__ import annotations

from ...utils.utils import GeoUtils
from pydantic import Field, validate_call
from typing import TYPE_CHECKING, Any, List
import numpy as np

from ..base import BaseGeometry
from .adapter import PointAdapter
from .construct import *

if TYPE_CHECKING:
    from ..angle import Angle
    from ..line import Line, LineSegment
    from ..vector import Vector
    from ..circle import Circle

class Point(BaseGeometry):
    attrs: List[str] = Field(default=["coord"], description="点属性列表", init=False)
    coord: np.ndarray = Field(default=np.zeros(2), description="点坐标", init=False)
    args: PointConstructArgs = Field(discriminator='construct_type', description="点构造参数")
    
    @property
    def construct_type(self) -> PointConstructType:
        return self.args.construct_type
    
    def model_post_init(self, __context: Any):
        """模型初始化后，更新名字并添加依赖关系"""
        # 实例化 PointAdapter，传入 PointConstructArgs
        self.adapter = PointAdapter(args=self.args)
        self.name = GeoUtils.get_name(self.name, self, self.construct_type)

        # 遍历 args 模型中的所有 BaseGeometry 实例，并添加到 _dependencies
        # 普通类型将被忽略
        for field_name, field_info in self.args.__class__.model_fields.items():
            field_value = getattr(self.args, field_name)
            
            # 基本几何对象
            if isinstance(field_value, BaseGeometry):
                self._add_dependency(field_value)

            # 列表类型依赖 (extended)
            elif isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, BaseGeometry):
                        self._add_dependency(item)
        
            # 可拓展

        self.update() # 首次计算
    
    def set_coord(self, coord: np.ndarray):
        """
        更新 `PointFree` 或 `PointConstraint` 坐标
        坐标设置仅对于 Free 构造有效，其他构造类型将抛出 ValueError
        """
        if self.construct_type not in ["Free"]:
            raise ValueError(f"不可设置非 FreePoint 点坐标 (当前构造类型: {self.construct_type})")
        
        new_args = FreeArgs(coord=coord)
        self.update(new_args)

    # 构造方法
    
    @staticmethod
    @validate_call
    def Free(coord: np.ndarray, name: str = "") -> Point:
        """
        构造自由点（叶子节点）

        `coord`: 点坐标
        """
        return Point(
            name=name,
            args=FreeArgs(coord=coord)
        )
    
    @staticmethod
    @validate_call
    def Constraint(coord: np.ndarray, name: str = "") -> Point:
        """
        构造约束点（非叶子节点）

        `coord`: 坐标
        """
        return Point(
            name=name,
            args=ConstraintArgs(coord=coord)
        )

    @staticmethod
    @validate_call
    def MidPP(point1: Point, point2: Point, name: str = "") -> Point:
        """
        构造两点中点

        `point1`: 第一个点  
        `point2`: 第二个点
        """
        return Point(
            name=name,
            args=MidPPArgs(point1=point1, point2=point2)
        )
    
    @staticmethod
    @validate_call
    def MidL(line: LineSegment, name: str = "") -> Point:
        """
        构造线段中点

        `line`: 线段对象
        """
        return Point(
            name=name,
            args=MidLArgs(line=line)
        )
    
    @staticmethod
    @validate_call
    def ExtensionPP(start: Point, through: Point, factor: Number, name: str = "") -> Point:
        """
        构造比例延长（位似）点

        `start`: 起点  
        `through`: 经过点  
        `factor`: 延长比例, 1 为恒等延长
        """
        return Point(
            name=name,
            args=ExtensionPPArgs(start=start, through=through, factor=factor)
        )
    
    @staticmethod
    @validate_call
    def AxisymmetricPL(point: Point, line: Line, name: str = "") -> Point:
        """
        构造轴对称点

        `point`: 原始点  
        `line`: 对称轴线
        """
        return Point(
            name=name,
            args=AxisymmetricPLArgs(point=point, line=line)
        )
    
    @staticmethod
    @validate_call
    def VerticalPL(point: Point, line: Line, name: str = "") -> Point:
        """
        构造垂足点

        `point`: 原始基准点  
        `line`: 目标直线
        """
        return Point(
            name=name,
            args=VerticalPLArgs(point=point, line=line)
        )
    
    @staticmethod
    @validate_call
    def ParallelPL(point: Point, line: Line, distance: Number, name: str = "") -> Point:
        """
        构造平行线上一点

        `point`: 基准点  
        `line`: 平行基准线  
        `distance`: 沿平行方向的绝对距离
        """
        return Point(
            name=name,
            args=ParallelPLArgs(point=point, line=line, distance=distance)
        )
    
    @staticmethod
    @validate_call
    def InversionPCir(point: Point, circle: Circle, name: str = "") -> Point:
        """
        构造反演点

        `point`: 原始点  
        `circle`: 反演基准圆
        """
        return Point(
            name=name,
            args=InversionPCirArgs(point=point, circle=circle)
        )
    
    @staticmethod
    @validate_call
    def IntersectionLL(line1: Line, line2: Line, regard_infinite: bool = False, name: str = "") -> Point:
        """
        构造两线交点

        `line1`: 第一条线  
        `line2`: 第二条线  
        `regard_infinite`: 是否视为无限长直线
        """
        return Point(
            name=name,
            args=IntersectionLLArgs(line1=line1, line2=line2, regard_infinite=regard_infinite)
        )
    
    @staticmethod
    @validate_call
    def TranslationPV(point: Point, vector: Vector, name: str = "") -> Point:
        """
        构造平移点

        `point`: 原始点  
        `vector`: 平移向量
        """
        return Point(
            name=name,
            args=TranslationPVArgs(point=point, vector=vector)
        )
    
    @staticmethod
    @validate_call
    def CentroidPPP(point1: Point, point2: Point, point3: Point, name: str = "") -> Point:
        """
        构造三角形重心

        `point1`: 第一个顶点  
        `point2`: 第二个顶点  
        `point3`: 第三个顶点
        """
        return Point(
            name=name,
            args=CentroidPPPArgs(point1=point1, point2=point2, point3=point3)
        )
    
    @staticmethod
    @validate_call
    def CircumcenterPPP(point1: Point, point2: Point, point3: Point, name: str = "") -> Point:
        """
        构造三角形外心

        `point1`: 第一个顶点  
        `point2`: 第二个顶点  
        `point3`: 第三个顶点
        """
        return Point(
            name=name,
            args=CircumcenterPPPArgs(point1=point1, point2=point2, point3=point3)
        )
    
    @staticmethod
    @validate_call
    def IncenterPPP(point1: Point, point2: Point, point3: Point, name: str = "") -> Point:
        """
        构造三角形内心

        `point1`: 第一个顶点  
        `point2`: 第二个顶点  
        `point3`: 第三个顶点
        """
        return Point(
            name=name,
            args=IncenterPPPArgs(point1=point1, point2=point2, point3=point3)
        )
    
    @staticmethod
    @validate_call
    def OrthocenterPPP(point1: Point, point2: Point, point3: Point, name: str = "") -> Point:
        """
        构造三角形垂心

        `point1`: 第一个顶点  
        `point2`: 第二个顶点  
        `point3`: 第三个顶点
        """
        return Point(
            name=name,
            args=OrthocenterPPPArgs(point1=point1, point2=point2, point3=point3)
        )
    
    @staticmethod
    @validate_call
    def Cir(circle: Circle, name: str = "") -> Point:
        """
        构造圆心

        `circle`: 圆对象
        """
        return Point(
            name=name,
            args=CirArgs(circle=circle)
        )
    
    @staticmethod
    @validate_call
    def RotatePPA(point: Point, center: Point, angle: Angle, name: str = "") -> Point:
        """
        构造旋转点

        `point`: 原始点  
        `center`: 旋转中心  
        `angle`: 旋转角度
        """
        return Point(
            name=name,
            args=RotatePPAArgs(point=point, center=center, angle=angle)
        )