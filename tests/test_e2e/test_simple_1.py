import numpy as np
from manimgeo.components import *
from manimgeo.utils.utils import print_dependencies

def test_simple1():
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
    print("Dependencies of B:")
    print_dependencies(B)
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