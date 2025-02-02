from manimgeo.components import *
from manimgeo.anime.manager import GeoManager
from manimgeo.anime.manimgl.state import StateManager
from manimgeo.anime.manimgl.error_func import ErrorFunctionManimGL as GLError

from manimlib import Mobject
from typing import Sequence, Callable, Dict

def dim_23(x: np.ndarray) -> np.ndarray:
    return np.append(x, 0)

class GeoManimGLManager(GeoManager):
    """管理 ManimGL Mobject 和几何对象之间的自动映射"""
    on_error_exec: Union[None, Literal["vis", "stay"], Callable[[bool, BaseGeometry, Mobject], None]]
    state_manager = StateManager("manimgl", GLError.set_visible_by_state)
    ids: List[int]

    def __init__(self):
        super().__init__()
        self.on_error_exec = "vis"
        self.ids = []

    def create_mobjects_from_geometry(
            self,
            objs: Sequence[Union[Point, Line, Circle]],
        ):
        """
        通过几何对象创建 Mobject，并自动关联
        """
        return [self.create_mobject_from_geometry(geo) for geo in objs]

    def create_mobject_from_geometry(
            self,
            obj: Union[Point, Line, Circle]
        ):
        """
        通过几何对象创建 Mobject，并自动关联
        """
        mobject: Mobject

        match obj:
            case Point():
                from manimlib import Dot as MDot
                mobject = MDot()

            case Line():
                from manimlib import Line as MLine
                if isinstance(obj, LineSegment):
                    mobject = MLine()
                elif isinstance(obj, Ray):
                    mobject = MLine()
                elif isinstance(obj, InfinityLine):
                    mobject = MLine()
                else:
                    raise ValueError(f"Type {type(obj).__name__} is not a Line")

            case Circle():
                from manimlib import Circle as MCircle
                mobject = MCircle()

            case _:
                raise NotImplementedError(f"Cannot create mobject from object of type: {type(obj)}")
            
        self._adapt_mobjects(obj, mobject)
        self.register_updater(obj, mobject)
        return mobject
    
    def register_updater(self, obj: BaseGeometry, mobj: Mobject):
        """
        注册更新器
        """
        if isinstance(obj, Point) and obj.adapter.construct_type == "Free":
            # 自由点，叶子节点
            print(f"Register leaf object: {obj.name}")
            self.ids.append(id(mobj))
            mobj.add_updater(lambda mobj: self.update_leaf(mobj, obj))
        else:
            # 非自由对象
            mobj.add_updater(lambda mobj: self.update_node(mobj, obj))

    def update_leaf(self, mobj: Mobject, obj: BaseGeometry):
        """叶子 Updater，读取部件信息并应用至 FreePoint 坐标"""
        
        if not self.start_update:
            return
        
        if isinstance(obj, Point) and id(mobj) in self.ids:
            obj.set_coord(mobj.get_center()[:2])

    def _adapt_mobjects(self, obj: BaseGeometry, mobj: Mobject):
        """控制物件具体位置等更新"""
        INFINITY_LINE_SCALE = 20

        match obj:
            case Point():
                mobj.move_to(dim_23(obj.coord))

            case Line():
                from manimlib import Line as MLine
                mobj: MLine

                if not np.allclose(obj.start, obj.end):
                    if isinstance(obj, LineSegment):
                        mobj.set_points_by_ends(dim_23(obj.start), dim_23(obj.end))

                    elif isinstance(obj, Ray):
                        mobj.set_points_by_ends(
                            dim_23(obj.start), 
                            dim_23(obj.start + INFINITY_LINE_SCALE * obj.unit_direction)
                        )

                    elif isinstance(obj, InfinityLine):
                        mobj.set_points_by_ends(
                            dim_23(obj.end - INFINITY_LINE_SCALE * obj.unit_direction),
                            dim_23(obj.start + INFINITY_LINE_SCALE * obj.unit_direction)
                        )

            case Circle():
                from manimlib import Circle as MCircle
                mobj: MCircle

                # 需要通过半径计算实际相对缩放
                r = mobj.get_radius()
                mobj.scale(obj.radius / r).move_to(dim_23(obj.center))

            case _:
                raise NotImplementedError(f"Cannot create mobject from object of type: {type(obj)}")

    def update_node(self, mobj: Mobject, obj: BaseGeometry):
        """被约束对象 Updater，读取约束更改后信息应用到 Mobject"""

        if not self.start_update:
            return
        
        # 更新状态自动机并自动处理错误对象
        self.state_manager.update(obj, mobj)

        # 更新对象位置
        self._adapt_mobjects(obj, mobj)

    def set_on_error_exec(self, exec: Union[None, Literal["vis", "stay"], Callable[[bool, BaseGeometry, Mobject], None]] = "vis"):
        """
        设置几何对象计算错误时的行为

        几何对象通常会因为解不存在等问题出现错误，并且错误会随依赖链条向下传播，通过该函数设置发生错误时的行为

        `exec`: 
         - `None`: 不执行任何操作，异常将抛出 (develop)
         - `"vis"`: 几何对象将隐藏可见，直到错误消失
         - `"stay"`: 几何对象将保持静止，直到错误消失
         - `(on_error: bool, obj: BaseGeometry, mobj: Mobject) -> None`: 自定义回调函数
        """
        if exec == None:
            # TODO
            pass
        elif exec == "vis":
            self.state_manager.set_strategy_func(GLError.set_visible_by_state)
        elif exec == "stay":
            self.state_manager.set_strategy_func(lambda s, o, mo: ...)
        elif callable(exec):
            self.state_manager.set_strategy_func(lambda s, o, mo: GLError.func_by_state(s, o, mo, exec))
        else:
            raise ValueError(f"Cannot set error handler as {exec}")
