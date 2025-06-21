# Utils

`GeoUtils` 提供了一系列工具函数

通过 `from manimgeo.utils import GeoUtils` 导入

---

### `GEO_PRINT_EXC` 标志位

bool, 标志几何对象计算出错时是否输出错误信息

---

### 检查参数数量与类型

#### `check_params(objs: Sequence, *expected_types)`

逐一检查参数是否为指定类型

**参数**:
 - `objs` (Sequence): 将要检查的参数序列
 - `expected_types`: 期望的参数类型序列，可以为 `None` 表示不检查

---

### 批量检查参数数量与类型

#### `check_params_batch(op_type_map: Dict[str, Sequence], op: str, objs: Sequence)`

类似于 `check_params`，通过字典批量检查，更简洁

---

### 统一几何对象名称设置

#### `get_name(default_name: str, obj, construct_type: str)`

统一对几何对象名称进行设置

 - `default_name` 非空，直接返回 `default_name`
 - `default_name` 为空，设置几何对象名称为 `TYPE[CONSTRUCT_TYPE]@[HASH]`
   - `TYPE`: 几何对象类型，例如 `Circle`
   - `CONSTRUCT_TYPE`: 几何对象构建方式，例如 `PPP`
   - `HASH`: 几何对象本体的内存摘要，`id(obj) % 10000`

---

### 展平嵌套序列

#### `flatten(iterable: Iterable)`

---

### 输出依赖关系

#### `print_dependencies(root: BaseGeometry, depth: int = 0, max_depth: int = 20)`

自上而下输出几何对象之间的依赖关系，相同对象将使用相同颜色标识

**参数**:
 - `root` (BaseGeometry): 根几何对象
 - `depth` (int): 当前深度
 - `max_depth` (int): 允许遍历的最大深度

---

### 错误信息输出设置

#### `set_debug(debug: bool = True)`

设置是否打开 `GEO_PRINT_EXC` 标志位

---