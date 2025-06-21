# Angle

**`Angle` 类支持加法、减法与数乘**


## 1. 通过三点构造角

#### `AnglePPP(start: Point, center: Point, end: Point, name: str = "")`
通过三个点构造一个角，指定起始点、中心点和终止点。

**参数**:
- `start` (Point): 角的起始点。
- `center` (Point): 角的中心点，通常是角的顶点。
- `end` (Point): 角的终止点。
- `name` (str, 可选): 角的名称，默认为空字符串。

**返回值**:
- `Angle`: 返回通过三点构造的角对象。


## 2. 通过两线构造角

#### `AngleLL(line1: Line, line2: Line, name: str = "")`
通过两条直线构造一个角，角的两边分别为指定的两条直线。

**参数**:
- `line1` (Line): 角的第一边。
- `line2` (Line): 角的第二边。
- `name` (str, 可选): 角的名称，默认为空字符串。

**返回值**:
- `Angle`: 返回通过两条线构造的角对象。


## 3. 通过一线和一点构造角

#### `AngleLP(line: Line, point: Point, name: str = "")`
通过一条直线和一个点来构造一个角，点位于角的另一端。

**参数**:
- `line` (Line): 角的起始边。
- `point` (Point): 角的终止点。
- `name` (str, 可选): 角的名称，默认为空字符串。

**返回值**:
- `Angle`: 返回通过一线和一点构造的角对象。


## 4. 通过角度构造角

#### `AngleN(angle: Number, turn: Literal["Clockwise", "Counterclockwise"] = "Counterclockwise", name: str = "")`
通过给定的角度和旋转方向构造一个角。

**参数**:
- `angle` (Number): 角度，数值类型。
- `turn` (Literal["Clockwise", "Counterclockwise"], 可选): 旋转方向，默认为“Counterclockwise”（逆时针）。
- `name` (str, 可选): 角的名称，默认为空字符串。

**返回值**:
- `Angle`: 返回通过角度构造的角对象。


## 5. 反转角旋转方向构造角

#### `AngleTurnA(angle: Angle, name: str = "")`
通过反转给定角的旋转方向来构造一个新角。

**参数**:
- `angle` (Angle): 已存在的角对象。
- `name` (str, 可选): 新角的名称，默认为空字符串。

**返回值**:
- `Angle`: 返回通过反转旋转方向得到的新角对象。
