import numpy as np
from manimgeo.components import *
from manimgeo.utils.utils import GeoUtils

class TestClassicalGeometry:
    def test_simple_1(self):
        # 创建自由点
        A = Point.Free(np.array([0, 0, 0]), "A")
        B = Point.Free(np.array([4, 0, 0]), "B")
        C = Point.Free(np.array([1, 3, 0]), "C")

        # 构造线段AB, BC, AC
        AB = LineSegment.PP(A, B, "AB")
        BC = LineSegment.PP(B, C, "BC")
        AC = LineSegment.PP(A, C, "AC")

        # 创建中点M
        M = Point.MidL(AB, "M")

        # 构造线段CM
        CM = LineSegment.PP(C, M, "CM")

        # 创建延长点N, O
        N = Point.ExtensionPP(C, M, factor=2.0, name="N")
        O = Point.ExtensionPP(C, M, factor=3.0, name="O")

        # 构造射线AN，交OB于P
        AN = Ray.PP(A, N, "AN")
        OB = Ray.PP(O, B, "OB")
        P = Point.IntersectionLL(AN, OB, False, "P")

        # 打印 A 依赖关系
        print("Dependencies of A:")
        GeoUtils.print_dependencies(A)
        print("")

        # 输出移动前坐标
        print("Before moving B:")
        print(f"{P.name}: {P.coord}")
        assert np.allclose(P.coord, np.array([4, -4, 0]))

        # 移动B
        B.set_coord(np.array([5, 0, 0]))

        # 输出移动后坐标
        print("After moving P:")
        print(f"{P.name}: {P.coord}")
        assert np.allclose(P.coord, np.array([16/3, -4, 0]))

    def test_simple_2(self):
        # 创建自由点
        A = Point.Free(np.array([0, 0, 0]), "A")
        B = Point.Free(np.array([5, 0, 0]), "B")
        C = Point.Free(np.array([1, 3, 0]), "C")
        D = Point.Free(np.array([2, -1, 0]), "D")

        AB = InfinityLine.PP(A, B, "AB")
        BC = InfinityLine.PP(B, C, "BC")

        vl_d_ab = Ray.VerticalPL(D, AB, "VL")
        E = Point.IntersectionLL(BC, vl_d_ab, True, "IE")

        print(E.coord)
        assert np.allclose(E.coord, np.array([2, 2.25, 0]))

        # 构造三点圆
        circle = Circle.PPP(E, D, C, "ThreePointCircle")
        centerF = Point.Cir(circle, "CCF")

        GeoUtils.print_dependencies(A)
        print(centerF.coord)
        assert np.allclose(centerF.coord, np.array([0, 0.625, 0]))

    def test_nine_point_circle(self):
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
        GeoUtils.print_dependencies(A)
        print("")
        
        # 验证所有点都在九点圆上
        for point in [AB_mid, BC_mid, AC_mid, AB_foot, BC_foot, AC_foot] + euler_points:
            point: Point
            r, c = nine_point_circle.radius, nine_point_circle.center
            assert np.isclose(r, np.linalg.norm(point.coord - c))
        
    def test_euler_line(self):
        # 构造三角形ABC
        A = Point.Free(np.array([0, 0, 0]), "A")
        B = Point.Free(np.array([5, 0, 0]), "B")
        C = Point.Free(np.array([2, 3, 0]), "C")
        
        # 构造边
        AB = InfinityLine.PP(A, B, "AB")
        BC = InfinityLine.PP(B, C, "BC")
        AC = InfinityLine.PP(A, C, "AC")

        # 重心 垂心 外心
        centroid = Point.CentroidPPP(A, B, C, "Centroid").coord
        orthocenter = Point.OrthocenterPPP(A, B, C, "Orthocenter").coord
        circumcenter = Point.CircumcenterPPP(A, B, C, "Circumcenter").coord

        # 打印依赖关系
        print("Dependencies of A:")
        GeoUtils.print_dependencies(A)
        print("")
        
        # 验证三点共线
        vectors = np.array([
            centroid - orthocenter,
            circumcenter - orthocenter
        ])
        rank = np.linalg.matrix_rank(vectors)
        assert rank == 1
        
    def test_simson_line(self):
        # 构造三角形ABC
        A = Point.Free(np.array([0, 0, 0]), "A")
        B = Point.Free(np.array([4, 0, 0]), "B")
        C = Point.Free(np.array([2, 3, 0]), "C")
        
        # 构造边
        AB = LineSegment.PP(A, B, "AB")
        BC = LineSegment.PP(B, C, "BC")
        AC = LineSegment.PP(A, C, "AC")
        
        # 构造外接圆
        circumcircle = Circle.PPP(A, B, C)
        
        # 构造圆上一点P
        P = Point.Free(np.array([2, -4/3, 0]), "P")
        
        # 使用高级几何工具构造垂足点
        foot_AB = Point.VerticalPL(P, AB, "foot_AB")
        foot_BC = Point.VerticalPL(P, BC, "foot_BC")
        foot_CA = Point.VerticalPL(P, AC, "foot_CA")

        # 打印依赖关系
        print("Dependencies of A:")
        GeoUtils.print_dependencies(A)
        print("")
        
        # 验证三点共线
        vectors = np.array([
            foot_AB.coord - foot_BC.coord,
            foot_BC.coord - foot_CA.coord
        ])
        assert np.linalg.matrix_rank(vectors) == 1, "西姆松线三点不共线"
        
    def test_inversion(self):
        # 使用两点构造法创建反演圆（圆心O，半径2）
        O = Point.Free(np.array([0, 0, 0]), "O")
        R = Point.Free(np.array([2, 0, 0]), "R")
        inversion_circle = Circle.PP(O, R, "InversionCircle")
        
        # 构造点P并计算反演点
        P = Point.Free(np.array([3, 0, 0]), "P")
        Q = Point.InversionPCir(P, inversion_circle, name="Q")
        
        # 打印依赖关系
        print("Dependencies of O:")
        GeoUtils.print_dependencies(O)
        print("")

        # 验证反演
        OQ = np.linalg.norm(O.coord - Q.coord)
        assert np.allclose(OQ, 4/3)