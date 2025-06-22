# 快速开始

## 几何搭建示例

为了快速认识 ManimGeo，你可以在文件夹内新建一个文件 `euler_line.py`，然后将以下代码粘贴到你的文件内

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
print("")

# 验证三点共线
vectors = np.array([
    centroid - orthocenter,
    circumcenter - orthocenter
])
rank = np.linalg.matrix_rank(vectors)
assert rank == 1
```

接下来，运行这个程序

```shell
python euler_line.py
```

接下来你应该会看到如下输出：

```plaintext
A: [0 0]
B: [5 0]
C: [2 3]
AB: [0 0] -> [5 0]
BC: [5 0] -> [2 3]
AC: [0 0] -> [2 3]
Centroid: [2.33333333 1.        ]
Orthocenter: [2. 2.]
Circumcenter: [2.5 0.5]

Dependencies of A:
· Point - (A)
  · InfinityLine - (AB)
  · InfinityLine - (AC)
  · Point - (Centroid)
  · Point - (Orthocenter)
  · Point - (Circumcenter)

rank == 1: True
```

这行代码的作用是：**验证三角形的重心、垂心与外心三点共线**

然后，我们具体看一下这段代码干了什么：

---

```python title="导入相关依赖" {2,3}
import numpy as np
from manimgeo.components import *
from manimgeo.utils import GeoUtils
```

以上三行导入了相关依赖：`NumPy` 和 `ManimGeo`，前者帮助我们创建数组、进行计算，后者帮助我们创建几何图形。

:::tip 一次性导入所有需要的几何组件
ManimGeo 的几何组件分布在 `components` 的各个子文件夹中，但是通过 `from manimgeo.components import *` 便可以全部导入
:::

---

```python title="构造点" {2,3,4}
# 构造三角形ABC
A = Point.Free(np.array([0, 0]), "A")
B = Point.Free(np.array([5, 0]), "B")
C = Point.Free(np.array([2, 3]), "C")
```

以上四行创建了最基本的几何图形：**自由点 (PointFree)**，“自由”意味着这些点是人工构建的、整个几何搭建的开始，传入**坐标**与**名称**完成创建

我们不直接通过向 `Point` 类传参来构建点，而是使用 `Point.Free` 这个个**工厂方法**

原因在于，一个点的构建方式是无穷无尽的（e.g. 线段中点、交点、...），而 `Point.Free` 方法则帮我们隐藏了具体构建的细节，我们只用关心它返回了一个 Point 对象

由此，现在我们创建了以下三点：

- $A\,(0, 0)$
- $B\,(5, 0)$
- $C\,(2, 3)$

> ℹ 关于几何组件
> ManimGeo 的几何组件都拥有 `name` 这一参数，创建合适的名称可以方便调试与理解

---

```python title="输出点坐标" {1}
[print(f"{P.name}: {P.coord}") for P in [A, B, C]]
```

这一行的作用是，通过访问每个点的 `name` 属性与 `coord` 属性，输出每个点的名称与坐标，即对应了以下输出

```plaintext
A: [0 0]
B: [5 0]
C: [2 3]
```

---

```python title="构造边" {2,3,4}
# 构造边
AB = LineSegment.PP(A, B, "AB")
BC = LineSegment.PP(B, C, "BC")
AC = LineSegment.PP(A, C, "AC")
```

上面这四行构造了 $\triangle ABC$ 的三条边，每条边都由两点构成

注意到我们这里使用的，用于构造线段的工厂函数是 `PP`，它表示构造几何对象的方式（两点构造线段，Point & Point）

`PP` 会返回一个 `LineSegment` 类的对象，这就是创建好的线段

---

```python title="输出线段信息" {1}
[print(f"{L.name}: {L.start} -> {L.end}") for L in [AB, BC, AC]]
```

上面一行输出了三条线段的信息，`start`、`end` 表示线段的起点和终点坐标

```plaintext
AB: [0 0] -> [5 0]
BC: [5 0] -> [2 3]
AC: [0 0] -> [2 3]
```

---

```python title="重心，垂心与外心" {1,2,3,5}
CENTROID = Point.CentroidPPP(A, B, C, "Centroid")
ORTHOCENTER = Point.OrthocenterPPP(A, B, C, "Orthocenter")
CIRCUMCENTER = Point.CircumcenterPPP(A, B, C, "Circumcenter")

[print(f"{P.name}: {P.coord}") for P in [CENTROID, ORTHOCENTER, CIRCUMCENTER]]
```

上面这五行，创建了三角形的重心，垂心与外心，然后输出了它们的坐标

```plaintext
Centroid: [2.33333333 1.        ]
Orthocenter: [2. 2.]
Circumcenter: [2.5 0.5]
```

---

```python title="输出依赖关系" {3}
# 测试依赖关系
print("\nDependencies of A:")
GeoUtils.print_dependencies(A)
print("")
```

上面三行输出了点 $A$ 的依赖信息：

```
Dependencies of A:
· Point - (A)
  · InfinityLine - (AB)
  · InfinityLine - (AC)
  · Point - (Centroid)
  · Point - (Orthocenter)
  · Point - (Circumcenter)
```

这幅图描述了以下决定关系：

- $A$ 的位置决定了线段 $AB$、$AC$ 的位置
- $A$ 的位置决定了点 $Centroid$、$Orthocenter$ 和 $Circumcenter$ 的位置

有了这种依赖关系，ManimGeo 就能根据上游组件的信息，自上而下自动计算出每个几何对象的信息，避免了人工计算的繁琐

<br />
<br />

```python title="三点共线验证" {2,3,4,5,6,7}
# 验证三点共线
vectors = np.array([
    CENTROID.coord - ORTHOCENTER.coord,
    CIRCUMCENTER.coord - ORTHOCENTER.coord
])
rank = np.linalg.matrix_rank(vectors)
print(f"rank == 1: {rank == 1}")
```

以上七行，首先构建了重心，垂心与外心两两之间的向量，然后组合为矩阵，通过计算矩阵的秩判断这三点是否共线。输出：

```plaintext
rank == 1: True
```

即，矩阵不满秩，三点共线

## 动画演示示例

🚧施工中