# Point

## 1. 构造自由点（叶子节点）

#### `PointFree(coord: np.ndarray, name: str = "")`
构造一个自由点。自由点即不受约束的点。

**参数**:
- `coord` (np.ndarray): 点的坐标。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回一个自由点对象。


## 2. 构造约束点（非叶子节点）

#### `PointConstraint(coord: np.ndarray, name: str = "")`
构造一个约束点。约束点的坐标会被后续依赖更新覆盖。

**参数**:
- `coord` (np.ndarray): 初始坐标（会被后续更新）。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回一个约束点对象。


## 3. 构造两点中点

#### `PointMidPP(point1: Point, point2: Point, name: str = "")`
构造两个点的中点。

**参数**:
- `point1` (Point): 第一个点。
- `point2` (Point): 第二个点。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回中点对象。


## 4. 构造线段中点

#### `PointMidL(line: LineSegment, name: str = "")`
构造线段的中点。

**参数**:
- `line` (LineSegment): 线段对象。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回线段中点对象。


## 5. 构造比例延长（位似）点

#### `PointExtensionPP(start: Point, through: Point, factor: Number, name: str = "")`
构造一个基于比例延长的点。

**参数**:
- `start` (Point): 起始点。
- `through` (Point): 经过点。
- `factor` (Number): 延长比例，1 表示恒等延长。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回延长点对象。


## 6. 构造轴对称点

#### `PointAxisymmetricPL(point: Point, line: Line, name: str = "")`
构造一个关于直线的轴对称点。

**参数**:
- `point` (Point): 原始点。
- `line` (Line): 对称轴线。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回轴对称点对象。


## 7. 构造垂足点

#### `PointVerticalPL(point: Point, line: Line, name: str = "")`
构造一个点到直线的垂足点。

**参数**:
- `point` (Point): 原始基准点。
- `line` (Line): 目标直线。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回垂足点对象。


## 8. 构造平行线上一点

#### `PointParallelPL(point: Point, line: Line, distance: Number, name: str = "")`
构造一个平行于某条直线的点。

**参数**:
- `point` (Point): 基准点。
- `line` (Line): 平行基准线。
- `distance` (Number): 沿平行方向的绝对距离。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回平行点对象。


## 9. 构造反演点

#### `PointInversionPCir(point: Point, circle: Circle, name: str = "")`
构造一个反演点，相对于某个圆。

**参数**:
- `point` (Point): 原始点。
- `circle` (Circle): 反演基准圆。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回反演点对象。


## 10. 构造两线交点

#### `PointIntersectionLL(line1: Line, line2: Line, regard_infinite: bool = False, name: str = "")`
构造两条线的交点。

**参数**:
- `line1` (Line): 第一条线。
- `line2` (Line): 第二条线。
- `regard_infinite` (bool, 可选): 是否视为无限长直线，默认为 `False`。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回交点对象。


## 11. 构造线与圆的交点对

#### `Points2IntersectionLCir(line: Line, circle: Circle, filter: Optional[Callable[[np.ndarray], bool]] = None, regard_infinite: bool = False, name: str = "")`
构造线与圆的交点对。

**参数**:
- `line` (Line): 直线/线段。
- `circle` (Circle): 圆。
- `filter` (Callable[[np.ndarray], bool], 可选): 给定条件，筛选返回符合条件的点
- `regard_infinite` (bool, 可选): 是否视为无限长直线，默认为 `False`。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Union[List[Point], Point]`: 返回交点对列表，或单个符合条件的交点。


## 12. 构造两圆交点对

#### `Points2IntersectionCirCir(circle1: Circle, circle2: Circle, filter: Optional[Callable[[np.ndarray], bool]] = None, name: str = "")`
构造两圆的交点对。

**参数**:
- `circle1` (Circle): 第一个圆。
- `circle2` (Circle): 第二个圆。
- `filter` (Callable[[np.ndarray], bool], 可选): 给定条件，筛选返回符合条件的点
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Union[List[Point], Point]`: 返回交点对列表，或单个符合条件的交点。


## 13. 构造平移点

#### `PointTranslationPV(point: Point, vector: Vector, name: str = "")`
构造平移后的点。

**参数**:
- `point` (Point): 原始点。
- `vector` (Vector): 平移向量。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回平移点对象。


## 14. 构造三角形重心

#### `PointCentroidPPP(point1: Point, point2: Point, point3: Point, name: str = "")`
构造三角形的重心。

**参数**:
- `point1` (Point): 第一个顶点。
- `point2` (Point): 第二个顶点。
- `point3` (Point): 第三个顶点。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回三角形重心对象。


## 15. 构造三角形外心

#### `PointCircumcenterPPP(point1: Point, point2: Point, point3: Point, name: str = "")`
构造三角形的外心。

**参数**:
- `point1` (Point): 第一个顶点。
- `point2` (Point): 第二个顶点。
- `point3` (Point): 第三个顶点。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回三角形外心对象。


## 16. 构造三角形内心

#### `PointIncenterPPP(point1: Point, point2: Point, point3: Point, name: str = "")`
构造三角形的内心。

**参数**:
- `point1` (Point): 第一个顶点。
- `point2` (Point): 第二个顶点。
- `point3` (Point): 第三个顶点。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回三角形内心对象。


## 17. 构造三角形垂心

#### `PointOrthocenterPPP(point1: Point, point2: Point, point3: Point, name: str = "")`
构造三角形的垂心。

**参数**:
- `point1` (Point): 第一个顶点。
- `point2` (Point): 第二个顶点。
- `point3` (Point): 第三个顶点。
- `name`

 (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回三角形垂心对象。


## 18. 构造圆心

#### `PointCircleCenter(circle: Circle, name: str = "")`
构造圆的圆心。

**参数**:
- `circle` (Circle): 圆。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回圆心对象。


## 19. 获取两点中的单点对象

#### `PointOfPoints2(points2: Points2, index: Literal[0, 1], name: str = "")`
从一个点对对象中获取单独的点。

**参数**:
- `points2` (Points2): 两点组合对象。
- `index` (Literal[0, 1]): 两点中的其中一点索引。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回指定点的对象。


## 20. 获取两点中的单点对象列表

#### `PointOfPoints2List(points2: Points2, name: str = "")`
获取两点对象的所有点。

**参数**:
- `points2` (Points2): 两点组合对象。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `List[Point]`: 返回包含两个点的列表。


## 21. 获取符合条件的单点对象

#### `PointOfPoints2Fit(points2: Points2, filter: Callable[[np.ndarray], bool], name: str = "")`
获取符合条件的第一个单点对象

**参数**:
- `points2` (Points2): 两点组合对象。
- `filter` (Callable[[np.ndarray], bool]): 给定点坐标，判定坐标是否满足条件。

**返回值**:
- `Point`: 返回符合条件的第一个点


## 22. 旋转构造点

#### `PointRotatePPA(point: Point, center: Point, angle: Angle, name: str = "")`
通过旋转构造一个点

**参数**:
- `point` (Point): 将要旋转的点对象。
- `center` (Point): 旋转中心点对象。
- `angle` (Angle): 将要旋转的角度对象。
- `name` (str, 可选): 点的名称，默认为空字符串。

**返回值**:
- `Point`: 返回旋转点对象
