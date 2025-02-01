from manimgeo.components import *

from manimlib import Mobject
from typing import Sequence

def dim_23(x: np.ndarray) -> np.ndarray:
    return np.append(x, 0)

class GeoManimGLManager:
    """管理 ManimGL Mobject 和几何对象之间的自动映射"""
    start_update: bool

    def __init__(self):
        self.start_update = False

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
        if isinstance(obj, Point) and obj.adapter.construct_type is "Free":
            # 自由点，叶子节点
            mobj.add_updater(lambda mobj: self.update_leaf(mobj, obj))
        else:
            # 非自由对象
            mobj.add_updater(lambda mobj: self.update_node(mobj, obj))


    def update_leaf(self, mobj: Mobject, obj: BaseGeometry):
        """叶子 Updater，读取部件信息并应用至 FreePoint 坐标"""
        
        if not self.start_update:
            return
        
        if isinstance(obj, Point):
            obj.set_coord(mobj.get_center()[:2])

    def _adapt_mobjects(self, obj: BaseGeometry, mobj: Mobject):
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
        
        # 处理错误对象

        # 更新对象位置
        self._adapt_mobjects(obj, mobj)
    
    def start_trace(self):
        """
        追踪所有部件几何运动

        等同于 __enter__()
        """
        self.__enter__()

    def stop_trace(self):
        """
        结束 Trace

        等同于 __exit__()
        """
        self.__exit__()

    def __enter__(self):
        """
        追踪所有部件几何运动
        """
        self.start_update = True

    def __exit__(self, exc_type, exc_value, traceback):
        """
        结束 Trace
        """
        self.start_update = False