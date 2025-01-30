import numpy as np
from typing import TYPE_CHECKING, Union, Literal
from numbers import Number

from manimgeo.components.base import GeometryAdapter, BaseGeometry
from manimgeo.utils.utils import GeoUtils
from manimgeo.utils.mathe import GeoMathe

if TYPE_CHECKING:
    from manimgeo.components.point import Point

class LineAdapter(GeometryAdapter):
    start: np.ndarray
    end: np.ndarray
    length: np.ndarray
    unit_direction: np.ndarray

    def __init__(
            self,
            construct_type: Literal["PP"],
            current_geo_obj: Union["LineSegment", "Ray", "InfinityLine"],
            *objs: Union[BaseGeometry, any]
        ):
        """
        PP: 线上始终点
        """
        super().__init__(construct_type)

        [obj.add_dependent(current_geo_obj) for obj in objs if isinstance(obj, BaseGeometry)]

    def __call__(self, *objs: Union[BaseGeometry, any]):
        match self.construct_type:
            case "PP":
                GeoUtils.check_params(objs, Point, Point)
                self.start = objs[0].coord
                self.end = objs[1].coord
            
            case _:
                raise ValueError(f"Invalid constructing method: {self.construct_type}")
            
        self.length = np.linalg.norm(self.end - self.start)
        self.unit_direction = (self.end - self.start) / self.length

class Line(BaseGeometry):
    attrs = ["start", "end", "length", "unit_direction"]
    start: np.ndarray
    end: np.ndarray
    length: np.ndarray
    unit_direction: np.ndarray

    line_type: str

    def __init__(
            self, 
            construct_type: Literal["PP"],
            line_type: str,
            *objs,
            name: str = ""
        ):
        """通过指定构造方式与对象构造线"""
        super().__init__(GeoUtils.get_name(name, self, construct_type))
        self.line_type = line_type
        self.objs = objs
        self.adapter = LineAdapter(construct_type, self, *objs)
        self.update()

class LineSegment(Line):
    def __init__(
            self, 
            construct_type: Literal["PP"], 
            *objs, 
            name: str = ""
        ):
        """通过指定构造方式与对象构造线段"""
        super().__init__(construct_type, "LineSegment", *objs, name=name)

class Ray(Line):
    def __init__(
            self, 
            construct_type: Literal["PP"], 
            *objs, 
            name: str = ""
        ):
        """通过指定构造方式与对象构造射线"""
        super().__init__(construct_type, "Ray", *objs, name=name)

class InfinityLine(Line):
    def __init__(
            self, 
            construct_type: Literal["PP"], 
            *objs, 
            name: str = ""
        ):
        """通过指定构造方式与对象构造直线"""
        super().__init__(construct_type, "InfinityLine", *objs, name=name)

# Constructing Methods

def LineSegmentLL(start: Point, end: Point, name: str = ""):
    """
    ## 起始点构造线段

    `start`: 起点
    `end`: 终点
    """
    return LineSegment("PP", start, end, name=name)

def RayLL(start: Point, end: Point, name: str = ""):
    """
    ## 起始点构造射线

    `start`: 起点
    `end`: 终点
    """
    return Ray("PP", start, end, name=name)

def InfinityLineLL(start: Point, end: Point, name: str = ""):
    """
    ## 起始点构造直线

    `start`: 起点
    `end`: 终点
    """
    return InfinityLine("PP", start, end, name=name)