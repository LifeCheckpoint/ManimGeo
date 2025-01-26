from manimgeo.components import *

import numpy as np

# 创建自由点
A = FreePoint(np.array([0, 0]), "A")
B = FreePoint(np.array([5, 0]), "B")
C = FreePoint(np.array([1, 3]), "C")
D = FreePoint(np.array([2, -1]), "D")

AB = InfinityLinePP(A, B, "AB")
BC = InfinityLinePP(B, C, "BC")

vl_d_ab, _ = VerticalInfinieLinePL(D, AB, "VL")
E = IntersectionPointLL(BC, vl_d_ab, "IE")

print(E.coord)

# 构造三点圆
circle = CirclePPP(E, D, C, "ThreePointCircle")
centerF, _ = CircumcenterPPP(circle, "CCF")

# geo_print_dependencies(A)
print(centerF.coord)