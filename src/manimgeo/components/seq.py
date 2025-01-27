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
    trans_point = TranslationPointP(point, direction, f"TranslationPoint")
    vertical_point = RotationPointPPA(trans_point, point, AnglePP(np.pi/2, point, trans_point), f"VerticalPoint")
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

def CircumcenterCir(circle: CirclePPP, name: str = "") -> Tuple[IntersectionPointLL, List[BaseGeometry]]:
    """
    ## 外接圆三点圆心

    see also `CircumcenterPPP`
    """
    return CircumcenterPPP(circle.point1, circle.point2, circle.point3, name)

def AngleBisectorLL(line1: LineLike, line2: LineLike, sort: bool = True, name: str = "") -> Tuple[InfinityLinePP, InfinityLinePP, List[BaseGeometry]]:
    """
    ## 两线角平分线

    两条平分线的角度将按照锐角 → 钝角顺序排列
    
    return: InfinityLinePP, InfinityLinePP, [IntersectionPointLL, CircleP, IntersectionPointLCir, IntersectionPointLCir, LineSegmentPP, LineSegmentPP, MidPointL, MidPointL, InfinityLinePP, InfinityLinePP]
    """
    # TODO 重新设计以保证单解性
    intersection = IntersectionPointLL(line1, line2, f"Intersection")
    radius = min(
        0.1, 
        np.linalg.norm(intersection.coord - line1.start),
        np.linalg.norm(intersection.coord - line1.end),
        np.linalg.norm(intersection.coord - line2.start),
        np.linalg.norm(intersection.coord - line2.end)
    )
    cir = CircleP(intersection, radius, f"Circle")
    l1_intersections = IntersectionPointLCir(line1, cir, f"IntersectionPointLine1")
    l2_intersections = IntersectionPointLCir(line2, cir, f"IntersectionPointLine2")

    seg_line1 = LineSegmentPP(l1_intersections.point1, l2_intersections.point1, f"LineSegment1")
    seg_line2 = LineSegmentPP(l1_intersections.point1, l2_intersections.point2, f"LineSegment2")

    mid1 = MidPointL(seg_line1, f"MidPoint1")
    mid2 = MidPointL(seg_line2, f"MidPoint2")

    bis1 = InfinityLinePP(mid1, intersection, f"AngleBisector1")
    bis2 = InfinityLinePP(mid2, intersection, f"AngleBisector2")

    # 计算角度并排序
    angle1 = min(
        GeoUtils.calculate_angle(intersection.coord, mid1.coord, l2_intersections.point1.coord),
        GeoUtils.calculate_angle(intersection.coord, mid1.coord, l2_intersections.point2.coord)   
    )
    angle2 = min(
        GeoUtils.calculate_angle(intersection.coord, mid2.coord, l1_intersections.point1.coord),
        GeoUtils.calculate_angle(intersection.coord, mid2.coord, l1_intersections.point2.coord)   
    )
    # 锐角角平分线在前
    if sort and angle1 > angle2:
        bis1, bis2 = bis2, bis1

    GeometrySequence([intersection, cir, l1_intersections, l2_intersections, seg_line1, seg_line2, mid1, mid2, bis1, bis2], name)
    return bis1, bis2, [intersection, cir, l1_intersections, l2_intersections, seg_line1, seg_line2, mid1, mid2, bis1, bis2]

# def IncenterPPP(point1: PointLike, point2: PointLike, point3: PointLike, name: str = "") -> Tuple[IntersectionPointLL, List[BaseGeometry]]:
#     """
#     ## 三点内心
    
#     return: IntersectionPointLL, [LineLike, LineLike, *AngleBisectorLL, LineLike, LineLike, *AngleBisectorLL, IntersectionPointLL]
#     """

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

Circles = Union[CircleP, CirclePP, CirclePPP]

