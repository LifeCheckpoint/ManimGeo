# GeometryAdapter 几何参数适配器

几何参数适配器，负责几何参数计算，解耦参数与几何对象之间的耦合


单个几何对象有多种构造方式，例如 `Circle` 对象可能有如下构造方式：

1. `PR`: 中心与半径构造圆
2. `PP`: 中心与圆上一点构造圆
3. `L`: 半径线段构造圆
4. `PPP`: 圆上三点构造圆
5. `TranslationCirV`: 构造平移圆
6. `InverseCirCir`: 构造反演圆
7. `InscribePPP`: 构造三点内切圆

为每一种构造建立一个类，代码复用低且组合爆炸，因此将参数的计算责任交予 `Adapter`。具体来说：

 - **`BaseGeometry` 及其子类**: 几何对象本体，负责传递依赖更新信息，并从 `Adapter` 中得到其统一属性
 - **`GeometryAdapter` 及其子类**: 负责几何参数的计算，几何对象通知适配器进行计算时，适配器根据构造方法将多种构造参数转换为统一参数属性，从而可被几何对象读取

---

## 初始化

#### (GeometryAdapter) `__init__(self, construct_type: str)`

#### (子类) `__init__(self, construct_type: str, current_geo_obj, *objs: Union[BaseGeometry, any])`

**参数**:
 - `construct_type` (str): 传入构造类型声明，例如 `"PP"`
 - `current_geo_obj` (BaseGeometry): 当前 `Adapter` 率属的几何对象
 - `objs` (BaseGeometry): 该对象依赖的上游对象，`Adapter` 将为当前对象添加父依赖


## 执行计算

#### `__call__(self, *objs)`

通过读入上游对象的几何信息，计算当前对象的信息。根据预先指定的构造方法进行参数的类型检查与参数的具体计算

**参数**:
 - `objs` (BaseGeometry): 计算依赖的上游对象


## 结果传递

#### `bind_attributes(self, target: BaseGeometry, attrs: List[str])`

批量复制属性（计算结果）到对象中

**参数**:
 - `target` (BaseGeometry): 目标几何对象
 - `attrs` (List[str]): 将要从 `Adapter` 复制到目标几何对象的属性列表
