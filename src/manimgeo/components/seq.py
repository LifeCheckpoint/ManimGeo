from manimgeo.components.base import BaseGeometry
from manimgeo.utils.output import *
from typing import List, NoReturn

def flatten(iterable):
    for item in iterable:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

def GeometrySequence(operations: List[BaseGeometry], name: str = "") -> NoReturn:
    """几何操作序列容器标记"""
    name = name if name is not "" else f"Sequence@{id(operations)}"

    color = generate_simple_color()

    # 为每个组件加上归属管理后缀
    for op in flatten(operations):
        op: BaseGeometry
        op.name = f"[{op.name}]{color_text(name, *color)}"

# 组合几何方法
from manimgeo.components.angle import *
from manimgeo.components.base import *
from manimgeo.components.conic_section import *
from manimgeo.components.lines import *
from manimgeo.components.points import *
from manimgeo.components.vector import *

def VerticalInfinieLinePL(point: PointLike, line: LineLike, name: str = "") -> Tuple[InfinityLinePP, List[BaseGeometry]]:
    """
    ## 作过一点垂直线
    
    return: InfinityLinePP, [LineDirection, TranslationPoint, VerticalPoint, InfinityLinePP]
    """
    direction = VectorPP(line.start, line.end, f"LineDirection")
    trans_point = TranslationPoint(point, direction, f"TranslationPoint")
    vertical_point = RotationPoint(trans_point, point, AnglePP(np.pi/2, point, trans_point), f"VerticalPoint")
    inf_line = InfinityLinePP(point, vertical_point, f"InfinityLine")
    
    GeometrySequence([direction, trans_point, vertical_point, inf_line], name)
    return inf_line, [direction, trans_point, vertical_point, inf_line]

def PerpendicularBisectorInfiniteLinePP(point1: PointLike, point2: PointLike, name: str = "") -> Tuple[InfinityLinePP, List[BaseGeometry]]:
    """
    ## 作两点中垂线

    return: InfinityLinePP, [MidPointPP, InfinityLinePP, InfinityLinePP, *VerticalInfinieLinePL] 
    """
    mid_point = MidPointPP(point1, point2, f"MidPoint")
    line = InfinityLinePP(point1, point2, f"InfiniteLine")
    inf_line, ops = VerticalInfinieLinePL(mid_point, line, f"VerticalInfiniteLine")

    GeometrySequence([mid_point, line, inf_line, ops], name)
    return inf_line, [mid_point, line, inf_line, ops]

def CentroidPPP(point1: PointLike, point2: PointLike, point3: PointLike, name: str = "") -> Tuple[IntersectionPointLL, List[BaseGeometry]]:
    """
    ## 三点重心

    return: IntersectionPointLL, [MidPointPP, MidPointPP, InfinityLinePP, InfinityLinePP, IntersectionPointLL]
    """
    mid_12 = MidPointPP(point1, point2, f"MD12")
    mid_23 = MidPointPP(point2, point3, f"MD13")
    line_mid_12 = InfinityLinePP(point3, mid_12, "LMD3-12")
    line_mid_23 = InfinityLinePP(point1, mid_23, "LMD1-23")
    intersection = IntersectionPointLL(line_mid_12, line_mid_23, "Centroid")

    GeometrySequence([mid_12, mid_23, line_mid_12, line_mid_23, intersection], name)
    return intersection, [mid_12, mid_23, line_mid_12, line_mid_23, intersection]