def TangentLineCirP(circle: Circles, point: PointLike, name: str = "") -> Tuple[InfinityLinePP, List[BaseGeometry]]:
    """
    ## 作圆上一点切线

    如果该点不在圆上则会作出平行线

    See Also `TangentLineCir2`

    return: InfinityLinePP, [InfinityLinePP, InfinityLinePP, *VerticalInfinieLinePL]
    """
    line = InfinityLinePP(circle.center_point, point, f"Line")
    tangent, ops = VerticalInfinieLinePL(point, line, f"Tangent")

    GeometrySequence([line, tangent, ops], name)
    return tangent, [line, tangent, ops]

def TangentLineCirCir(circle1: Circles, circle2: Circles, name: str = "") -> Tuple[InfinityLinePP, List[BaseGeometry]]:
    """
    ## 作两圆切线
    
    如果两圆相切则作出切线，否则作出平行线

    return: InfinityLinePP, [InfinityLinePP, *VerticalInfinieLinePL]
    """
    tangent, ops = PerpendicularBisectorInfiniteLinePP(circle1.center_point, circle2.center_point, f"Tangent")

    GeometrySequence([tangent, ops], name)
    return tangent, [tangent, ops]

def TangentLineCirP2(circle: Circles, point: PointLike, name: str = "") -> Tuple[InfinityLinePP, InfinityLinePP, List[BaseGeometry]]:
    """
    ## 尺规作过一点圆两条切线

    See Also `TangentLineCirP`

    return: InfinityLinePP, InfinityLinePP, [LineSegmentPP, MidPointL, CirclePP, IntersectionPointCirCir, InfinityLinePP, InfinityLinePP]
    """
    line_OP = LineSegmentPP(circle.center_point, point, f"LineOP")
    mid = MidPointL(line_OP, f"Mid")
    cir_M = CirclePP(mid, circle.center_point, f"CircleM")
    intersections = IntersectionPointCirCir(cir_M, circle, f"IntersectionsMO")
    tangent1 = InfinityLinePP(point, intersections.point1, f"Tangent1")
    tangent2 = InfinityLinePP(point, intersections.point2, f"Tangent2")

    GeometrySequence([line_OP, mid, cir_M, intersections, tangent1, tangent2], name)
    return tangent1, tangent2, [line_OP, mid, cir_M, intersections, tangent1, tangent2]

def PolarInfiniteLineCirP(circle: Circles, point: PointLike, name: str = "") -> Tuple[InfinityLinePP, List[BaseGeometry]]:
    """
    ## 作圆外极点对应极线

    return: InfinityLinePP, [InfinityLinePP, InfinityLinePP, *TangentLineCirP2, InfinityLinePP]
    """
    tg1, tg2, ops = TangentLineCirP2(circle, point, "TangentLines")
    polar = InfinityLinePP(ops[3].point1, ops[3].point2, f"PolarInfiniteLine") # 依赖于 TangentLineCirP2

    GeometrySequence([tg1, tg2, ops, polar], name)
    return polar, [tg1, tg2, ops, polar]

def PolePointCirL(circle: Circles, line: LineLike, name: str = "") -> Tuple[IntersectionPointLL, List[BaseGeometry]]:
    """
    ## 作圆内极线对应极点

    return: IntersectionPointLL, [IntersectionPointLCir, InfinityLinePP, *TangentLineCirP, InfinityLinePP, *TangentLineCirP, IntersectionPointLL]
    """
    intersections = IntersectionPointLCir(circle, line, "Intersections")
    tangent1, ops1 = TangentLineCirP(circle, intersections.point1, "Tangent1")
    tangent2, ops2 = TangentLineCirP(circle, intersections.point2, "Tangent2")
    polar = IntersectionPointLL(tangent1, tangent2, "PolePoint")

    GeometrySequence([intersections, tangent1, ops1, tangent2, ops2, polar], name)
    return polar, [intersections, tangent1, ops1, tangent2, ops2, polar]