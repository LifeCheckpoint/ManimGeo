
# def PerpendicularBisectorInfiniteLinePP(point1: PointLike, point2: PointLike, name: str = "") -> Tuple[InfinityLinePP]:
#     """
#     ## 作两点中垂线
#     """
#     mid_point = MidPointPP(point1, point2, f"MidPoint")
#     line = InfinityLinePP(point1, point2, f"InfiniteLine")
#     inf_line = VerticalInfinieLinePL(mid_point, line, f"VerticalInfiniteLine")

#     GeometrySequence([mid_point, line, inf_line], name)
#     return inf_line

# def AngleBisectorLL(line1: LineLike, line2: LineLike, sort: bool = True, name: str = "") -> Tuple[InfinityLinePP, InfinityLinePP]:
#     """
#     ## 两线角平分线

#     两条平分线的角度将按照锐角 → 钝角顺序排列
#     """
#     # TODO 重新设计以保证单解性
#     intersection = IntersectionPointLL(line1, line2, f"Intersection")
#     radius = min(
#         0.1, 
#         np.linalg.norm(intersection.coord - line1.start),
#         np.linalg.norm(intersection.coord - line1.end),
#         np.linalg.norm(intersection.coord - line2.start),
#         np.linalg.norm(intersection.coord - line2.end)
#     )
#     cir = CircleP(intersection, radius, f"Circle")
#     l1_intersections = IntersectionPointLCir(line1, cir, f"IntersectionPointLine1")
#     l2_intersections = IntersectionPointLCir(line2, cir, f"IntersectionPointLine2")

#     seg_line1 = LineSegmentPP(l1_intersections.point1, l2_intersections.point1, f"LineSegment1")
#     seg_line2 = LineSegmentPP(l1_intersections.point1, l2_intersections.point2, f"LineSegment2")

#     mid1 = MidPointL(seg_line1, f"MidPoint1")
#     mid2 = MidPointL(seg_line2, f"MidPoint2")

#     bis1 = InfinityLinePP(mid1, intersection, f"AngleBisector1")
#     bis2 = InfinityLinePP(mid2, intersection, f"AngleBisector2")

#     # 计算角度并排序
#     angle1 = min(
#         GeoUtils.calculate_angle(intersection.coord, mid1.coord, l2_intersections.point1.coord),
#         GeoUtils.calculate_angle(intersection.coord, mid1.coord, l2_intersections.point2.coord)   
#     )
#     angle2 = min(
#         GeoUtils.calculate_angle(intersection.coord, mid2.coord, l1_intersections.point1.coord),
#         GeoUtils.calculate_angle(intersection.coord, mid2.coord, l1_intersections.point2.coord)   
#     )
#     # 锐角角平分线在前
#     if sort and angle1 > angle2:
#         bis1, bis2 = bis2, bis1

#     GeometrySequence([intersection, cir, l1_intersections, l2_intersections, seg_line1, seg_line2, mid1, mid2, bis1, bis2], name)
#     return bis1, bis2

# Circles = Union[CircleP, CirclePP, CirclePPP]

# def TangentLineCirP(circle: Circles, point: PointLike, name: str = "") -> Tuple[InfinityLinePP]:
#     """
#     ## 作圆上一点切线

#     如果该点不在圆上则会作出平行线

#     See Also `TangentLineCir2`
#     """
#     line = InfinityLinePP(circle.center_point, point, f"Line")
#     tangent = VerticalInfinieLinePL(point, line, f"Tangent")

#     GeometrySequence([line, tangent], name)
#     return tangent

# def TangentLineCirCir(circle1: Circles, circle2: Circles, name: str = "") -> Tuple[InfinityLinePP]:
#     """
#     ## 作两圆切线
    
#     如果两圆相切则作出切线，否则作出平行线
#     """
#     tangent = PerpendicularBisectorInfiniteLinePP(circle1.center_point, circle2.center_point, f"Tangent")

#     GeometrySequence([tangent], name)
#     return tangent

# def TangentLineCirP2(circle: Circles, point: PointLike, name: str = "") -> Tuple[InfinityLinePP, InfinityLinePP]:
#     """
#     ## 尺规作过一点圆两条切线

