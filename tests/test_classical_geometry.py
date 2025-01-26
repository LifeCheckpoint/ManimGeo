import numpy as np
from manimgeo.components import *

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
        AB_mid = MidPointPP(A, B, "AB_mid")
        print(f"中点 {AB_mid.name} 坐标: {AB_mid.coord}")
        BC_mid = MidPointPP(B, C, "BC_mid")
        print(f"中点 {BC_mid.name} 坐标: {BC_mid.coord}")
        AC_mid = MidPointPP(A, C, "AC_mid")
        print(f"中点 {AC_mid.name} 坐标: {AC_mid.coord}")
        
        # 构造边
        AB = LineSegmentPP(A, B, "AB")
        BC = LineSegmentPP(B, C, "BC")
        AC = LineSegmentPP(A, C, "AC")

        # 构造垂足
        AB_foot = VerticalPointPL(C, AB, "AB_foot")
        print(f"垂足 {AB_foot.name} 坐标: {AB_foot.coord}")

        BC_foot = VerticalPointPL(A, BC, "BC_foot")
        print(f"垂足 {BC_foot.name} 坐标: {BC_foot.coord}")
        
        AC_foot = VerticalPointPL(B, AC, "AC_foot")
        print(f"垂足 {AC_foot.name} 坐标: {AC_foot.coord}")
        
        # 构造欧拉点
        orthocenter = IntersectionPointLL(
            InfinityLinePP(AB_foot, C),
            InfinityLinePP(BC_foot, A), 
            "Orthocenter"
        )
        print(f"垂心 {orthocenter.name} 坐标: {orthocenter.coord}")
        euler_points = [
            MidPointPP(A, orthocenter, "A_orthocenter_mid"),
            MidPointPP(B, orthocenter, "B_orthocenter_mid"),
            MidPointPP(C, orthocenter, "C_orthocenter_mid")
        ]
        for point in euler_points:
            print(f"欧拉点 {point.name} 坐标: {point.coord}")
        
        # 构造九点圆
        nine_point_circle = CirclePPP(AB_mid, BC_mid, AC_mid, "NinePointCircle")
        print(f"九点圆 {nine_point_circle.name} 半径与圆心: {nine_point_circle.radius_and_center}")

        # 打印依赖关系
        print("Dependencies of A:")
        geo_print_dependencies(A)
        print("")
        
        # 验证所有点都在九点圆上
        for point in [AB_mid, BC_mid, AC_mid, AB_foot, BC_foot, AC_foot] + euler_points:
            point: PointLike
            r, c = nine_point_circle.radius_and_center
            assert np.isclose(r, np.linalg.norm(point.coord - c))
        
    def test_euler_line(self):
        # 构造三角形ABC
        A = FreePoint(np.array([0, 0]), "A")
        B = FreePoint(np.array([5, 0]), "B")
        C = FreePoint(np.array([2, 3]), "C")
        
        # 构造边
        AB = InfinityLinePP(A, B, "AB")
        BC = InfinityLinePP(B, C, "BC")
        AC = InfinityLinePP(A, C, "AC")

        # 重心 垂心 外心
        centroid = CentroidPPP(A, B, C, "Centroid")[0].coord
        orthocenter = OrthocenterPPP(A, B, C, "Orthocenter")[0].coord
        circumcenter = CircumcenterPPP(A, B, C, "Circumcenter")[0].coord

        # 打印依赖关系
        print("Dependencies of A:")
        geo_print_dependencies(A)
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
        A = FreePoint(np.array([0, 0]), "A")
        B = FreePoint(np.array([4, 0]), "B")
        C = FreePoint(np.array([2, 3]), "C")
        
        # 构造边
        AB = LineSegmentPP(A, B, "AB")
        BC = LineSegmentPP(B, C, "BC")
        AC = LineSegmentPP(A, C, "AC")
        
        # 构造外接圆
        circumcircle = CirclePPP(A, B, C)
        
        # 构造圆上一点P
        P = FreePoint(np.array([2, -4/3]), "P")
        
        # 使用高级几何工具构造垂足点
        foot_AB = VerticalPointPL(P, AB, "foot_AB")
        foot_BC = VerticalPointPL(P, BC, "foot_BC")
        foot_CA = VerticalPointPL(P, AC, "foot_CA")

        # 打印依赖关系
        print("Dependencies of A:")
        geo_print_dependencies(A)
        print("")
        
        # 验证三点共线
        vectors = np.array([
            foot_AB.coord - foot_BC.coord,
            foot_BC.coord - foot_CA.coord
        ])
        assert np.linalg.matrix_rank(vectors) == 1, "西姆松线三点不共线"
        
    def test_inversion(self):
        # 使用两点构造法创建反演圆（圆心O，半径2）
        O = FreePoint(np.array([0, 0]), "O")
        R = FreePoint(np.array([2, 0]), "R")
        inversion_circle = CirclePP(O, R, "InversionCircle")
        
        # 构造点P并计算反演点
        P = FreePoint(np.array([3, 0]), "P")
        Q = InversionPointCir(P, inversion_circle, name="Q")
        
        # 打印依赖关系
        print("Dependencies of O:")
        geo_print_dependencies(O)
        print("")

        # 验证反演
        OQ = np.linalg.norm(O.coord - Q.coord)
        assert np.allclose(OQ, 4/3)
        