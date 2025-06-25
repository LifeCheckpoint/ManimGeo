import numpy as np
from manimgeo.components import *
from manimgeo.utils.utils import print_dependencies

def test_simson_line():
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
    print_dependencies(A)
    print("")

    # 验证三点共线
    vectors = np.array([
        foot_AB.coord - foot_BC.coord,
        foot_BC.coord - foot_CA.coord
    ])
    assert np.linalg.matrix_rank(vectors) == 1, "西姆松线三点不共线"