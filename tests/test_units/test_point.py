import numpy as np
import math
import sys
sys.path.append("D://wroot//ManimGeo//src") # 使用绝对路径避免测试路径问题

from manimgeo.components import *

class TestPoint:
    def test_AxisymmetricPointPL(self):
        # 对称点测试
        line = InfinityLinePP(FreePoint(np.array([0, 0])), FreePoint(np.array([1, 0])))  # x轴
        point = FreePoint(np.array([2, 3]))
        sym_point = AxisymmetricPointPL(point, line)
        assert np.allclose(sym_point.coord, np.array(np.array([2, -3])))  # 对称后应为(2,-3)

        line2 = InfinityLinePP(FreePoint(np.array([1, 1])), FreePoint(np.array([2, 2])))  # 直线y=x
        point2 = FreePoint(np.array([3, 2]))
        sym_point2 = AxisymmetricPointPL(point2, line2)
        assert np.allclose(sym_point2.coord, np.array(np.array([2, 3])))  # 关于y=x对称

    def test_ConstraintPoint(self):
        # 约束点测试
        pass

    def test_ExtensionPointPP(self):
        # 延长点测试
        A = FreePoint(np.array([0, 0]))
        B = FreePoint(np.array([1, 1]))
        extend_point = ExtensionPointPP(A, B, 2)  # 延长到B之后，总长度2倍
        assert np.allclose(extend_point.coord, np.array([2, 2]))

        C = FreePoint(np.array([3, 4]))
        D = FreePoint(np.array([5, 7]))
        extend_point2 = ExtensionPointPP(C, D, -0.5)  # 反向，一半
        assert np.allclose(extend_point2.coord, np.array([2, 2.5]))

    def test_IntersectionPointCirCir(self):
        # 两圆交点测试

        # 相交情况
        circle1 = CirclePP(FreePoint(np.array([0, 0])), FreePoint(np.array([1, 0])))  # 圆心(0,0)，半径1
        circle2 = CirclePP(FreePoint(np.array([1, 0])), FreePoint(np.array([2, 0])))  # 圆心(1,0)，半径1
        inter_points = IntersectionPointCirCir(circle1, circle2)
        expected1 = np.array([0.5, math.sqrt(3)/2])
        expected2 = np.array([0.5, -math.sqrt(3)/2])
        assert (np.allclose(inter_points.point1.coord, expected1) or 
                np.allclose(inter_points.point1.coord, expected2))
        
        # 相切情况
        circle3 = CirclePP(FreePoint(np.array([0, 0])), FreePoint(np.array([2, 0])))  # 半径2
        circle4 = CirclePP(FreePoint(np.array([4, 0])), FreePoint(np.array([2, 0])))  # 圆心(4,0)，半径2
        inter_points2 = IntersectionPointCirCir(circle3, circle4)
        assert np.allclose(inter_points2.point1.coord, [2, 0])

        # 无交点情况 BUG
        circle5 = CirclePP(FreePoint(np.array([0, 0])), FreePoint(np.array([1, 0])))
        circle6 = CirclePP(FreePoint(np.array([3, 0])), FreePoint(np.array([2, 0])))
        try:
            IntersectionPointCirCir(circle5, circle6)
            assert False, "Expected ValueError for no intersection"
        except ValueError:
            pass

    def test_IntersectionPointLCir(self):
        # 线圆交点测试
        
        # 线段与圆相交
        circle = CirclePP(FreePoint(np.array([0, 0])), FreePoint(np.array([1, 0])))  # 单位圆
        line = LineSegmentPP(FreePoint(np.array([-2, 0])), FreePoint(np.array([2, 0])))  # x轴线段
        intersections = IntersectionPointLCir(line, circle)
        assert (np.allclose(intersections.point1.coord, [1, 0]) and \
               np.allclose(intersections.point2.coord, [-1, 0])) or \
               (np.allclose(intersections.point1.coord, [-1, 0]) and \
               np.allclose(intersections.point2.coord, [1, 0]))

        # 射线与圆相切
        circle2 = CirclePP(FreePoint(np.array([0, 0])), FreePoint(np.array([1, 0])))
        ray = RayPP(FreePoint(np.array([0, 1])), FreePoint(np.array([1, 1])))  # 水平射线y=1
        tangent_point = IntersectionPointLCir(ray, circle2)
        assert np.allclose(tangent_point.point1.coord, [0, 1]) and np.allclose(tangent_point.point2.coord, [0, 1])

        # 无限直线不相交
        inf_line = InfinityLinePP(FreePoint(np.array([3, 0])), FreePoint(np.array([3, 1])))  # x=3
        try:
            IntersectionPointLCir(inf_line, circle)
            assert False, "Expected no intersection"
        except ValueError:
            pass

    def test_IntersectionPointLL(self):
        # 线线交点测试

        # 普通测试
        seg1 = LineSegmentPP(FreePoint(np.array([1, 1])), FreePoint(np.array([2, 2])))
        seg2 = LineSegmentPP(FreePoint(np.array([1, 2])), FreePoint(np.array([2, 1])))
        inter = IntersectionPointLL(seg1, seg2)
        assert np.allclose(inter.coord, np.array([1.5, 1.5]))

        ray1 = RayPP(FreePoint(np.array([1, 1])), FreePoint(np.array([2, 2])))
        ray2 = RayPP(FreePoint(np.array([3.5, -1])), FreePoint(np.array([3.5, 0])))
        inter = IntersectionPointLL(ray1, ray2)
        assert np.allclose(inter.coord, np.array([3.5, 3.5]))

        inf1 = InfinityLinePP(FreePoint(np.array([1, 1])), FreePoint(np.array([2, 2])))
        inf2 = InfinityLinePP(FreePoint(np.array([1, -1])), FreePoint(np.array([2, -2])))
        inter = IntersectionPointLL(inf1, inf2)
        assert np.allclose(inter.coord, np.array([0, 0]))

        # 无交点测试 BUG
        seg1 = LineSegmentPP(FreePoint(np.array([1, 1])), FreePoint(np.array([2, 2])))
        seg2 = LineSegmentPP(FreePoint(np.array([3, 4])), FreePoint(np.array([4, 3])))
        try:
            inter = IntersectionPointLL(seg1, seg2)
            assert False, "Expected ValueError"
        except ValueError:
            pass

        ray1 = RayPP(FreePoint(np.array([1, 1])), FreePoint(np.array([2, 2])))
        ray2 = RayPP(FreePoint(np.array([3, 4])), FreePoint(np.array([2, 5])))
        try:
            inter = IntersectionPointLL(ray1, ray2)
            assert False, "Expected ValueError"
        except ValueError:
            pass

        inf1 = InfinityLinePP(FreePoint(np.array([1, 1])), FreePoint(np.array([2, 2])))
        inf2 = InfinityLinePP(FreePoint(np.array([3, 3])), FreePoint(np.array([4, 4])))
        try:
            inter = IntersectionPointLL(inf1, inf2)
            assert False, "Expected ValueError"
        except ValueError:
            pass

    def test_InversionPointPCir(self):
        # 反演点测试
        pass

    def test_MidPointL(self):
        # 线段中点测试
        p1 = FreePoint(np.array([1, -3]))
        p2 = FreePoint(np.array([17, -14]))
        mid = MidPointL(LineSegmentPP(p1, p2))
        assert np.allclose(mid.coord, np.array([9, -8.5]))

    def test_MidPointPP(self):
        # 两点中点测试
        p1 = FreePoint(np.array([-1, 3]))
        p2 = FreePoint(np.array([4, 17]))
        mid = MidPointPP(p1, p2)
        assert np.allclose(mid.coord, np.array([1.5, 10]))

    def test_ParallelPointPL(self):
        # 平行点测试
        p1 = FreePoint(np.array([-1, 3]))
        line = InfinityLinePP(FreePoint(np.array([0, 0])), FreePoint(np.array([1, 1])))
        parallel = ParallelPointPL(p1, line, np.sqrt(2))
        assert np.allclose(parallel.coord, np.array([0, 4]))

    def test_RotationPointPPA(self):
        # 固定角度旋转点测试
        pass

    def test_TranslationPointP(self):
        # 平移点测试
        point = FreePoint(np.array([2, 3]))
        vector = VectorPP(FreePoint(np.array([0, 0])), FreePoint(np.array([1, -1])))
        translated_point = TranslationPointP(point, vector)
        assert np.allclose(translated_point.coord, [3, 2])

        point = FreePoint(np.array([2, 3]))
        vector = VectorParam(np.array([1, -1]))
        translated_point = TranslationPointP(point, vector)
        assert np.allclose(translated_point.coord, [3, 2])

    def test_VerticalPointPL(self):
        # 垂足点测试
        line = InfinityLinePP(FreePoint(np.array([0, 0])), FreePoint(np.array([1, 0])))  # x轴
        point = FreePoint(np.array([3, 4]))
        foot = VerticalPointPL(point, line)
        assert np.allclose(foot.coord, np.array([3, 0]))  # 垂足为(3,0)

        line2 = InfinityLinePP(FreePoint(np.array([1, 1])), FreePoint(np.array([2, 2])))  # y=x
        point2 = FreePoint(np.array([3, 0]))
        foot2 = VerticalPointPL(point2, line2)
        assert np.allclose(foot2.coord, np.array([1.5, 1.5]))  # 投影到y=x的垂足
        