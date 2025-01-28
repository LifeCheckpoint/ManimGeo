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

def VerticalInfinieLinePL(point: PointLike, line: LineLike, name: str = "") -> Tuple[InfinityLinePP]:
    """
    ## 作过一点垂直线
    """
    direction = VectorPP(line.start, line.end, f"LineDirection")
    trans_point = TranslationPointP(point, direction, f"TranslationPoint")
    vertical_point = RotationPointPPA(trans_point, point, AnglePP(np.pi/2, point, trans_point), f"VerticalPoint")
    inf_line = InfinityLinePP(point, vertical_point, f"InfinityLine")
    
    GeometrySequence([direction, trans_point, vertical_point, inf_line], name)
    return inf_line

def PerpendicularBisectorInfiniteLinePP(point1: PointLike, point2: PointLike, name: str = "") -> Tuple[InfinityLinePP]:
    """
    ## 作两点中垂线
    """
    mid_point = MidPointPP(point1, point2, f"MidPoint")
    line = InfinityLinePP(point1, point2, f"InfiniteLine")
    inf_line = VerticalInfinieLinePL(mid_point, line, f"VerticalInfiniteLine")

    GeometrySequence([mid_point, line, inf_line], name)
    return inf_line

def CentroidPPP(point1: PointLike, point2: PointLike, point3: PointLike, name: str = "") -> Tuple[IntersectionPointLL]:
    """
    ## 三点重心
    """
    mid_12 = MidPointPP(point1, point2, f"MD12")
    mid_23 = MidPointPP(point2, point3, f"MD13")
    line_mid_12 = InfinityLinePP(point3, mid_12, "LMD3-12")
    line_mid_23 = InfinityLinePP(point1, mid_23, "LMD1-23")
    intersection = IntersectionPointLL(line_mid_12, line_mid_23, "Centroid")

    GeometrySequence([mid_12, mid_23, line_mid_12, line_mid_23, intersection], name)
    return intersection

def CircumcenterPPP(point1: PointLike, point2: PointLike, point3: PointLike, name: str = "") -> Tuple[IntersectionPointLL]:
    """
    ## 三点外心
    """
    pb_12 = PerpendicularBisectorInfiniteLinePP(point1, point2, f"PBInfiniteLine 12")
    pb_23 = PerpendicularBisectorInfiniteLinePP(point2, point3, f"PBInfiniteLine 23")
    intersection = IntersectionPointLL(pb_12, pb_23, "Circumcenter")

    GeometrySequence([pb_12, pb_23, intersection], name)
    return intersection

def CircumcenterCir(circle: CirclePPP, name: str = "") -> Tuple[IntersectionPointLL]:
    """
    ## 外接圆三点圆心

    see also `CircumcenterPPP`
    """
    return CircumcenterPPP(circle.point1, circle.point2, circle.point3, name)

def AngleBisectorLL(line1: LineLike, line2: LineLike, sort: bool = True, name: str = "") -> Tuple[InfinityLinePP, InfinityLinePP]:
    """
    ## 两线角平分线

    两条平分线的角度将按照锐角 → 钝角顺序排列
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
    return bis1, bis2

# def IncenterPPP(point1: PointLike, point2: PointLike, point3: PointLike, name: str = "") -> Tuple[IntersectionPointLL]:
#     """
#     ## 三点内心
#     """

def OrthocenterPPP(point1: PointLike, point2: PointLike, point3: PointLike, name: str = "") -> Tuple[IntersectionPointLL]:
    """
    ## 三点垂心
    """
    line12 = InfinityLinePP(point1, point2, f"Line12")
    altitude3 = VerticalInfinieLinePL(point3, line12, f"Altitude3")
    line23 = InfinityLinePP(point2, point3, f"Line23")
    altitude1 = VerticalInfinieLinePL(point1, line23, f"Altitude1")
    intersection = IntersectionPointLL(altitude3, altitude1, "Orthocenter")

    GeometrySequence([line12, altitude3, line23, altitude1, intersection], name)
    return intersection

Circles = Union[CircleP, CirclePP, CirclePPP]

def TangentLineCirP(circle: Circles, point: PointLike, name: str = "") -> Tuple[InfinityLinePP]:
    """
    ## 作圆上一点切线

    如果该点不在圆上则会作出平行线

    See Also `TangentLineCir2`
    """
    line = InfinityLinePP(circle.center_point, point, f"Line")
    tangent = VerticalInfinieLinePL(point, line, f"Tangent")

    GeometrySequence([line, tangent], name)
    return tangent

def TangentLineCirCir(circle1: Circles, circle2: Circles, name: str = "") -> Tuple[InfinityLinePP]:
    """
    ## 作两圆切线
    
    如果两圆相切则作出切线，否则作出平行线
    """
    tangent = PerpendicularBisectorInfiniteLinePP(circle1.center_point, circle2.center_point, f"Tangent")

    GeometrySequence([tangent], name)
    return tangent

def TangentLineCirP2(circle: Circles, point: PointLike, name: str = "") -> Tuple[InfinityLinePP, InfinityLinePP]:
    """
    ## 尺规作过一点圆两条切线

    See Also `TangentLineCirP`
    """
    line_OP = LineSegmentPP(circle.center_point, point, f"LineOP")
    mid = MidPointL(line_OP, f"Mid")
    cir_M = CirclePP(mid, circle.center_point, f"CircleM")
    intersections = IntersectionPointCirCir(cir_M, circle, f"IntersectionsMO")
    tangent1 = InfinityLinePP(point, intersections.point1, f"Tangent1")
    tangent2 = InfinityLinePP(point, intersections.point2, f"Tangent2")

    GeometrySequence([line_OP, mid, cir_M, intersections, tangent1, tangent2], name)
    return tangent1, tangent2

