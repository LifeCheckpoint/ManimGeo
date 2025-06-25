import numpy as np
from manimgeo.components import *
from manimgeo.utils.utils import print_dependencies

def test_simple2():
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

    print_dependencies(A)
    print(centerF.coord)
    assert np.allclose(centerF.coord, np.array([0, 0.625, 0]))