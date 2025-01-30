from __future__ import annotations

import numpy as np
from typing import TYPE_CHECKING, Union, Literal
from numbers import Number

from manimgeo.components.base import GeometryAdapter, BaseGeometry
from manimgeo.utils.utils import GeoUtils
from manimgeo.utils.mathe import GeoMathe

if TYPE_CHECKING:
    from manimgeo.components.point import Point

EllipseConstructType = Literal[
    "XY", "NXY", "CE", "NCE"
]

class EllipseAdapter(GeometryAdapter):
    center: np.array
    half_x_a: Number
    half_y_b: Number
    focus_c: Number
    eccentricity: Number

    def __init__(
            self, 
            construct_type: EllipseConstructType, 
            current_geo_obj: "Ellipse", 
            *objs: Union[BaseGeometry, any]
        ):
        """
        XY: 两个半轴轴点构造椭圆
        NXY: 两个半轴（数值）构造椭圆
        CE: 焦点离心率构造椭圆
        NCE: 焦距（数值）离心率构造椭圆
        """
        super().__init__(construct_type)

        # 添加依赖
        [obj.add_dependent(current_geo_obj) for obj in objs if isinstance(obj, BaseGeometry)]

    def __call__(self, *objs: Union[BaseGeometry, any]):
        from manimgeo.components.point import Point

        op_type_map = {
            "XY": [Point, Point, Point],
            "NXY": [Point, Number, Number],
            "CE": [Point, Point, Number],
            "NCE": [Point, Number, Number, str] # c, e, focus_on ("x" or "y")
        }
        GeoUtils.check_params_batch(op_type_map, self.construct_type, objs)

        def valid_point_axis(center: np.ndarray, x_a: np.ndarray, y_b: np.ndarray):
            if np.allclose(center, x_a) or np.allclose(center, y_b) or np.allclose(x_a, y_b):
                return False
            if np.allclose(center[1], x_a[1]) and np.allclose(center[0], y_b[0]):
                return True
            return False

        match self.construct_type:
            case "XY":
                if not valid_point_axis(objs[0].coord, objs[1].coord, objs[2].coord):
                    raise ValueError("Invalid axis point")
                self.center = objs[0].coord
                self.half_x_a = (objs[1].coord - objs[0].coord)[0]
                self.half_y_b = (objs[2].coord - objs[0].coord)[1]

            case "NXY":
                self.center = objs[0].coord
                self.half_x_a = objs[1]
                self.half_y_b = objs[2]

            case "CE":
                dx = objs[1].coord[0] - objs[0].coord[0]
                dy = objs[1].coord[1] - objs[0].coord[1]
                c = dx if np.allclose(dy, 0) else dy
                if not np.allclose(objs[0].coord[0], objs[1].coord[0]) or not np.allclose(objs[0].coord[1], objs[1].coord[1]):
                    raise ValueError("Invalid focus point")
                self.center = objs[0].coord
                self.half_x_a = c / objs[2]
                self.half_y_b = np.sqrt(self.half_x_a**2 - c**2)

            case "NCE":
                # TODO
                pass

class Ellipse(BaseGeometry):
    attrs = ["center", "half_x_a", "half_y_b", "focus_c", "eccentricity"]
    center: np.array
    half_x_a: Number
    half_y_b: Number
    focus_c: Number
    eccentricity: Number

    def __init__(self, construct_type: EllipseConstructType, *objs, name: str = ""):
        """通过指定构造方式与对象构造椭圆"""
        super().__init__(GeoUtils.get_name(name, self, construct_type))
        self.objs = objs
        self.adapter = EllipseAdapter(construct_type, self, *objs)
        self.update()

# Constructing Methods

def EllipseXY(center: Point, X_axis_point: Point, Y_axis_point: Point, name: str = ""):
    """
    ## 轴点构造椭圆

    `center`: 椭圆中心点
    `X_axis_point`: 椭圆长轴端点
    `Y_axis_point`: 椭圆短轴端点
    """
    return Ellipse("XY", center, X_axis_point, Y_axis_point, name=name)

def EllipseNXY(center: Point, half_x_a: Number, half_y_b: Number, name: str = ""):
    """
    ## 数值构造椭圆

    `center`: 椭圆中心点
    `half_x_a`: 椭圆长轴半长度
    `half_y_b`: 椭圆短轴半长度
    """
    return Ellipse("NXY", center, half_x_a, half_y_b, name=name)

def EllipseCE(center: Point, focus: Point, eccentricity: Number, name: str = ""):
    """
    ## 离心率构造椭圆

    `center`: 椭圆中心点
    `focus`: 椭圆焦点
    `eccentricity`: 椭圆离心率
    """
    return Ellipse("CE", center, focus, eccentricity, name=name)

def EllipseNCE(center: Point, focus_c: Number, eccentricity: Number, focus_on: str = "x", name: str = ""):
    """
    ## 数值离心率构造椭圆

    `center`: 椭圆中心点
    `focus_c`: 椭圆焦距
    `eccentricity`: 椭圆离心率
    `focus_on`: 焦点在x轴还是y轴
    """
    return Ellipse("NCE", center, focus_c, eccentricity, focus_on, name=name)
