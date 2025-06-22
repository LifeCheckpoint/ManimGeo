import numpy as np
from manimgeo.components import *
from manimgeo.utils import GeoUtils

def test_euler_line():
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