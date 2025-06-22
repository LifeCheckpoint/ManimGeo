# Utils

⚠ **文档可能含有未修复的过时部分**

`GeoUtils` 提供了一系列工具函数

通过 `from manimgeo.utils import GeoUtils` 导入

---

## `GEO_PRINT_EXC` 标志位

bool, 标志几何对象计算出错时是否输出错误信息

---

## 展平嵌套序列

### `flatten(iterable: Iterable)`

---

## 输出依赖关系

### `print_dependencies(root: BaseGeometry, depth: int = 0, max_depth: int = 20)`

自上而下输出几何对象之间的依赖关系，相同对象将使用相同颜色标识

**参数**:

- `root` (BaseGeometry): 根几何对象
- `depth` (int): 当前深度
- `max_depth` (int): 允许遍历的最大深度

---

## 错误信息输出设置

### `set_debug(debug: bool = True)`

设置是否打开 `GEO_PRINT_EXC` 标志位

---
