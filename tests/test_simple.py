from manimgeo.components.points import FreePoint, MidPointL, ExtensionPointPP, IntersectionPointLL
from manimgeo.components.lines import LineSegmentPP, RayPP
from manimgeo.utils.utils import GeoUtils

import numpy as np

# 创建自由点
A = FreePoint(np.array([0, 0]), "A")
B = FreePoint(np.array([4, 0]), "B")
C = FreePoint(np.array([1, 3]), "C")

# 构造线段AB, BC, AC
AB = LineSegmentPP(A, B, "AB")
BC = LineSegmentPP(B, C, "BC")
AC = LineSegmentPP(A, C, "AC")

# 创建中点M
M = MidPointL(AB, "M")

# 构造线段CM
CM = LineSegmentPP(C, M, "CM")

# 创建延长点N, O
N = ExtensionPointPP(C, M, factor=2.0, name="N")
O = ExtensionPointPP(C, M, factor=3.0, name="O")

# 构造射线AN，交OB于P
AN = RayPP(A, N, "AN")
OB = RayPP(O, B, "OB")
P = IntersectionPointLL(AN, OB, "P")

# 打印 P 依赖关系
print("Dependencies of A:")
GeoUtils.print_dependencies(A)
print("")

# 输出移动前坐标
print("Before moving B:")
print(f"{P.name}: {P.coord}")

# 移动B时的级联更新
B.coord = np.array([5, 0])

# 输出移动后坐标
print("After moving P:")
print(f"{P.name}: {P.coord}")
