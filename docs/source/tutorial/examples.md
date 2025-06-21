# Examples

manimgeo 库的 `tests` 文件夹下提供了一些示例

```python title="简单几何搭建测试"
import numpy as np
from manimgeo.components import *
from manimgeo.utils import GeoUtils

# 创建自由点
A = PointFree(np.array([0, 0]), "A")
B = PointFree(np.array([4, 0]), "B")
C = PointFree(np.array([1, 3]), "C")

# 构造线段AB, BC, AC
AB = LineSegmentPP(A, B, "AB")
BC = LineSegmentPP(B, C, "BC")
AC = LineSegmentPP(A, C, "AC")

# 创建中点M
M = PointMidL(AB, "M")

# 构造线段CM
CM = LineSegmentPP(C, M, "CM")

# 创建延长点N, O
N = PointExtensionPP(C, M, factor=2.0, name="N")
O = PointExtensionPP(C, M, factor=3.0, name="O")

# 构造射线AN，交OB于P
AN = RayPP(A, N, "AN")
OB = RayPP(O, B, "OB")
P = PointIntersectionLL(AN, OB, False, "P")

# 打印 A 依赖关系
print("Dependencies of A:")
GeoUtils.print_dependencies(A)
print("")

# 输出移动前坐标
print("Before moving B:")
print(f"{P.name}: {P.coord}")
assert np.allclose(P.coord, np.array([4, -4]))

# 移动B
B.set_coord(np.array([5, 0]))

# 输出移动后坐标
print("After moving P:")
print(f"{P.name}: {P.coord}")
assert np.allclose(P.coord, np.array([16/3, -4]))
```

```python title="九点共圆"
import numpy as np
from manimgeo.components import *
from manimgeo.utils import GeoUtils

# 构造三角形ABC
A = PointFree(np.array([0, 0]), "A")
B = PointFree(np.array([5, 0]), "B")
C = PointFree(np.array([2, 3]), "C")
print(f"顶点 {A.name} 坐标: {A.coord}")
print(f"顶点 {B.name} 坐标: {B.coord}")
print(f"顶点 {C.name} 坐标: {C.coord}")

# 构造中点
AB_mid = PointMidPP(A, B, "AB_mid")
BC_mid = PointMidPP(B, C, "BC_mid")
AC_mid = PointMidPP(A, C, "AC_mid")
print(f"中点 {AB_mid.name} 坐标: {AB_mid.coord}")
print(f"中点 {BC_mid.name} 坐标: {BC_mid.coord}")
print(f"中点 {AC_mid.name} 坐标: {AC_mid.coord}")

# 构造边
AB = LineSegmentPP(A, B, "AB")
BC = LineSegmentPP(B, C, "BC")
AC = LineSegmentPP(A, C, "AC")

# 构造垂足
AB_foot = PointVerticalPL(C, AB, "AB_foot")
BC_foot = PointVerticalPL(A, BC, "BC_foot")
AC_foot = PointVerticalPL(B, AC, "AC_foot")
print(f"垂足 {AB_foot.name} 坐标: {AB_foot.coord}")
print(f"垂足 {BC_foot.name} 坐标: {BC_foot.coord}")
print(f"垂足 {AC_foot.name} 坐标: {AC_foot.coord}")

# 构造欧拉点
orthocenter = PointIntersectionLL(
    InfinityLinePP(AB_foot, C),
    InfinityLinePP(BC_foot, A), 
    True,
    "Orthocenter"
)
euler_points = [
    PointMidPP(A, orthocenter, "A_orthocenter_mid"),
    PointMidPP(B, orthocenter, "B_orthocenter_mid"),
    PointMidPP(C, orthocenter, "C_orthocenter_mid")
]
print(f"垂心 {orthocenter.name} 坐标: {orthocenter.coord}")
for point in euler_points:
    print(f"欧拉点 {point.name} 坐标: {point.coord}")

# 构造九点圆
nine_point_circle = CirclePPP(AB_mid, BC_mid, AC_mid, "NinePointCircle")
print(f"九点圆 {nine_point_circle.name} 半径: {nine_point_circle.radius} 圆心: {nine_point_circle.center}")

# 打印依赖关系
print("Dependencies of A:")
GeoUtils.print_dependencies(A)
print("")

# 验证所有点都在九点圆上
for point in [AB_mid, BC_mid, AC_mid, AB_foot, BC_foot, AC_foot] + euler_points:
    point: Point
    r, c = nine_point_circle.radius, nine_point_circle.center
    assert np.isclose(r, np.linalg.norm(point.coord - c))
```

🚧施工中