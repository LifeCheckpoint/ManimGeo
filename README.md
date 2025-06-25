# ManimGeo - 几何构建与动画辅助库

ManimGeo 是一个基于 Numpy 等强大核心的几何构建库，旨在简化几何图形的构建、管理和动画生成、帮助创建复杂的几何场景，并自动处理几何元素之间的依赖关系，确保在任何基础元素发生变化时，整个几何系统都能保持一致性。

## ✨ 主要特性

- **智能几何构建**: 支持点、线、圆、角、向量等多种基本几何元素的创建，并提供多种构造方式（如自由点、中点、交点等）。
- **自动依赖管理**: 核心“三位一体”架构（Base, Args, Adapter）确保几何对象之间的依赖关系被自动维护。当上游几何对象发生变化时，所有依赖它的下游对象都会自动更新。
- **灵活的几何变换**: 支持反演等几何变换操作，为复杂的几何探索提供便利。
- **高度可扩展性**: 清晰的架构设计使得添加新的几何类型或构造方法变得简单。
- **动画引擎集成 (developing)**: 旨在与 ManimGL 和 JAnim 等动画库无缝集成，将构建的几何场景轻松转化为动态演示。

## 🚀 快速开始

通过一个简单的欧拉线示例了解 ManimGeo 如何构建几何图形并管理依赖：

```python title="euler_line.py"
import numpy as np
from manimgeo.components import *
from manimgeo.utils import GeoUtils

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

# 验证三点共线
vectors = np.array([
    centroid - orthocenter,
    circumcenter - orthocenter
])
rank = np.linalg.matrix_rank(vectors)
assert rank == 1
print(f"rank == 1: {rank == 1}")
```

运行此代码，你将看到三角形的重心、垂心和外心被计算出来，并且验证了它们三点共线。

同时，你可以观察到 ManimGeo 如何自动管理这些几何对象之间的依赖关系。

## 📦 安装

ManimGeo 库要求的最低 Python 版本是 `3.12`。

### 使用 pip

```bash
# 仅安装核心库（数值计算和几何构建）
pip install manimgeo

# 安装 ManimGL 集成
pip install manimgeo[manim]

# 安装 JAnim 集成 (要求 janim[gui] >= 3.4.0)
pip install manimgeo[janim]

# 安装开发与测试工具
pip install manimgeo[dev]

# 安装所有功能
pip install manimgeo[full]
```

### 使用 uv (推荐)

如果尚未安装 `uv`，请先安装：

```bash
pip install uv
uv --version
```

然后，在你的项目目录中创建虚拟环境并安装 ManimGeo：

```bash
mkdir your/project/dir
cd your/project/dir
uv init
uv add manimgeo # 仅核心
uv add manimgeo --extra full # 安装所有功能
```

## 📐 核心架构

ManimGeo 的核心设计理念是“三位一体”：

- **`BaseGeometry` (基础几何对象)**: 代表几何实体本身（如 `Point`, `Line`, `Circle`），管理对象的属性、名称以及与其他几何对象之间的依赖关系。
- **`Args` (参数模型)**: 定义了如何构造一个几何对象。每个几何对象都可以通过多种方式构造（例如，一个点可以是自由的，也可以是两条线的交点）。`Args` 模型封装了这些构造方法所需的输入参数，并能识别出这些参数中包含的其它几何对象依赖。
- **`Adapter` (适配器)**: 连接 `Args` 和 `Base` 的桥梁。它根据 `Args` 中定义的构造方式和参数，执行具体的几何计算，并将计算结果适配到 `Base` 几何对象的属性上。

这种架构使得 ManimGeo 能够构建一个动态的、相互关联的几何对象网络，并实现高效的依赖管理和自动更新机制。

## 🎬 动画集成

ManimGeo 旨在与动画库（如 ManimGL 和 JAnim）无缝协作，将构建的几何场景转化为动画。

样例展示：

https://github.com/user-attachments/assets/36fec8c6-ad72-4b34-b9fc-f636a6808cfb

https://github.com/user-attachments/assets/b47f8a04-351a-42b2-8f1a-f4bcf2d0d79f

https://github.com/user-attachments/assets/e94ea012-1053-4585-82dd-058d04feb9ac

**developing**: 动画集成重构中，敬请期待

## 📚 项目文档

更详细的文档、API 参考和高级用法，请访问：
[ManimGeo 文档](https://manimgeo.readthedocs.io/zh-cn/latest/)

## 🤝 贡献

欢迎所有形式的贡献！如果您有任何建议、功能请求或发现 Bug，请随时提交 Issue 或 Pull Request。

## 📄 许可证

本项目采用 MIT 许可证。
