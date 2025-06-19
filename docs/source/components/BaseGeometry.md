# BaseGeometry 基础几何类

几何基类，负责依赖传递等


## 初始化

#### `__init__(self, name: str = "")`

初始化几何对象

**参数**:
 - `name` (str, 可选): 几何对象的名称


## 添加 / 删除依赖对象

#### (添加依赖对象) `add_dependent(self, obj: BaseGeometry)`

#### (删除依赖对象) `remove_dependent(self, obj: BaseGeometry)`

添加和删除当前几何对象的依赖

**参数**:
 - `obj` (BaseGeometry): 下游依赖


## 向所有依赖项发出更新信号

#### `board_update_msg(self, on_error: bool = False)`

向所有依赖项发出更新信号，以指示下游依赖重新计算参数

**参数**:
 - `on_error` (bool): 当前几何对象是否出现计算错误，该标志将会向下游传播


## 执行当前对象更新

#### `update(self, *new_objs: Optional[Union[BaseGeometry, any]])`

执行当前对象的更新，包括 `Adapter` 的重新计算，然后通过 `board_update_msg` 向下游广播更新通知

如果在参数计算过程中发生了错误，则错误会被捕获，当前几何对象错误标志位变化为 `True`

**参数**:
 - `new_objs` (BaseGeometry 或任意类型, 可选): 如果更新时发生了上游对象的替换而非单纯参数更新，则需要提供该参数指示使用新对象进行参数计算
