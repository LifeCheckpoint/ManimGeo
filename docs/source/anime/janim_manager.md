# GeoJAnimManager

⚠ **文档已过时**

`GeoJAnimManager` 负责管理 JAnim VItem 和几何对象之间的自动映射


**由于 JAnim 不同版本在 `DataUpdater` 上的行为不同，使用方式也会有所区别**

## 旧版本 `janim <= 2.3.0` 创建机制

物件创建时，为 `VItem` 动画物件创建 `DataUpdater`。由于框架限制，`DataUpdater` 将被挂载在一个空对象而非动画对象本体上

 - 对于**叶子节点**，`DataUpdater` 将读取叶子节点的组件信息，应用到几何对象，几何对象自行逐层更新
 - 对于**非叶子节点**，`DataUpdater` 将读取几何对象的参数计算结果，将其应用至动画对象。

## 新版本 `janim > 2.3.0` 创建机制

等 jk 大佬重构


## 初始化

#### `__init__(self, timeline: Optional[Timeline] = None)`

初始化动画管理器，可以提供当前场景的时间轴以便于添加 `DataUpdater`


## 创建 `VItems` 并自动注册 `DataUpdater`

#### `create_vitems_with_add_updater(self, objs: Sequence[Union[Point, Line, Circle]], duration: Number, timeline: Optional[Timeline] = None, **kwargs)`

创建 `VItems` ，并为每个创建好的 `VItem` 以指定时长注册 `DataUpdater` 到动画中

**参数**:
 - `objs` (Union[Point, Line, Circle]): 将要创建动画物件的几何对象
 - `duration` (Number): `DataUpdater` 持续时间，建议与动画时长相等
 - `timeline` (Timeline): 动画时间轴，如果初始化时未传入则需在此传入
 - `kwargs`: 将要传递给 `timeline.play()` 的其它字典参数


## 从几何对象创建 `Vitems`

#### `create_vitem_from_geometry(self, obj: Union[Point, Line, Circle])`

通过几何对象创建动画图形对象，并自动为该对象增加 `DataUpdater`


## 从几何对象列表创建 `Vitems`

#### `create_vitems_from_geometry(self, objs: Sequence[Union[Point, Line, Circle]])`

传入几何对象列表，该函数将调用 `create_vitem_from_geometry` 创建动画图形对象


## 注册更新器

#### `register_updater(self, obj: BaseGeometry, vitem: VItem)`

关联几何对象与动画物件，并注册 `DataUpdater` 以进行更新



## 设置几何对象更新错误行为

#### `set_on_error_exec(self, exec: Union[None, Literal["vis", "stay"], Callable[[bool, BaseGeometry, VItem], None]] = "vis")`

设置几何对象计算错误时的行为

几何对象通常会因为**解不存在**，或者偶发的**精度问题**等出现错误，并且错误会随依赖链条向下传播，通过该函数设置发生错误时的行为

`exec`: 
 - `"vis"`: 几何对象将**隐藏可见**，直到错误消失
 - `"stay"`: 几何对象将**保持静止**，直到错误消失
 - `(on_error: bool, obj: BaseGeometry, vitem: VItem) -> None`: 自定义回调函数
