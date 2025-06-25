import numpy as np
from manimgeo.components import *
from manimgeo.utils.utils import print_dependencies

def test_nine_point_circle():
    # 构造三角形ABC
    A = Point.Free(np.array([0, 0, 0]), "A")
    B = Point.Free(np.array([5, 0, 0]), "B")
    C = Point.Free(np.array([2, 3, 0]), "C")
    print(f"顶点 {A.name} 坐标: {A.coord}")
    print(f"顶点 {B.name} 坐标: {B.coord}")
    print(f"顶点 {C.name} 坐标: {C.coord}")

    # 构造中点
    AB_mid = Point.MidPP(A, B, "AB_mid")
    BC_mid = Point.MidPP(B, C, "BC_mid")
    AC_mid = Point.MidPP(A, C, "AC_mid")
    print(f"中点 {AB_mid.name} 坐标: {AB_mid.coord}")
    print(f"中点 {BC_mid.name} 坐标: {BC_mid.coord}")
    print(f"中点 {AC_mid.name} 坐标: {AC_mid.coord}")

    # 构造边
    AB = LineSegment.PP(A, B, "AB")
    BC = LineSegment.PP(B, C, "BC")
    AC = LineSegment.PP(A, C, "AC")

    # 构造垂足
    AB_foot = Point.VerticalPL(C, AB, "AB_foot")
    BC_foot = Point.VerticalPL(A, BC, "BC_foot")
    AC_foot = Point.VerticalPL(B, AC, "AC_foot")
    print(f"垂足 {AB_foot.name} 坐标: {AB_foot.coord}")
    print(f"垂足 {BC_foot.name} 坐标: {BC_foot.coord}")
    print(f"垂足 {AC_foot.name} 坐标: {AC_foot.coord}")

    # 构造欧拉点
    orthocenter = Point.IntersectionLL(
        InfinityLine.PP(AB_foot, C),
        InfinityLine.PP(BC_foot, A), 
        True,
        "Orthocenter"
    )
    euler_points = [
        Point.MidPP(A, orthocenter, "A_orthocenter_mid"),
        Point.MidPP(B, orthocenter, "B_orthocenter_mid"),
        Point.MidPP(C, orthocenter, "C_orthocenter_mid")
    ]
    print(f"垂心 {orthocenter.name} 坐标: {orthocenter.coord}")
    for point in euler_points:
        print(f"欧拉点 {point.name} 坐标: {point.coord}")

    # 构造九点圆
    nine_point_circle = Circle.PPP(AB_mid, BC_mid, AC_mid, "NinePointCircle")
    print(f"九点圆 {nine_point_circle.name} 半径: {nine_point_circle.radius} 圆心: {nine_point_circle.center}")

    # 打印依赖关系
    print("Dependencies of A:")
    print_dependencies(A)
    print("")

    # 验证所有点都在九点圆上
    for geometry_point in [AB_mid, BC_mid, AC_mid, AB_foot, BC_foot, AC_foot] + euler_points:
        geometry_point: Point
        r, c = nine_point_circle.radius, nine_point_circle.center
        assert np.isclose(r, np.linalg.norm(geometry_point.coord - c))