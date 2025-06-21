# Vector

**`Vector` 类支持加法、减法与数乘**


## 1. 通过两点构造向量

#### `VectorPP(start: Point, end: Point, name: str = "")`
通过起点和终点构造一个向量。

**参数**:
- `start` (Point): 向量的起点。
- `end` (Point): 向量的终点。
- `name` (str, 可选): 向量的名称，默认为空字符串。

**返回值**:
- `Vector`: 返回通过两点构造的向量对象。


## 2. 通过线段构造向量

#### `VectorL(line: LineSegment, name: str = "")`
通过线段构造向量，线段的起点和终点分别作为向量的起点和终点。

**参数**:
- `line` (LineSegment): 线段对象，用来构造向量。
- `name` (str, 可选): 向量的名称，默认为空字符串。

**返回值**:
- `Vector`: 返回通过线段构造的向量对象。


## 3. 通过数值构造向量

#### `VectorN(vec: np.ndarray, name: str = "")`
通过一个给定的数值数组构造一个向量。

**参数**:
- `vec` (np.ndarray): 向量的数值表示（例如，`np.array([1, 2, 3])`）。
- `name` (str, 可选): 向量的名称，默认为空字符串。

**返回值**:
- `Vector`: 返回通过数值数组构造的向量对象。


## 4. 通过两点的数值表示构造向量

#### `VectorNPP(start: np.ndarray, end: np.ndarray, name: str = "")`
通过两点的数值表示来构造向量。

**参数**:
- `start` (np.ndarray): 向量的起点数值表示。
- `end` (np.ndarray): 向量的终点数值表示。
- `name` (str, 可选): 向量的名称，默认为空字符串。

**返回值**:
- `Vector`: 返回通过两点数值表示构造的向量对象。


## 5. 通过模长和方向构造向量

#### `VectorNNormDirection(norm: Number, direction: np.ndarray, name: str = "")`
通过给定的模长和方向构造向量。

**参数**:
- `norm` (Number): 向量的模长（大小）。
- `direction` (np.ndarray): 向量的方向，表示为数值数组。
- `name` (str, 可选): 向量的名称，默认为空字符串。

**返回值**:
- `Vector`: 返回通过模长和方向构造的向量对象。
