import numpy as np
import math
import sys
sys.path.append("D://wroot//ManimGeo//src") # 使用绝对路径避免测试路径问题

from manimgeo.components import *

class TestPoint:
    def test_PointFree(self):
        point = PointFree(np.array([114, 514]))
        assert np.allclose(point.coord, np.array([114, 514]))

    def test_AxisymmetricPointPL(self):
        # 对称点测试
        line = InfinityLinePP(PointFree(np.array([0, 0])), PointFree(np.array([1, 0])))  # x轴
        point = PointFree(np.array([2, 3]))
        sym_point = PointAxisymmetricPL(point, line)
        assert np.allclose(sym_point.coord, np.array(np.array([2, -3])))  # 对称后应为(2,-3)

        line2 = InfinityLinePP(PointFree(np.array([1, 1])), PointFree(np.array([2, 2])))  # 直线y=x
        point2 = PointFree(np.array([3, 2]))
        sym_point2 = PointAxisymmetricPL(point2, line2)
        assert np.allclose(sym_point2.coord, np.array(np.array([2, 3])))  # 关于y=x对称

    def test_ConstraintPoint(self):
        # 约束点测试
        pass

    def test_ExtensionPointPP(self):
        # 延长点测试
        A = PointFree(np.array([0, 0]))
        B = PointFree(np.array([1, 1]))
        extend_point = PointExtensionPP(A, B, 2)  # 延长到B之后，总长度2倍
        assert np.allclose(extend_point.coord, np.array([2, 2]))

        C = PointFree(np.array([3, 4]))
        D = PointFree(np.array([5, 7]))
        extend_point2 = PointExtensionPP(C, D, -0.5)  # 反向，一半
        assert np.allclose(extend_point2.coord, np.array([2, 2.5]))

    def test_IntersectionPointCirCir(self):
        # 两圆交点测试

        # 相交情况
        circle1 = CirclePP(PointFree(np.array([0, 0])), PointFree(np.array([1, 0])))  # 圆心(0,0)，半径1
        circle2 = CirclePP(PointFree(np.array([1, 0])), PointFree(np.array([2, 0])))  # 圆心(1,0)，半径1
        inter_points = Points2IntersectionCirCir(circle1, circle2)
        expected1 = np.array([0.5, math.sqrt(3)/2])
        expected2 = np.array([0.5, -math.sqrt(3)/2])
        assert (np.allclose(inter_points.coord1, expected1) or 
                np.allclose(inter_points.coord1, expected2))
        
        # 相切情况
        circle3 = CirclePP(PointFree(np.array([0, 0])), PointFree(np.array([2, 0])))  # 半径2
        circle4 = CirclePP(PointFree(np.array([4, 0])), PointFree(np.array([2, 0])))  # 圆心(4,0)，半径2
        inter_points2 = Points2IntersectionCirCir(circle3, circle4)
        assert np.allclose(inter_points2.coord1, [2, 0])

        # 无交点情况 BUG
        circle5 = CirclePP(PointFree(np.array([0, 0])), PointFree(np.array([1, 0])))
        circle6 = CirclePP(PointFree(np.array([3, 0])), PointFree(np.array([2, 0])))
        try:
            Points2IntersectionCirCir(circle5, circle6)
            assert False, "Expected ValueError for no intersection"
        except ValueError:
            pass

    def test_IntersectionPointLCir(self):
        # 线圆交点测试
        
        # 线段与圆相交
        circle = CirclePP(PointFree(np.array([0, 0])), PointFree(np.array([1, 0])))  # 单位圆
        line = LineSegmentPP(PointFree(np.array([-2, 0])), PointFree(np.array([2, 0])))  # x轴线段
        intersections = Points2IntersectionLCir(line, circle)
        assert (np.allclose(intersections.coord1, [1, 0]) and \
               np.allclose(intersections.coord2, [-1, 0])) or \
               (np.allclose(intersections.coord1, [-1, 0]) and \
               np.allclose(intersections.coord2, [1, 0]))

        # 射线与圆相切
        circle2 = CirclePP(PointFree(np.array([0, 0])), PointFree(np.array([1, 0])))
        ray = RayPP(PointFree(np.array([0, 1])), PointFree(np.array([1, 1])))  # 水平射线y=1
        tangent_point = Points2IntersectionLCir(ray, circle2)
        assert np.allclose(tangent_point.coord1, [0, 1]) and np.allclose(tangent_point.coord2, [0, 1])

        # 无限直线不相交
        inf_line = InfinityLinePP(PointFree(np.array([3, 0])), PointFree(np.array([3, 1])))  # x=3
        try:
            Points2IntersectionLCir(inf_line, circle)
            assert False, "Expected no intersection"
        except ValueError:
            pass

    def test_IntersectionPointLL(self):
        # 线线交点测试

        # 普通测试
        seg1 = LineSegmentPP(PointFree(np.array([1, 1])), PointFree(np.array([2, 2])))
        seg2 = LineSegmentPP(PointFree(np.array([1, 2])), PointFree(np.array([2, 1])))
        inter = PointIntersectionLL(seg1, seg2)
        assert np.allclose(inter.coord, np.array([1.5, 1.5]))

        ray1 = RayPP(PointFree(np.array([1, 1])), PointFree(np.array([2, 2])))
        ray2 = RayPP(PointFree(np.array([3.5, -1])), PointFree(np.array([3.5, 0])))
        inter = PointIntersectionLL(ray1, ray2)
        assert np.allclose(inter.coord, np.array([3.5, 3.5]))

        inf1 = InfinityLinePP(PointFree(np.array([1, 1])), PointFree(np.array([2, 2])))
        inf2 = InfinityLinePP(PointFree(np.array([1, -1])), PointFree(np.array([2, -2])))
        inter = PointIntersectionLL(inf1, inf2)
        assert np.allclose(inter.coord, np.array([0, 0]))

        # 无交点测试 BUG
        seg1 = LineSegmentPP(PointFree(np.array([1, 1])), PointFree(np.array([2, 2])))
        seg2 = LineSegmentPP(PointFree(np.array([3, 4])), PointFree(np.array([4, 3])))
        try:
            inter = PointIntersectionLL(seg1, seg2)
            assert False, "Expected ValueError"
        except ValueError:
            pass

        ray1 = RayPP(PointFree(np.array([1, 1])), PointFree(np.array([2, 2])))
        ray2 = RayPP(PointFree(np.array([3, 4])), PointFree(np.array([2, 5])))
        try:
            inter = PointIntersectionLL(ray1, ray2)
            assert False, "Expected ValueError"
        except ValueError:
            pass

        inf1 = InfinityLinePP(PointFree(np.array([1, 1])), PointFree(np.array([2, 2])))
        inf2 = InfinityLinePP(PointFree(np.array([3, 3])), PointFree(np.array([4, 4])))
        try:
            inter = PointIntersectionLL(inf1, inf2)
            assert False, "Expected ValueError"
        except ValueError:
            pass

    def test_InversionPointPCir(self):
        # 反演点测试
        pass

    def test_MidPointL(self):
        # 线段中点测试
        p1 = PointFree(np.array([1, -3]))
        p2 = PointFree(np.array([17, -14]))
        mid = PointMidL(LineSegmentPP(p1, p2))
        assert np.allclose(mid.coord, np.array([9, -8.5]))

    def test_MidPointPP(self):
        # 两点中点测试
        p1 = PointFree(np.array([-1, 3]))
        p2 = PointFree(np.array([4, 17]))
        mid = PointMidPP(p1, p2)
        assert np.allclose(mid.coord, np.array([1.5, 10]))

    def test_ParallelPointPL(self):
        # 平行点测试
        p1 = PointFree(np.array([-1, 3]))
        line = InfinityLinePP(PointFree(np.array([0, 0])), PointFree(np.array([1, 1])))
        parallel = PointParallelPL(p1, line, np.sqrt(2))
        assert np.allclose(parallel.coord, np.array([0, 4]))

    def test_RotationPointPPA(self):
        # 固定角度旋转点测试
        pass

    def test_TranslationPointP(self):
        # 平移点测试
        point = PointFree(np.array([2, 3]))
        vector = VectorPP(PointFree(np.array([0, 0])), PointFree(np.array([1, -1])))
        translated_point = PointTranslationPV(point, vector)
        assert np.allclose(translated_point.coord, [3, 2])

        point = PointFree(np.array([2, 3]))
        vector = VectorN(np.array([1, -1]))
        translated_point = PointTranslationPV(point, vector)
        assert np.allclose(translated_point.coord, [3, 2])

    def test_VerticalPointPL(self):
        # 垂足点测试
        line = InfinityLinePP(PointFree(np.array([0, 0])), PointFree(np.array([1, 0])))  # x轴
        point = PointFree(np.array([3, 4]))
        foot = PointVerticalPL(point, line)
        assert np.allclose(foot.coord, np.array([3, 0]))  # 垂足为(3,0)

        line2 = InfinityLinePP(PointFree(np.array([1, 1])), PointFree(np.array([2, 2])))  # y=x
        point2 = PointFree(np.array([3, 0]))
        foot2 = PointVerticalPL(point2, line2)
        assert np.allclose(foot2.coord, np.array([1.5, 1.5]))  # 投影到y=x的垂足
        