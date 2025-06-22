# Examples

这里是 `manimgeo` 的一些示例

```python title="简单几何搭建测试"
# 简单几何搭建测试
import numpy as np
from manimgeo.components import *
from manimgeo.utils import GeoUtils

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
    GeoUtils.print_dependencies(B)
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
```

---

```python title="西姆松线"
# 西姆松线
import numpy as np
from manimgeo.components import *
from manimgeo.utils import GeoUtils

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
    GeoUtils.print_dependencies(A)
    print("")

    # 验证三点共线
    vectors = np.array([
        foot_AB.coord - foot_BC.coord,
        foot_BC.coord - foot_CA.coord
    ])
    assert np.linalg.matrix_rank(vectors) == 1, "西姆松线三点不共线"
```

---

```python title="九点共圆"
# 九点共圆
import numpy as np
from manimgeo.components import *
from manimgeo.utils import GeoUtils

def test_nine_point_circle():
    # 构造三角形ABC
    A = Point.Free(np.array([0, 0, 0]), "A")
    B = Point.Free(np.array([5, 0, 0]), "B")
    C = Point.Free(np.array([2, 3, 0]), "C")
    print(f"顶点 {A.name} 坐标: {A.coord}")
    print(f"顶点 {B.name} 坐标: {B.coord}")
    print(f"顶点 {C.name} 坐标: {C.coord}")

    # 构造中点
    AB_mid = Point.MidPP(A, B, "AB_mid")
    BC_mid = Point.MidPP(B, C, "BC_mid")
    AC_mid = Point.MidPP(A, C, "AC_mid")
    print(f"中点 {AB_mid.name} 坐标: {AB_mid.coord}")
    print(f"中点 {BC_mid.name} 坐标: {BC_mid.coord}")
    print(f"中点 {AC_mid.name} 坐标: {AC_mid.coord}")

    # 构造边
    AB = LineSegment.PP(A, B, "AB")
    BC = LineSegment.PP(B, C, "BC")
    AC = LineSegment.PP(A, C, "AC")

    # 构造垂足
    AB_foot = Point.VerticalPL(C, AB, "AB_foot")
    BC_foot = Point.VerticalPL(A, BC, "BC_foot")
    AC_foot = Point.VerticalPL(B, AC, "AC_foot")
    print(f"垂足 {AB_foot.name} 坐标: {AB_foot.coord}")
    print(f"垂足 {BC_foot.name} 坐标: {BC_foot.coord}")
    print(f"垂足 {AC_foot.name} 坐标: {AC_foot.coord}")

    # 构造欧拉点
    orthocenter = Point.IntersectionLL(
        InfinityLine.PP(AB_foot, C),
        InfinityLine.PP(BC_foot, A), 
        True,
        "Orthocenter"
    )
    euler_points = [
        Point.MidPP(A, orthocenter, "A_orthocenter_mid"),
        Point.MidPP(B, orthocenter, "B_orthocenter_mid"),
        Point.MidPP(C, orthocenter, "C_orthocenter_mid")
    ]
    print(f"垂心 {orthocenter.name} 坐标: {orthocenter.coord}")
    for point in euler_points:
        print(f"欧拉点 {point.name} 坐标: {point.coord}")

    # 构造九点圆
    nine_point_circle = Circle.PPP(AB_mid, BC_mid, AC_mid, "NinePointCircle")
    print(f"九点圆 {nine_point_circle.name} 半径: {nine_point_circle.radius} 圆心: {nine_point_circle.center}")

    # 打印依赖关系
    print("Dependencies of A:")
    GeoUtils.print_dependencies(A)
    print("")

    # 验证所有点都在九点圆上
    for geometry_point in [AB_mid, BC_mid, AC_mid, AB_foot, BC_foot, AC_foot] + euler_points:
        geometry_point: Point
        r, c = nine_point_circle.radius, nine_point_circle.center
        assert np.isclose(r, np.linalg.norm(geometry_point.coord - c))
```

🚧施工中
