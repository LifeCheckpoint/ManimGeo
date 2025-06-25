import numpy as np
import pytest

from manimgeo.components import *

class TestPoint:
    def test_Free(self):
        point = Point.Free(np.array([114, 514, 0]))
        assert np.allclose(point.coord, np.array([114, 514, 0]))

    def test_AxisymmetricPL(self):
        # 对称点测试
        line = InfinityLine.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([1, 0, 0])))  # x轴
        point = Point.Free(np.array([2, 3, 0]))
        sym_point = Point.AxisymmetricPL(point, line)
        assert np.allclose(sym_point.coord, np.array(np.array([2, -3, 0])))  # 对称后应为(2,-3)

        line2 = InfinityLine.PP(Point.Free(np.array([1, 1, 0])), Point.Free(np.array([2, 2, 0])))  # 直线y=x
        point2 = Point.Free(np.array([3, 2, 0]))
        sym_point2 = Point.AxisymmetricPL(point2, line2)
        assert np.allclose(sym_point2.coord, np.array(np.array([2, 3, 0])))  # 关于y=x对称

    @pytest.mark.skip(reason="Not implemented")
    def test_ConstraintPoint(self):
        # 约束点测试
        pass

    def test_ExtensionPP(self):
        # 延长点测试
        A = Point.Free(np.array([0, 0, 0]))
        B = Point.Free(np.array([1, 1, 0]))
        extend_point = Point.ExtensionPP(A, B, 2)  # 延长到B之后，总长度2倍
        assert np.allclose(extend_point.coord, np.array([2, 2, 0]))

        C = Point.Free(np.array([3, 4, 0]))
        D = Point.Free(np.array([5, 7, 0]))
        extend_point2 = Point.ExtensionPP(C, D, -0.5)  # 反向，一半
        assert np.allclose(extend_point2.coord, np.array([2, 2.5, 0]))

    @pytest.mark.skip(reason="Not implemented yet")
    def test_IntersectionCirCir(self):
        # 两圆交点测试

        # 相交情况
        circle1 = Circle.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([1, 0, 0])))  # 圆心(0,0)，半径1
        circle2 = Circle.PP(Point.Free(np.array([1, 0, 0])), Point.Free(np.array([2, 0, 0])))  # 圆心(1,0)，半径1
        inter_points = Point.IntersectionCirCir(circle1, circle2)
        expected1 = np.array([0.5, np.sqrt(3)/2, 0])
        expected2 = np.array([0.5, -np.sqrt(3)/2, 0])
        assert (np.allclose(inter_points.coord1, expected1) or 
                np.allclose(inter_points.coord1, expected2))
        
        # 相切情况
        circle3 = Circle.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([2, 0, 0])))  # 半径2
        circle4 = Circle.PP(Point.Free(np.array([4, 0, 0])), Point.Free(np.array([2, 0, 0])))  # 圆心(4,0)，半径2
        inter_points2 = Point.IntersectionCirCir(circle3, circle4)
        assert np.allclose(inter_points2.coord1, [2, 0, 0])

        # 无交点情况 BUG
        circle5 = Circle.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([1, 0, 0])))
        circle6 = Circle.PP(Point.Free(np.array([3, 0, 0])), Point.Free(np.array([2, 0, 0])))
        try:
            Point.IntersectionCirCir(circle5, circle6)
            assert False, "Expected ValueError for no intersection"
        except ValueError:
            pass

    @pytest.mark.skip(reason="Not implemented yet")
    def test_IntersectionLCir(self):
        # 线圆交点测试
        
        # 线段与圆相交
        circle = Circle.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([1, 0, 0])))  # 单位圆
        line = LineSegment.PP(Point.Free(np.array([-2, 0, 0])), Point.Free(np.array([2, 0, 0])))  # x轴线段
        intersections = Point.IntersectionLCir(line, circle)
        assert (np.allclose(intersections.coord1, [1, 0, 0]) and \
               np.allclose(intersections.coord2, [-1, 0, 0])) or \
               (np.allclose(intersections.coord1, [-1, 0, 0]) and \
               np.allclose(intersections.coord2, [1, 0, 0]))

        # 射线与圆相切
        circle2 = Circle.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([1, 0, 0])))
        ray = RayPP(Point.Free(np.array([0, 1, 0])), Point.Free(np.array([1, 1, 0])))  # 水平射线y=1
        tangent_point = Point.IntersectionLCir(ray, circle2)
        assert np.allclose(tangent_point.coord1, [0, 1, 0]) and np.allclose(tangent_point.coord2, [0, 1, 0])

        # 无限直线不相交
        inf_line = InfinityLine.PP(Point.Free(np.array([3, 0, 0])), Point.Free(np.array([3, 1, 0])))  # x=3
        try:
            Point.IntersectionLCir(inf_line, circle)
            assert False, "Expected no intersection"
        except ValueError:
            pass

    def test_IntersectionLL(self):
        # 线线交点测试

        # 普通测试
        seg1 = LineSegment.PP(Point.Free(np.array([1, 1, 0])), Point.Free(np.array([2, 2, 0])))
        seg2 = LineSegment.PP(Point.Free(np.array([1, 2, 0])), Point.Free(np.array([2, 1, 0])))
        inter = Point.IntersectionLL(seg1, seg2)
        assert np.allclose(inter.coord, np.array([1.5, 1.5, 0]))

        ray1 = Ray.PP(Point.Free(np.array([1, 1, 0])), Point.Free(np.array([2, 2, 0])))
        ray2 = Ray.PP(Point.Free(np.array([3.5, -1, 0])), Point.Free(np.array([3.5, 0, 0])))
        inter = Point.IntersectionLL(ray1, ray2)
        assert np.allclose(inter.coord, np.array([3.5, 3.5, 0]))

        inf1 = InfinityLine.PP(Point.Free(np.array([1, 1, 0])), Point.Free(np.array([2, 2, 0])))
        inf2 = InfinityLine.PP(Point.Free(np.array([1, -1, 0])), Point.Free(np.array([2, -2, 0])))
        inter = Point.IntersectionLL(inf1, inf2)
        assert np.allclose(inter.coord, np.array([0, 0, 0]))

        # 无交点测试
        seg1 = LineSegment.PP(Point.Free(np.array([1, 1, 0])), Point.Free(np.array([2, 2, 0])))
        seg2 = LineSegment.PP(Point.Free(np.array([3, 4, 0])), Point.Free(np.array([4, 3, 0])))
        try:
            inter = Point.IntersectionLL(seg1, seg2)
            assert False, "Expected ValueError"
        except ValueError:
            pass

        ray1 = Ray.PP(Point.Free(np.array([1, 1, 0])), Point.Free(np.array([2, 2, 0])))
        ray2 = Ray.PP(Point.Free(np.array([3, 4, 0])), Point.Free(np.array([2, 5, 0])))
        try:
            inter = Point.IntersectionLL(ray1, ray2)
            assert False, "Expected ValueError"
        except ValueError:
            pass

        inf1 = InfinityLine.PP(Point.Free(np.array([1, 1, 0])), Point.Free(np.array([2, 2, 0])))
        inf2 = InfinityLine.PP(Point.Free(np.array([3, 3, 0])), Point.Free(np.array([4, 4, 0])))
        try:
            inter = Point.IntersectionLL(inf1, inf2)
            assert False, "Expected ValueError"
        except ValueError:
            pass

    def test_InversionPCir(self):
        # 反演点测试
        p1 = Point.Free(np.array([1, 2, 0]))
        circle = Circle.PR(Point.Free(np.array([0, 0, 0])), 1)
        inverted_point = Point.InversionPCir(p1, circle)
        assert np.allclose(inverted_point.coord, np.array([0.2, 0.4, 0]))

    def test_MidL(self):
        # 线段中点测试
        p1 = Point.Free(np.array([1, -3, 0]))
        p2 = Point.Free(np.array([17, -14, 0]))
        mid = Point.MidL(LineSegment.PP(p1, p2))
        assert np.allclose(mid.coord, np.array([9, -8.5, 0]))

    def test_MidPP(self):
        # 两点中点测试
        p1 = Point.Free(np.array([-1, 3, 0]))
        p2 = Point.Free(np.array([4, 17, 0]))
        mid = Point.MidPP(p1, p2)
        assert np.allclose(mid.coord, np.array([1.5, 10, 0]))

    def test_ParallelPL(self):
        # 平行点测试
        p1 = Point.Free(np.array([-1, 3, 0]))
        line = InfinityLine.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([1, 1, 0])))
        parallel = Point.ParallelPL(p1, line, np.sqrt(2))
        assert np.allclose(parallel.coord, np.array([0, 4, 0]))

    def test_RotationPPA(self):
        # 固定角度旋转点测试
        point = Point.Free(np.array([1, 2, 3]))
        center = Point.Free(np.array([1, 1, 4]))
        angle = Angle.N(np.pi / 4+0.5)
        axis = Vector.N(np.array([2, 1, -1]))
        rotated_point = Point.RotatePPA(point, center, angle, axis)
        expected_coord = np.array([
            1.195262145875635,
            2.382088123313991,
            3.772612415065261
        ])
        assert np.allclose(rotated_point.coord, expected_coord)

    def test_TranslationPV(self):
        # 平移点测试
        point = Point.Free(np.array([2, 3, 0]))
        vector = Vector.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([1, -1, 0])))
        translated_point = Point.TranslationPV(point, vector)
        assert np.allclose(translated_point.coord, [3, 2, 0])

        point = Point.Free(np.array([2, 3, 0]))
        vector = Vector.N(np.array([1, -1, 0]))
        translated_point = Point.TranslationPV(point, vector)
        assert np.allclose(translated_point.coord, [3, 2, 0])

    def test_VerticalPL(self):
        # 垂足点测试
        line = InfinityLine.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([1, 0, 0])))  # x轴
        point = Point.Free(np.array([3, 4, 0]))
        foot = Point.VerticalPL(point, line)
        assert np.allclose(foot.coord, np.array([3, 0, 0]))  # 垂足为(3,0)

        line2 = InfinityLine.PP(Point.Free(np.array([1, 1, 0])), Point.Free(np.array([2, 2, 0])))  # y=x
        point2 = Point.Free(np.array([3, 0, 0]))
        foot2 = Point.VerticalPL(point2, line2)
        assert np.allclose(foot2.coord, np.array([1.5, 1.5, 0]))  # 投影到y=x的垂足
        