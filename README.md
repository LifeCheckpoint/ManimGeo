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

# 创建三角形ABC
A = FreePoint([0, 0], "A")
B = FreePoint([4, 0], "B") 
C = FreePoint([2, 3], "C")

# 构造边和中点
AB = LineSegmentPP(A, B, "AB")
M = MidPointL(AB, "M")

# 构造九点圆
nine_point_circle = CirclePPP(
    MidPointPP(A, B),
    MidPointPP(B, C),
    MidPointPP(A, C)
)

# 打印依赖关系
print("Dependencies of A:")
geo_print_dependencies(A)
```
