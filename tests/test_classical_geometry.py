import numpy as np
import pytest
from manimgeo.components.points import FreePoint, MidPoint, IntersectionPoint, ExtensionPoint
from manimgeo.components.lines import LineSegment, VerticalLine
from manimgeo.components.conic_section import Circle, ThreePointCircle
from manimgeo.components.base import PointLike
from manimgeo.utils.utils import GeoUtils

class TestClassicalGeometry:
    def test_nine_point_circle(self):
        # 构造三角形ABC
        A = FreePoint(np.array([0, 0]), "A")
        print(f"顶点 {A.name} 坐标: {A.coord}")
        B = FreePoint(np.array([5, 0]), "B")
        print(f"顶点 {B.name} 坐标: {B.coord}")
        C = FreePoint(np.array([2, 3]), "C")
        print(f"顶点 {C.name} 坐标: {C.coord}")
        
        # 构造中点
        AB_mid = MidPoint(A, B, "AB_mid")
        print(f"中点 {AB_mid.name} 坐标: {AB_mid.coord}")
        BC_mid = MidPoint(B, C, "BC_mid")
        print(f"中点 {BC_mid.name} 坐标: {BC_mid.coord}")
        AC_mid = MidPoint(A, C, "AC_mid")
        print(f"中点 {AC_mid.name} 坐标: {AC_mid.coord}")
        
        # 构造边
        AB = LineSegment(A, B, "AB")
        BC = LineSegment(B, C, "BC")
        AC = LineSegment(A, C, "AC")

        # 构造垂足
        C_AB_perp = VerticalLine(C, AB, "C_AB_perp")
        AB_foot = IntersectionPoint(C_AB_perp, AB, "AB_foot")
        print(f"垂足 {AB_foot.name} 坐标: {AB_foot.coord}")

        A_BC_prep = VerticalLine(A, BC, "A_BC_perp")
        BC_foot = IntersectionPoint(A_BC_prep, BC, "BC_foot")
        print(f"垂足 {BC_foot.name} 坐标: {BC_foot.coord}")
        
        B_AC_perp = VerticalLine(B, AC, "B_AC_perp")
        AC_foot = IntersectionPoint(B_AC_perp, AC, "AC_foot")
        print(f"垂足 {AC_foot.name} 坐标: {AC_foot.coord}")
        
        # 构造欧拉点
        orthocenter = IntersectionPoint(A_BC_prep, B_AC_perp, "Orthocenter")
        print(f"垂心 {orthocenter.name} 坐标: {orthocenter.coord}")
        euler_points = [
            MidPoint(A, orthocenter, "A_orthocenter_mid"),
            MidPoint(B, orthocenter, "B_orthocenter_mid"),
            MidPoint(C, orthocenter, "C_orthocenter_mid")
        ]
        for point in euler_points:
            print(f"欧拉点 {point.name} 坐标: {point.coord}")
        
        # 构造九点圆
        nine_point_circle = ThreePointCircle(AB_mid, BC_mid, AC_mid, "NinePointCircle")

        # 打印依赖关系
        print("Dependencies of A:")
        GeoUtils.print_dependencies(A)
        print("")
        
        # 验证所有点都在九点圆上
        for point in [AB_mid, BC_mid, AC_mid, AB_foot, BC_foot, AC_foot] + euler_points:
            point: PointLike
            assert np.isclose(nine_point_circle.radius, np.linalg.norm(point.coord - nine_point_circle.center))
        
    def test_euler_line(self):
        # 构造三角形ABC
        A = FreePoint(np.array([0, 0]), "A")
        B = FreePoint(np.array([4, 0]), "B")
        C = FreePoint(np.array([2, 3]), "C")
        
        # 构造边
        AB = LineSegment(A, B, "AB")
        BC = LineSegment(B, C, "BC")
        AC = LineSegment(A, C, "AC")
        
        # 找到重心
        centroid = (A.coord + B.coord + C.coord) / 3
        
        # 找到垂心
        orthocenter = IntersectionPoint(
            VerticalLine(A, BC),
            VerticalLine(B, AC),
            "Orthocenter"
        )
        
        # 找到外心
        AB_mid = MidPoint(A, B, "AB_mid")
        AC_mid = MidPoint(A, C, "AC_mid")
        perpendicular_bisector_AB = VerticalLine(AB_mid, AB, "AB_perp_bisector")
        perpendicular_bisector_AC = VerticalLine(AC_mid, AC, "AC_perp_bisector")
        circumcenter = IntersectionPoint(perpendicular_bisector_AB, perpendicular_bisector_AC, "Circumcenter")
        
        # 验证三点共线
        vectors = np.array([
            centroid - orthocenter,
            circumcenter - orthocenter
        ])
        rank = np.linalg.matrix_rank(vectors)
        assert rank == 1
        
    def test_simson_line(self):
        # 构造三角形ABC
        A = FreePoint(np.array([0, 0]), "A")
        B = FreePoint(np.array([4, 0]), "B")
        C = FreePoint(np.array([2, 3]), "C")
        
        # 构造边
        AB = LineSegment(A, B, "AB")
        BC = LineSegment(B, C, "BC")
        AC = LineSegment(A, C, "AC")
        
        # 构造外接圆
        circumcircle = ThreePointCircle(A, B, C)
        
        # 构造圆上一点P
        P = FreePoint(np.array([3, 2]), "P")
        
        # 构造西姆松线
        foot_AB = IntersectionPoint(
            VerticalLine(P, AB, "P_AB_perp"),
            AB,
            "foot_AB"
        )
        foot_BC = IntersectionPoint(
            VerticalLine(P, BC, "P_BC_perp"),
            BC,
            "foot_BC"
        )
        foot_CA = IntersectionPoint(
            VerticalLine(P, AC, "P_AC_perp"),
            AC,
            "foot_CA"
        )
        
        # 验证三点共线
        vectors = np.array([
            foot_AB.coord - foot_BC.coord,
            foot_BC.coord - foot_CA.coord
        ])
        rank = np.linalg.matrix_rank(vectors)
        assert rank == 1
        
    def test_pedal_triangle(self):
        # 构造三角形ABC
        A = FreePoint(np.array([0, 0]), "A")
        B = FreePoint(np.array([4, 0]), "B")
        C = FreePoint(np.array([2, 3]), "C")
        
        # 构造边
        AB = LineSegment(A, B, "AB")
        BC = LineSegment(B, C, "BC")
        AC = LineSegment(A, C, "AC")
        
        # 构造垂足三角形
        foot_A = IntersectionPoint(
            VerticalLine(A, BC, "A_BC_perp"),
            BC,
            "foot_A"
        )
        foot_B = IntersectionPoint(
            VerticalLine(B, AC, "B_AC_perp"),
            AC,
            "foot_B"
        )
        foot_C = IntersectionPoint(
            VerticalLine(C, AB, "C_AB_perp"),
            AB,
            "foot_C"
        )
        
        # 验证垂足三角形性质
        area_pedal = 0.5 * np.linalg.norm(
            np.cross(foot_B.coord - foot_A.coord, foot_C.coord - foot_A.coord)
        )
        area_original = 0.5 * np.linalg.norm(
            np.cross(B.coord - A.coord, C.coord - A.coord)
        )
        assert np.isclose(area_pedal / area_original, 0.25)
        
    def test_inversion(self):
        # 构造反演圆
        O = FreePoint(np.array([0, 0]), "O")
        inversion_circle = Circle(O, 2)
        
        # 构造点P
        P = FreePoint(np.array([3, 0]), "P")
        
        # 计算反演点P'
        OP = LineSegment(O, P, "OP")
        OP_length = np.linalg.norm(P.coord - O.coord)
        inversion_radius = inversion_circle.radius**2 / OP_length
        P_prime = ExtensionPoint(O, P, factor=inversion_radius/OP_length, name="P_prime")
        
        # 验证反演性质
        assert np.isclose(
            np.linalg.norm(P.coord - O.coord) * np.linalg.norm(P_prime.coord - O.coord),
            inversion_circle.radius**2
        )
        
    def test_fermat_point(self):
        # 构造等边三角形ABC
        A = FreePoint(np.array([0, 0]), "A")
        B = FreePoint(np.array([4, 0]), "B")
        C = FreePoint(np.array([2, 3.464]), "C")
        
        # 构造费马点
        circle_AB = Circle(A, B, 60, "circle_AB")
        circle_BC = Circle(B, C, 60, "circle_BC")
        fermat_point = IntersectionPoint(
            circle_AB,
            circle_BC,
            "FermatPoint"
        )
        
        # 验证到三个顶点的距离和最小
        distances = [
            np.linalg.norm(fermat_point.coord - A.coord),
            np.linalg.norm(fermat_point.coord - B.coord),
            np.linalg.norm(fermat_point.coord - C.coord)
        ]
        total_distance = sum(distances)
        
        # 测试其他点的距离和
        test_point = FreePoint(np.array([2, 1]), "TestPoint")
        test_distances = [
            np.linalg.norm(test_point.coord - A.coord),
            np.linalg.norm(test_point.coord - B.coord),
            np.linalg.norm(test_point.coord - C.coord)
        ]
        test_total_distance = sum(test_distances)
        
        assert total_distance < test_total_distance