#     See Also `TangentLineCirP`
#     """
#     line_OP = LineSegmentPP(circle.center_point, point, f"LineOP")
#     mid = MidPointL(line_OP, f"Mid")
#     cir_M = CirclePP(mid, circle.center_point, f"CircleM")
#     intersections = IntersectionPointCirCir(cir_M, circle, f"IntersectionsMO")
#     tangent1 = InfinityLinePP(point, intersections.point1, f"Tangent1")
#     tangent2 = InfinityLinePP(point, intersections.point2, f"Tangent2")

#     GeometrySequence([line_OP, mid, cir_M, intersections, tangent1, tangent2], name)
#     return tangent1, tangent2

# # def PolarInfiniteLineCirP(circle: Circles, point: PointLike, name: str = "") -> Tuple[InfinityLinePP]:
# #     """
# #     ## 作圆外极点对应极线
# #     """
# #     tg1, tg2, ops = TangentLineCirP2(circle, point, "TangentLines")
# #     polar = InfinityLinePP(ops[3].point1, ops[3].point2, f"PolarInfiniteLine") # 依赖于 TangentLineCirP2
# # 
# #     GeometrySequence([tg1, tg2, polar], name)
# #     return polar

# def PolePointCirL(circle: Circles, line: LineLike, name: str = "") -> Tuple[IntersectionPointLL]:
#     """
#     ## 作圆内极线对应极点
#     """
#     intersections = IntersectionPointLCir(circle, line, "Intersections")
#     tangent1 = TangentLineCirP(circle, intersections.point1, "Tangent1")
#     tangent2 = TangentLineCirP(circle, intersections.point2, "Tangent2")
#     polar = IntersectionPointLL(tangent1, tangent2, "PolePoint")

#     GeometrySequence([intersections, tangent1, tangent2, polar], name)
#     return polar

# def SqrtLineL(line: LineSegmentPP, name: str = "") -> Tuple[LineSegmentPP]:
#     """
#     ## 尺规作一根线段，其长度为 line 的算数平方根
#     """
#     mid = MidPointL(line, "LineMid")
#     cir = CirclePP(mid, line.start)
#     p_unit_e = ParallelPointPL(line.start, line, 1, "UnitPointE")
#     l_ver = VerticalInfinieLinePL(p_unit_e, line, "LineEVertical")
#     intersections = IntersectionPointLCir(l_ver, cir, "ERIntersections")
#     seg = LineSegmentPP(line.start, intersections.point1, "SqrtLineSegment")

#     GeometrySequence([mid, cir, p_unit_e, l_ver, intersections, seg], name)
#     return seg

# def ParallelLineLP(line: LineLike, point: PointLike, radius_out: float = 1, name: str = "") -> Tuple[InfinityLinePP]:
#     """
#     ## 尺规作一根过 point 直线，平行于 line

#     `radius_out`: 作大于点到直线距离的圆时，半径向外拓展的大小，>0
#     """
#     if radius_out <= 0:
#         raise ValueError(f"Invalid radius_out: {radius_out}")

#     radius_min = GeoUtils.point_to_line_distance(line.start.coord, line.end.coord, point.coord)
#     r = radius_min + radius_out
#     cir1 = CircleP(point, r, "Cir1")
#     intersections1 = IntersectionPointLCir(line, cir1, "Intersections1")
#     cir2 = CircleP(intersections1.point1, r, "Cir2")
#     intersections2 = IntersectionPointLCir(line, cir2, "Intersections2")

#     # 判断距离较远的一对点
#     if np.linalg.norm(intersections2.point1.coord - point.coord) > np.linalg.norm(intersections2.point2.coord - point.coord):
#         p_long = intersections2.point1
#     else:
#         p_long = intersections2.point2
#     cir3 = CircleP(p_long, r, "Cir3")
#     intersections3 = IntersectionPointCirCir(cir1, cir3, "Intersections3")

#     # 判断平行点
#     if GeoUtils.is_point_on_infinite_line(intersections3.point1.coord, line.start.coord, line.end.coord):
#         p_final = intersections3.point2
#     else:
#         p_final = intersections3.point1
#     seg = LineSegmentPP(point, p_final, "ParallelSegment")

#     GeometrySequence([cir1, intersections1, cir2, intersections2, p_long, cir3, intersections3, p_final, seg], name)
#     return seg
