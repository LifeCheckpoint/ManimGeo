# ManimGeo - 几何动画辅助库

ManimGeo 是一个用于简化几何图形创建和动画生成的辅助库。它提供丰富的几何元素和操作，帮助快速构建复杂的几何场景。

*目前开发中，单元测试尚未完成，欢迎 PR！*

## 主要特性

- **几何元素创建**：支持点、线、圆、角等基本几何元素的创建
- **几何关系处理**：自动处理中点、垂足、交点等几何关系
- **几何变换**：支持反演等几何变换操作
- **依赖管理**：自动维护几何元素间的依赖关系
- **动画集成**：与 Manim 等动画系统的高集成

## 安装

使用 pip 安装：

```bash
pip install manimgeo
```

~~其实还没上传到 pypi~~

## 快速开始

### 纯几何构造

```python
from manimgeo import *

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
GeoUtils.geo_print_dependencies(A)
print("")

# 验证所有点都在九点圆上
for point in [AB_mid, BC_mid, AC_mid, AB_foot, BC_foot, AC_foot] + euler_points:
    point: Point
    r, c = nine_point_circle.radius, nine_point_circle.center
    assert np.isclose(r, np.linalg.norm(point.coord - c))

# 打印依赖关系
print("Dependencies of A:")
geo_print_dependencies(A)
```

### Manim 动画生成

```python
from manimlib import *
from manimgeo.components import *
from manimgeo.anime.manimgl import GeoManimGLManager

class EulerLine(Scene):
    def construct(self):
        # 构造三角形ABC
        A = PointFree(np.array([-5, -1]), "A")
        B = PointFree(np.array([3, -2]), "B")
        C = PointFree(np.array([2, 3]), "C")
        AB = LineSegmentPP(A, B, "AB")
        BC = LineSegmentPP(B, C, "BC")
        AC = LineSegmentPP(A, C, "AC")

        # 重心 垂心 外心
        CENTROID = PointCentroidPPP(A, B, C, "Centroid")
        ORTHOCENTER = PointOrthocenterPPP(A, B, C, "Orthocenter")
        CIRCUMCENTER = PointCircumcenterPPP(A, B, C, "Circumcenter")

        # 创建几何动画管理器
        gmm = GeoManimGLManager()
        
        # 创建 ManimGL VMobject 图形
        dot_a, dot_b, dot_c = gmm.create_mobjects_from_geometry([A, B, C])
        l_ab, l_bc, l_ac = gmm.create_mobjects_from_geometry([AB, BC, AC])
        dot_ct, dot_orth, dot_cir = gmm.create_mobjects_from_geometry([CENTROID, ORTHOCENTER, CIRCUMCENTER])

        text_ct = Text("Centroid", font="Arial").move_to(dot_ct.get_center() + 0.2*(UP + RIGHT)).scale(0.3)
        text_orth = Text("Orthocenter", font="Arial").move_to(dot_orth.get_center() + 0.2*(UP + RIGHT)).scale(0.3)
        text_cir = Text("Circumcenter", font="Arial").move_to(dot_cir.get_center() + 0.2*(UP + RIGHT)).scale(0.3)

        # 设置颜色
        def fit_color(*mobs: VMobject, hex_color: str = "#FFFFFF"):
            color = rgb_to_color(hex_to_rgb(hex_color))
            [mob.set_color(color) for mob in mobs]       

        fit_color(dot_a, dot_b, dot_c, l_ab, l_bc, l_ac, hex_color="#F9F871")
        fit_color(dot_ct, text_ct, hex_color="#FF9671")
        fit_color(dot_orth, text_orth, hex_color="#FF6F91")
        fit_color(dot_cir, text_cir, hex_color="#845EC2")

        # 添加到场景演示
        self.wait(1)
        self.play(Write(dot_a), Write(dot_b), Write(dot_c))
        self.play(Write(l_ab), Write(l_bc), Write(l_ac))
        self.play(Write(dot_ct), Write(text_ct))
        self.play(Write(dot_orth), Write(text_orth))
        self.play(Write(dot_cir), Write(text_cir))
        self.wait(1)
        
        text_ct.add_updater(lambda m: m.move_to(dot_ct.get_center() + 0.2*(UP + RIGHT)))
        text_orth.add_updater(lambda m: m.move_to(dot_orth.get_center() + 0.2*(UP + RIGHT)))
        text_cir.add_updater(lambda m: m.move_to(dot_cir.get_center() + 0.2*(UP + RIGHT)))

        # 在几何管理器下执行约束动画变换
        with gmm:
            now = self.time
            dot_a.add_updater(lambda m: m.shift(0.01 * UP * math.sin((self.time - now)*2.5)))
            dot_b.add_updater(lambda m: m.shift(0.01 * RIGHT * math.cos((self.time - now)*2)))
            dot_c.add_updater(lambda m: m.shift(0.005 * (UP + LEFT) * math.sin((self.time - now)*1.5)))
            self.wait(20)
```

```bash
manimgl tests\manimgl_anime\euler_line.py EulerLine
```

https://github.com/user-attachments/assets/36fec8c6-ad72-4b34-b9fc-f636a6808cfb
