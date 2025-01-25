import numpy as np
import pytest
from manimgeo.components.points import FreePoint, MidPoint, IntersectionPoint, ExtensionPoint
from manimgeo.components.lines import LineSegment, VerticalLine
from manimgeo.components.conic_section import Circle, ThreePointCircle
from manimgeo.components.base import PointLike

class TestClassicalGeometry:
    def test_nine_point_circle(self):
        # 构造三角形ABC
        A = FreePoint(np.array([0, 0]), "A")
        B = FreePoint(np.array([5, 0]), "B")
        C = FreePoint(np.array([2, 3]), "C")
        
        # 构造中点
        AB_mid = MidPoint(A, B, "AB_mid")
        BC_mid = MidPoint(B, C, "BC_mid")
        AC_mid = MidPoint(A, C, "AC_mid")
        
        # 构造垂足
        AB_foot = IntersectionPoint(
            VerticalLine(C, LineSegment(A, B)),
            LineSegment(A, B),
            "AB_foot"
        )
        BC_foot = IntersectionPoint(
            VerticalLine(A, LineSegment(B, C)),
            LineSegment(B, C),
            "BC_foot"
        )
        AC_foot = IntersectionPoint(
            VerticalLine(B, LineSegment(A, C)),
            LineSegment(A, C),
            "AC_foot"
        )
        
        # 构造欧拉点
        orthocenter = IntersectionPoint(
            VerticalLine(A, LineSegment(B, C)),
            VerticalLine(B, LineSegment(A, C)),
            "Orthocenter"
        )
        euler_points = [
            MidPoint(A, orthocenter),
            MidPoint(B, orthocenter),
            MidPoint(C, orthocenter)
        ]
        
        # 构造九点圆
        nine_point_circle = ThreePointCircle(AB_mid, BC_mid, AC_mid)
        
        # 验证所有点都在九点圆上
        for point in [AB_mid, BC_mid, AC_mid, AB_foot, BC_foot, AC_foot] + euler_points:
            point: PointLike
            assert np.isclose(nine_point_circle.radius, np.linalg.norm(point.coord - nine_point_circle.center))
        
    def test_euler_line(self):
        # 构造三角形ABC
        A = FreePoint(np.array([0, 0]), "A")
        B = FreePoint(np.array([4, 0]), "B")
        C = FreePoint(np.array([2, 3]), "C")
        
        # 找到重心
        centroid = (A.coord + B.coord + C.coord) / 3
        
        # 找到垂心
        orthocenter = IntersectionPoint(
            VerticalLine(A, LineSegment(B, C)),
            VerticalLine(B, LineSegment(A, C)),
            "Orthocenter"
        )
        
        # 找到外心
        perpendicular_bisector_AB = VerticalLine(MidPoint(A, B), LineSegment(A, B))
        perpendicular_bisector_AC = VerticalLine(MidPoint(A, C), LineSegment(A, C))
        circumcenter = IntersectionPoint(perpendicular_bisector_AB, perpendicular_bisector_AC)
        
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
        
        # 构造外接圆
        circumcircle = ThreePointCircle(A, B, C)
        
        # 构造圆上一点P
        P = FreePoint(np.array([3, 2]), "P")
        
        # 构造西姆松线
        foot_AB = IntersectionPoint(
            VerticalLine(P, LineSegment(A, B)),
            LineSegment(A, B)
        )
        foot_BC = IntersectionPoint(
            VerticalLine(P, LineSegment(B, C)),
            LineSegment(B, C)
        )
        foot_CA = IntersectionPoint(
            VerticalLine(P, LineSegment(C, A)),
            LineSegment(C, A)
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
        
        # 构造垂足三角形
        foot_A = IntersectionPoint(
            VerticalLine(A, LineSegment(B, C)),
            LineSegment(B, C)
        )
        foot_B = IntersectionPoint(
            VerticalLine(B, LineSegment(A, C)),
            LineSegment(A, C)
        )
        foot_C = IntersectionPoint(
            VerticalLine(C, LineSegment(A, B)),
            LineSegment(A, B)
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
        OP = LineSegment(O, P)
        OP_length = np.linalg.norm(P.coord - O.coord)
        inversion_radius = inversion_circle.radius**2 / OP_length
        P_prime = ExtensionPoint(O, P, factor=inversion_radius/OP_length)
        
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
        fermat_point = IntersectionPoint(
            Circle(A, B, 60),
            Circle(B, C, 60),
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
