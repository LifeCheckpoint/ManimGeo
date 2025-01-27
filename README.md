# ManimGeo - 几何动画辅助库

ManimGeo 是一个用于简化几何图形创建和动画生成的辅助库。它提供了丰富的几何元素和操作，帮助快速构建复杂的几何场景。

## 主要特性

- **几何元素创建**：支持点、线、圆、角等基本几何元素的创建
- **几何关系处理**：自动处理中点、垂足、交点等几何关系
- **几何变换**：支持反演等几何变换操作
- **依赖管理**：自动维护几何元素间的依赖关系
- **动画集成**：与 Manim 动画系统无缝集成

## 安装

使用 pip 安装：

```bash
pip install manimgeo
```

## 快速开始

```python
from manimgeo import *

# 构造三角形ABC
A = FreePoint(np.array([0, 0]), "A")
B = FreePoint(np.array([5, 0]), "B")
C = FreePoint(np.array([2, 3]), "C")
print(f"顶点 {A.name} 坐标: {A.coord}")
print(f"顶点 {B.name} 坐标: {B.coord}")
print(f"顶点 {C.name} 坐标: {C.coord}")

# 构造中点
AB_mid = MidPointPP(A, B, "AB_mid")
BC_mid = MidPointPP(B, C, "BC_mid")
AC_mid = MidPointPP(A, C, "AC_mid")
print(f"中点 {AB_mid.name} 坐标: {AB_mid.coord}")
print(f"中点 {BC_mid.name} 坐标: {BC_mid.coord}")
print(f"中点 {AC_mid.name} 坐标: {AC_mid.coord}")

# 构造边
AB = LineSegmentPP(A, B, "AB")
BC = LineSegmentPP(B, C, "BC")
AC = LineSegmentPP(A, C, "AC")

# 构造垂足
AB_foot = VerticalPointPL(C, AB, "AB_foot")
BC_foot = VerticalPointPL(A, BC, "BC_foot")
AC_foot = VerticalPointPL(B, AC, "AC_foot")
print(f"垂足 {AB_foot.name} 坐标: {AB_foot.coord}")
print(f"垂足 {BC_foot.name} 坐标: {BC_foot.coord}")
print(f"垂足 {AC_foot.name} 坐标: {AC_foot.coord}")

# 构造欧拉点
orthocenter = IntersectionPointLL(
    InfinityLinePP(AB_foot, C),
    InfinityLinePP(BC_foot, A), 
    "Orthocenter"
)
print(f"垂心 {orthocenter.name} 坐标: {orthocenter.coord}")
euler_points = [
    MidPointPP(A, orthocenter, "A_orthocenter_mid"),
    MidPointPP(B, orthocenter, "B_orthocenter_mid"),
    MidPointPP(C, orthocenter, "C_orthocenter_mid")
]
for point in euler_points:
    print(f"欧拉点 {point.name} 坐标: {point.coord}")

# 构造九点圆
nine_point_circle = CirclePPP(AB_mid, BC_mid, AC_mid, "NinePointCircle")
print(f"九点圆 {nine_point_circle.name} 半径与圆心: {nine_point_circle.radius_and_center}")

# 打印依赖关系
print("Dependencies of A:")
geo_print_dependencies(A)
print("")

# 验证所有点都在九点圆上
for point in [AB_mid, BC_mid, AC_mid, AB_foot, BC_foot, AC_foot] + euler_points:
    point: PointLike
    r, c = nine_point_circle.radius_and_center
    assert np.isclose(r, np.linalg.norm(point.coord - c))

# 打印依赖关系
print("Dependencies of A:")
geo_print_dependencies(A)
```
