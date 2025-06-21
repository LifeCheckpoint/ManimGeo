# Circle


## 1. 中心与半径构造圆

#### `CirclePR(center: Point, radius: Number, name: str = "")`
通过指定圆心和半径构造圆。

**参数**:
- `center` (Point): 圆心点。
- `radius` (Number): 圆的半径，数值类型。
- `name` (str, 可选): 圆的名称，默认为空字符串。

**返回值**:
- `Circle`: 返回构造的圆对象。


## 2. 中心与圆上一点构造圆

#### `CirclePP(center: Point, point: Point, name: str = "")`
通过指定圆心和圆上一点构造圆。

**参数**:
- `center` (Point): 圆心点。
- `point` (Point): 圆上一点，用于确定圆的大小和位置。
- `name` (str, 可选): 圆的名称，默认为空字符串。

**返回值**:
- `Circle`: 返回构造的圆对象。


## 3. 半径线段构造圆

#### `CircleL(radius_segment: LineSegment, name: str = "")`
通过指定半径线段构造圆。

**参数**:
- `radius_segment` (LineSegment): 半径线段，表示圆的半径。
- `name` (str, 可选): 圆的名称，默认为空字符串。

**返回值**:
- `Circle`: 返回构造的圆对象。


## 4. 圆上三点构造圆

#### `CirclePPP(point1: Point, point2: Point, point3: Point, name: str = "")`
通过三点确定圆的构造。

**参数**:
- `point1` (Point): 圆上的第一点。
- `point2` (Point): 圆上的第二点。
- `point3` (Point): 圆上的第三点。
- `name` (str, 可选): 圆的名称，默认为空字符串。

**返回值**:
- `Circle`: 返回构造的圆对象。


## 5. 平移构造圆

#### `CircleTranslationCirV(circle: Circle, vec: Vector, name: str = "")`
通过平移操作构造新的圆。

**参数**:
- `circle` (Circle): 原始圆对象。
- `vec` (Vector): 平移向量。
- `name` (str, 可选): 新圆的名称，默认为空字符串。

**返回值**:
- `Circle`: 返回平移后的圆对象。
