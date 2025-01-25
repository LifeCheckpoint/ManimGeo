# ManimGeo

**developing...**

ManimGeo 是一个用于简化 Manim 动画中创建几何图形及其依赖的辅助库。

## 特性

- 简化几何图形的创建 (正在做)
- 提供常用的几何操作 (做着呢)
- 兼容 Manim 的动画系统 (还没做)

单元测试也没做...

## 安装

使用 pip 安装：

```bash
pip install manimgeo
```

## 使用示例

```python
from manimgeo.components.points import FreePoint, MidPoint, ExtensionPoint, IntersectionPoint
from manimgeo.components.lines import LineSegment, Ray
from manimgeo.utils.utils import GeoUtils

import numpy as np

# 创建自由点
A = FreePoint(np.array([0, 0]), "A")
B = FreePoint(np.array([4, 0]), "B")
C = FreePoint(np.array([1, 3]), "C")

# 构造线段AB, BC, AC
AB = LineSegment(A, B, "AB")
BC = LineSegment(B, C, "BC")
AC = LineSegment(A, C, "AC")

# 创建中点M
M = MidPoint(AB, None, "M")

# 构造线段CM
CM = LineSegment(C, M, "CM")

# 创建延长点N, O
N = ExtensionPoint(C, M, factor=2.0, name="N")
O = ExtensionPoint(C, M, factor=3.0, name="O")

# 构造射线AN，交OB于P
AN = Ray(A, N, "AN")
OB = Ray(O, B, "OB")
P = IntersectionPoint(AN, OB, "P")

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
```