def CircumcenterPPP(point1: PointLike, point2: PointLike, point3: PointLike, name: str = "") -> Tuple[IntersectionPointLL, List[BaseGeometry]]:
    """
    ## 三点外心

    return: IntersectionPointLL, [InfiniteLinePP, *PerpendicularBisectorInfiniteLinePP, InfiniteLinePP, *PerpendicularBisectorInfiniteLinePP, IntersectionPointLL]
    """
    pb_12, ops1 = PerpendicularBisectorInfiniteLinePP(point1, point2, f"PBInfiniteLine 12")
    pb_23, ops2 = PerpendicularBisectorInfiniteLinePP(point2, point3, f"PBInfiniteLine 23")
    intersection = IntersectionPointLL(pb_12, pb_23, "Circumcenter")

    GeometrySequence([pb_12, ops1, pb_23, ops2, intersection], name)
    return intersection, [pb_12, ops1, pb_23, ops2, intersection]

def CircumcenterCirPPP(circle: CirclePPP, name: str = "") -> Tuple[IntersectionPointLL, List[BaseGeometry]]:
    """
    ## 外接圆三点圆心

    see also `CircumcenterPPP`
    """
    return CircumcenterPPP(circle.point1, circle.point2, circle.point3, name)

# def AngleBisectorLL(line1: LineLike, line2: LineLike, name: str = "") -> Tuple[InfinityLinePP, List[BaseGeometry]]:
#     """
#     ## 两线角平分线
    
#     return: InfinityLinePP, [IntersectionPointLL, RotationPoint, InfinityLinePP]
#     """
#     intersection = IntersectionPointLL(line1, line2, f"Intersection")
#     direction1 = VectorPP(intersection, line1.end, f"Direction1")
#     direction2 = VectorPP(intersection, line2.end, f"Direction2")
#     bisector_direction = RotationPoint(direction2.end, intersection, AnglePP(np.pi/2, intersection, direction1.end), f"BisectorDirection")
#     inf_line = InfinityLinePP(intersection, bisector_direction, f"InfinityLine")

#     GeometrySequence([intersection, direction1, direction2, bisector_direction, inf_line], name)
#     return inf_line, [intersection, direction1, direction2, bisector_direction, inf_line]

# def IncenterPPP(point1: PointLike, point2: PointLike, point3: PointLike, name: str = "") -> Tuple[IntersectionPointLL, List[BaseGeometry]]:
#     """
#     ## 三点内心
    
#     return: IntersectionPointLL, [LineLike, LineLike, *AngleBisectorLL, LineLike, LineLike, *AngleBisectorLL, IntersectionPointLL]
#     """
#     line12 = LineSegmentPP(point1, point2, f"Line12")
#     line23 = LineSegmentPP(point2, point3, f"Line23")
#     bisector12, ops1 = AngleBisectorLL(line12, line23, f"Bisector12")
#     line31 = LineSegmentPP(point3, point1, f"Line31")
#     bisector23, ops2 = AngleBisectorLL(line23, line31, f"Bisector23")
#     intersection = IntersectionPointLL(bisector12, bisector23, "Incenter")

#     GeometrySequence([line12, line23, bisector12, ops1, line31, bisector23, ops2, intersection], name)
#     return intersection, [line12, line23, bisector12, ops1, line31, bisector23, ops2, intersection]

def OrthocenterPPP(point1: PointLike, point2: PointLike, point3: PointLike, name: str = "") -> Tuple[IntersectionPointLL, List[BaseGeometry]]:
    """
    ## 三点垂心
    
    return: IntersectionPointLL, [InfinityLinePP, *VerticalInfinieLinePL, InfinityLinePP, *VerticalInfinieLinePL, IntersectionPointLL]
    """
    line12 = InfinityLinePP(point1, point2, f"Line12")
    altitude3, ops1 = VerticalInfinieLinePL(point3, line12, f"Altitude3")
    line23 = InfinityLinePP(point2, point3, f"Line23")
    altitude1, ops2 = VerticalInfinieLinePL(point1, line23, f"Altitude1")
    intersection = IntersectionPointLL(altitude3, altitude1, "Orthocenter")

    GeometrySequence([line12, altitude3, ops1, line23, altitude1, ops2, intersection], name)
    return intersection, [line12, altitude3, ops1, line23, altitude1, ops2, intersection]