# def PolarInfiniteLineCirP(circle: Circles, point: PointLike, name: str = "") -> Tuple[InfinityLinePP]:
#     """
#     ## 作圆外极点对应极线
#     """
#     tg1, tg2, ops = TangentLineCirP2(circle, point, "TangentLines")
#     polar = InfinityLinePP(ops[3].point1, ops[3].point2, f"PolarInfiniteLine") # 依赖于 TangentLineCirP2
# 
#     GeometrySequence([tg1, tg2, polar], name)
#     return polar

def PolePointCirL(circle: Circles, line: LineLike, name: str = "") -> Tuple[IntersectionPointLL]:
    """
    ## 作圆内极线对应极点
    """
    intersections = IntersectionPointLCir(circle, line, "Intersections")
    tangent1 = TangentLineCirP(circle, intersections.point1, "Tangent1")
    tangent2 = TangentLineCirP(circle, intersections.point2, "Tangent2")
    polar = IntersectionPointLL(tangent1, tangent2, "PolePoint")

    GeometrySequence([intersections, tangent1, tangent2, polar], name)
    return polar

def SqrtLineL(line: LineSegmentPP, name: str = "") -> Tuple[LineSegmentPP]:
    """
    ## 尺规作一根线段，其长度为 line 的算数平方根
    """
    mid = MidPointL(line, "LineMid")
    cir = CirclePP(mid, line.start)
    p_unit_e = ParallelPointPL(line.start, line, 1, "UnitPointE")
    l_ver = VerticalInfinieLinePL(p_unit_e, line, "LineEVertical")
    intersections = IntersectionPointLCir(l_ver, cir, "ERIntersections")
    seg = LineSegmentPP(line.start, intersections.point1, "SqrtLineSegment")

    GeometrySequence([mid, cir, p_unit_e, l_ver, intersections, seg], name)
    return seg

def ParallelLineLP(line: LineLike, point: PointLike, radius_out: float = 1, name: str = "") -> Tuple[InfinityLinePP]:
    """
    ## 尺规作一根过 point 直线，平行于 line

    `radius_out`: 作大于点到直线距离的圆时，半径向外拓展的大小，>0
    """
    if radius_out <= 0:
        raise ValueError(f"Invalid radius_out: {radius_out}")

    radius_min = GeoUtils.point_to_line_distance(line.start.coord, line.end.coord, point.coord)
    r = radius_min + radius_out
    cir1 = CircleP(point, r, "Cir1")
    intersections1 = IntersectionPointLCir(line, cir1, "Intersections1")
    cir2 = CircleP(intersections1.point1, r, "Cir2")
    intersections2 = IntersectionPointLCir(line, cir2, "Intersections2")

    # 判断距离较远的一对点
    if np.linalg.norm(intersections2.point1.coord - point.coord) > np.linalg.norm(intersections2.point2.coord - point.coord):
        p_long = intersections2.point1
    else:
        p_long = intersections2.point2
    cir3 = CircleP(p_long, r, "Cir3")
    intersections3 = IntersectionPointCirCir(cir1, cir3, "Intersections3")

    # 判断平行点
    if GeoUtils.is_point_on_infinite_line(intersections3.point1.coord, line.start.coord, line.end.coord):
        p_final = intersections3.point2
    else:
        p_final = intersections3.point1
    seg = LineSegmentPP(point, p_final, "ParallelSegment")

    GeometrySequence([cir1, intersections1, cir2, intersections2, p_long, cir3, intersections3, p_final, seg], name)
    return seg

# Warn: 依赖失败
def MultiplicationLineLL(line1: LineSegmentPP, line2: LineSegmentPP, name: str = "") -> Tuple[LineSegmentPP]:
    """
    ## 尺规作一根线段，其长度为 line1 的 line2 倍
    """
    l_v = VerticalInfinieLinePL(line1.start, line1, "VeriticalLine1")
    l_inf = InfinityLinePP(line1.start, line1.end)
    p_unit = ParallelPointPL(line1.start, l_v, 1, "UnitParallelPoint")
    l0 = LineSegmentPP(line1.end, p_unit)
    d = np.linalg.norm(line2.end.coord - line2.start.coord)
    cir_l2 = CircleP(line1.start, d, "CircleOfLine2")
    intersections1 = IntersectionPointLCir(l_v, cir_l2, "Intersections")
    
    # 找到与单位点距离最近的同侧点
    if np.linalg.norm(intersections1.point1.coord - p_unit.coord) < np.linalg.norm(intersections1.point2.coord - p_unit.coord):
        p_b = intersections1.point1
    else:
        p_b = intersections1.point2

    l_parallel = ParallelLineLP(l0, p_b, name="ParallelLine")
    intersections2 = IntersectionPointLL(l_inf, l_parallel, "MultiIntersection")
    l_final = LineSegmentPP(line1.start, intersections2)

    GeometrySequence([l_v, l_inf, p_unit, l0, cir_l2, intersections1, p_b, l_parallel, intersections2, l_final], name)
    return l_final

def DivisionLineL(line1: LineSegmentPP, line2: LineSegmentPP, name: str = "") -> Tuple[LineSegmentPP]:
    pass

