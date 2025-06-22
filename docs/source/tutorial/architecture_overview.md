# ManimGeo 架构：Args、Base 与 Adapter

## 三位一体

`ManimGeo` 任何一个几何对象（如点、线、圆等）的生命周期和行为都围绕以下三个核心概念：

- **`Base` (基础几何对象)**：代表几何实体本身。它是所有具体几何对象（如 `Point`、`Line`、`Circle`）的基石，负责管理对象的属性、名称以及最重要的——它与其他几何对象之间的依赖关系。
- **`Args` (参数模型)**：定义了如何构造一个几何对象。每个几何对象都可以通过多种方式构造（例如，一个点可以是自由的，也可以是两条线的交点）。`Args` 模型封装了这些构造方法所需的输入参数，并能识别出这些参数中包含的其它几何对象依赖。
- **`Adapter` (适配器)**：是连接 `Args` 和 `Base` 的桥梁。它根据 `Args` 中定义的构造方式和参数，执行具体的几何计算，并将计算结果“适配”到 `Base` 几何对象的属性上。

## `BaseGeometry`：几何对象的抽象

`BaseGeometry` 是所有具体几何对象（如 `Point`、`Line`、`Circle`、`Angle`、`Vector`）的抽象基类。它定义了所有几何对象共有的核心行为和属性：

- **`name`**: 几何对象的唯一标识符。
- **`attrs`**: 一个列表，定义了该几何对象需要从其 `Adapter` 中获取并绑定的属性名称。例如，`Point` 的 `attrs` 可能包含 `['coord']`。
- **`adapter`**: 关联的 `GeometryAdapter` 实例，负责执行具体的几何计算。
- **`dependencies`**: 一个列表，存储了当前几何对象所依赖的上游几何对象。当上游对象发生变化时，当前对象需要重新计算。
- **`dependents`**: 一个列表，存储了依赖于当前几何对象的下游几何对象。当当前对象发生变化时，需要通知这些下游对象进行更新。
- **`update()`**: 这是 `BaseGeometry` 中最核心的方法。它负责触发 `adapter` 进行计算，将计算结果绑定到自身属性，并通知所有 `dependents` 进行更新。
- **`_extract_dependencies_from_args()`**: 从 `Args` 模型中提取出所依赖的 `BaseGeometry` 对象，并建立 `dependencies` 和 `dependents` 关系。

`BaseGeometry` 奠定了 ManimGeo 依赖管理和自动更新机制的基础，使得几何对象能够形成一个动态的、相互关联的网络。

## `Args`：构造蓝图与依赖源头

`Args` 概念主要由 `ArgsModelBase` 及其子类体现。`ArgsModelBase` 继承自 `BaseModelN`，它定义了所有几何对象构造参数模型共有的特性。

- **`construct_type`**: 一个字符串字段，用于明确指定当前 `Args` 模型所代表的几何对象构造类型。例如，一个点可以通过“自由点”、“两点中点”或“两线交点”等方式构造，每种方式对应一个特定的 `construct_type`。
- **`_get_deps()`**: 这个方法是 `Args` 模型的核心功能之一。它负责遍历 `Args` 模型中定义的参数，识别出其中包含的 `BaseGeometry` 实例，并返回这些实例的列表。这些实例就是当前几何对象所依赖的上游对象。

### 4.1. 为什么需要 `Args` 模型？

1. **清晰的构造定义**: 不同的几何对象有不同的构造方式，即使是同一种几何对象，也可能有多种构造方法。`Args` 模型为每种构造方法提供了清晰、结构化的参数定义。
2. **数据验证**: 借助 Pydantic，`Args` 模型能够自动验证传入的构造参数是否符合预期，例如类型是否正确，是否缺少必要参数等。
3. **依赖识别**: `_get_deps()` 方法使得 ManimGeo 能够自动从构造参数中识别出几何对象之间的依赖关系，这是构建依赖图的关键。

### 4.2. `Args` 模型的例子

以 `Point` 为例，它可能有以下 `Args` 模型：

- **`FreeArgs`**: 用于构造一个自由点，可能只包含一个 `coord` 参数。
- **`MidPPArgs`**: 用于构造两个点的中点，包含两个 `Point` 类型的参数 `p1` 和 `p2`。
- **`IntersectionLLArgs`**: 用于构造两条线的交点，包含两个 `Line` 类型的参数 `l1` 和 `l2`。

这些 `Args` 模型通过 `Union` 类型组合成一个大的 `PointConstructArgs`，使得 `Point` 对象可以接受多种构造参数。

## `Adapter`：几何计算的执行

`Adapter` 概念主要由 `GeometryAdapter` 及其子类体现。`GeometryAdapter` 是一个泛型类，它封装了根据 `Args` 模型执行具体几何计算的逻辑。

- **`args`**: `GeometryAdapter` 实例会持有一个具体的 `Args` 模型实例。
- **`__call__()`**: 这是 `Adapter` 中最重要的方法。当 `BaseGeometry` 的 `update()` 方法被调用时，它会调用其关联 `Adapter` 的 `__call__()` 方法。`__call__()` 方法会根据 `args` 中定义的 `construct_type` 和参数，执行相应的几何计算。这些计算通常会调用 `src/manimgeo/math` 模块中的数学函数。
- **`bind_attributes()`**: 这个方法负责将 `Adapter` 计算出的结果（例如点的坐标、线的起点/终点、圆的中心/半径等）绑定到其关联的 `BaseGeometry` 实例的相应属性上。

