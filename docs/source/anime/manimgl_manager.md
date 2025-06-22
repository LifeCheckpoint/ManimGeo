# GeoManimGLManager

⚠ **文档已过时**

`GeoManimGLManager` 负责管理 ManimGL Mobject 和几何对象之间的自动映射

物件创建时，为 `Mobject` 动画物件创建 `Updater`。

 - 对于**叶子节点**，`Updater` 将读取叶子节点的组件信息，应用到几何对象，几何对象自行逐层更新
 - 对于**非叶子节点**，`Updater` 将读取几何对象的参数计算结果，将其应用至动画对象。


## 从几何对象创建 `Mobject`

#### `create_mobject_from_geometry(self, obj: Union[Point, Line, Circle])`

通过几何对象创建动画图形对象，并自动为该对象增加 `Updater`


## 从几何对象列表创建 `Mobject`

#### `create_mobjects_from_geometry(self, objs: Sequence[Union[Point, Line, Circle]])`

传入几何对象列表，该函数将调用 `create_mobject_from_geometry` 创建动画图形对象


## 注册更新器

#### `register_updater(self, obj: BaseGeometry, mobj: Mobject)`

关联几何对象与动画物件，并注册 `Updater` 以进行更新


## 设置几何对象更新错误行为

#### `set_on_error_exec(self, exec: Union[None, Literal["vis", "stay"], Callable[[bool, BaseGeometry, Mobject], None]] = "vis")`

设置几何对象计算错误时的行为

几何对象通常会因为**解不存在**，或者偶发的**精度问题**等出现错误，并且错误会随依赖链条向下传播，通过该函数设置发生错误时的行为

`exec`: 
 - `"vis"`: 几何对象将**隐藏可见**，直到错误消失
 - `"stay"`: 几何对象将**保持静止**，直到错误消失
 - `(on_error: bool, obj: BaseGeometry, mobj: Mobject) -> None`: 自定义回调函数