### 5.1. 为什么需要 `Adapter`？

1. **职责分离**: 将几何对象的属性管理（`BaseGeometry`）和具体的几何计算逻辑（`Adapter`）分离，使得代码结构更清晰，更易于维护。
2. **可扩展性**: 当需要添加新的几何对象构造方法时，只需创建新的 `Args` 模型和在 `Adapter` 中添加相应的计算逻辑，而无需修改 `BaseGeometry` 的核心代码。
3. **计算封装**: `Adapter` 封装了复杂的几何计算细节，使得 `BaseGeometry` 能够专注于依赖管理和更新传播。

### 5.2. `Adapter` 的例子

以 `PointAdapter` 为例，它的 `__call__()` 方法会根据 `self.args.construct_type` 的值，使用 `match` 语句来执行不同的计算：

- 如果 `construct_type` 是 `Free`，它可能直接使用 `self.args.coord` 作为点的坐标。
- 如果 `construct_type` 是 `MidPP`，它会获取 `self.args.p1` 和 `self.args.p2` 的坐标，然后计算中点坐标。
- 如果 `construct_type` 是 `IntersectionLL`，它会获取 `self.args.l1` 和 `self.args.l2` 的信息，然后调用 `src/manimgeo/math` 中的 `intersection_line_line` 函数来计算交点坐标。

## 6. 三者如何协同工作：一个点的生命周期

为了更好地理解 `Args`、`Base` 和 `Adapter` 如何协同工作，我们以创建一个“两点中点”为例：

1. **用户创建点**:

    ```python
    from manimgeo.components.point import Point
    from manimgeo.components.point.args import MidPPArgs

    # 假设 p1 和 p2 是已经存在的 Point 实例
    p1 = Point.Free(coord=[0, 0, 0])
    p2 = Point.Free(coord=[2, 0, 0])

    # 用户通过类方法创建中点
    mid_point = Point.MidPP(p1=p1, p2=p2)
    ```

2. **`Point.MidPP()` 内部**:
    - 这个类方法会创建一个 `MidPPArgs` 实例，并将 `p1` 和 `p2` 传入。
    - 它会调用 `Point` 的构造函数，将这个 `MidPPArgs` 实例作为 `args` 参数传入。

3. **`Point` 实例初始化 (`model_post_init`)**:
    - `Point` 继承自 `BaseGeometry`。在 `Point` 实例初始化后（Pydantic 的 `model_post_init` 钩子），会执行以下操作：
        - 实例化一个 `PointAdapter`，并将 `MidPPArgs` 实例传递给它。
        - 调用 `_extract_dependencies_from_args()` 方法。`MidPPArgs` 的 `_get_deps()` 方法会识别出 `p1` 和 `p2` 是依赖对象。
        - `mid_point` 的 `dependencies` 列表将包含 `p1` 和 `p2`。同时，`p1` 和 `p2` 的 `dependents` 列表将包含 `mid_point`。
        - 首次调用 `mid_point.update()` 方法。

4. **`mid_point.update()` 执行**:
    - `update()` 方法会调用 `mid_point.adapter.__call__()`。
    - `PointAdapter` 的 `__call__()` 方法会识别 `args` 的 `construct_type` 为 `MidPP`。
    - 它会获取 `p1.coord` 和 `p2.coord`，计算出中点坐标 `[1, 0, 0]`。
    - `PointAdapter` 调用 `bind_attributes()`，将计算出的中点坐标绑定到 `mid_point.coord` 属性上。

5. **依赖更新传播**:
    - 现在，如果 `p1.coord` 发生变化（例如，用户移动了 `p1`），`p1` 的 `update()` 方法会被调用。
    - `p1.update()` 完成后，它会遍历其 `dependents` 列表，找到 `mid_point`。
    - `p1` 会通知 `mid_point` 进行更新。
    - `mid_point` 接收到更新通知后，会再次调用自身的 `update()` 方法，重新计算中点坐标，从而实现自动联动。

## 7. 依赖管理和更新机制

ManimGeo 的核心优势在于其强大的依赖管理和自动更新机制。这得益于 `BaseGeometry` 中维护的 `dependencies` 和 `dependents` 列表，以及 `update()` 方法的设计。

- **依赖图**: 几何对象之间通过 `dependencies` 和 `dependents` 形成一个有向无环图（DAG）。
- **事件驱动**: 当一个几何对象的属性发生变化时，它会触发自身的 `update()` 方法。
- **递归更新**: `update()` 方法不仅更新自身，还会通知所有直接依赖于它的下游对象进行更新。这个过程会递归地进行，确保整个依赖链上的所有相关几何对象都得到正确更新。
- **错误处理**: 如果在更新过程中发生错误，`BaseGeometry` 会设置 `on_error` 标志，并将错误信息向下游传播，以便进行调试和处理。

这种机制使得 ManimGeo 能够轻松处理复杂的几何关系，并确保在任何一个基础对象发生变化时，整个系统都能保持一致性。
