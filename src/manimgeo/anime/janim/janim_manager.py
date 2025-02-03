from manimgeo.components import *
from manimgeo.anime.manager import GeoManager
from manimgeo.anime.state import StateManager
from manimgeo.anime.janim.error_func import ErrorFunctionJAnim as JAnimError
from janim.logger import log

from janim.imports import Timeline, VItem, DataUpdater
from typing import Sequence, Callable

def dim_23(x: np.ndarray) -> np.ndarray:
    return np.append(x, 0)

class GeoJAnimManager(GeoManager):
    """管理 JAnim Component 和几何对象之间的自动映射"""
    on_error_exec: Union[None, Literal["vis", "stay"], Callable[[bool, BaseGeometry, VItem], None]]
    state_manager = StateManager("janim", JAnimError.set_visible_by_state)
    current_helper_vitem: List[VItem] =  []

    def __init__(self):
        super().__init__()
        self.start_trace()
        self.on_error_exec = "vis"

    def create_vitems_with_add_updater(
            self,
            objs: Sequence[Union[Point, Line, Circle]],
            timeline: Timeline,
            duration: Number,
            **kwargs
        ) -> List[VItem]:
        """
        通过几何对象创建 VItem，创建对应 Updater 后立刻添加到时间轴
        """
        vitems, updaters = [], []
        for obj in objs:
            vitem, updater = self.create_vitem_from_geometry(obj)
            vitems.append(vitem)
            updaters.append(updater)

        timeline.prepare(*updaters, duration=duration, **kwargs)
        return vitems

    def create_vitems_from_geometry(
            self,
            objs: Sequence[Union[Point, Line, Circle]]
        ):
        """
        通过几何对象创建 VItem，并创建对应 Updater
        """
        return [self.create_vitem_from_geometry(geo) for geo in objs]

    def create_vitem_from_geometry(
            self,
            obj: Union[Point, Line, Circle]
        ):
        """
        通过几何对象创建 VItem，并创建对应 DataUpdater
        """
        vitem: VItem

        match obj:
            case Point():
                from janim.imports import Dot as VDot
                vitem = VDot()

            case Line():
                from janim.imports import Line as VLine
                vitem = VLine()

            case Circle():
                from janim.imports import Circle as VCircle
                vitem = VCircle()

            case _:
                raise NotImplementedError(f"Cannot create vitem from object of type: {type(obj)}")
            
        # log.debug(f"init: {obj.name} -> {id(vitem)}")
        self._adapt_vitems(obj, vitem)
        updater = self.register_updater(obj, vitem)
        return vitem, updater
    
    def _adapt_vitems(self, obj: BaseGeometry, vitem: VItem):
        """控制物件具体位置等更新"""
        INFINITY_LINE_SCALE = 20
    
        match obj:
            case Point():
                from janim.imports import Dot as VDot
                vitem: VDot
                vitem.points.move_to(dim_23(obj.coord))

            case Line():
                from janim.imports import Line as VLine
                vitem: VLine

                if not np.allclose(obj.start, obj.end):
                    if isinstance(obj, LineSegment):
                        vitem.points.put_start_and_end_on(dim_23(obj.start), dim_23(obj.end))

                    elif isinstance(obj, Ray):
                        vitem.points.put_start_and_end_on(
                            dim_23(obj.start), 
                            dim_23(obj.start + INFINITY_LINE_SCALE * obj.unit_direction)
                        )

                    elif isinstance(obj, InfinityLine):
                        vitem.points.put_start_and_end_on(
                            dim_23(obj.end - INFINITY_LINE_SCALE * obj.unit_direction),
                            dim_23(obj.start + INFINITY_LINE_SCALE * obj.unit_direction)
                        )

            case Circle():
                from janim.imports import Circle as VCircle
                vitem: VCircle

                # 需要通过半径计算实际相对缩放
                r = vitem.points.radius
                vitem.points.scale(obj.radius / r)
                vitem.points.move_to(dim_23(obj.center))

            case _:
                raise NotImplementedError(f"Cannot create vitem from object of type: {type(obj)}")
            
    def register_updater(self, obj: BaseGeometry, vitem: VItem):
        """为 VItem 物件注册更新器"""
        helper_vitem = VItem()
        self.current_helper_vitem.append(helper_vitem)

        if isinstance(obj, Point) and obj.adapter.construct_type == "Free":
            # 自由点，叶子节点
            return DataUpdater(helper_vitem, lambda data, p: self.update_leaf(vitem.current(), obj), skip_null_items=False)
        else:
            # 非自由对象
            return DataUpdater(helper_vitem, lambda data, p: self.update_node(vitem.current(), obj), skip_null_items=False)

    def update_leaf(self, vitem: VItem, obj: BaseGeometry):
        """叶子 Updater，读取部件信息并应用至 FreePoint 坐标"""


        if not self.start_update:
            return

        if isinstance(obj, Point):
            from janim.imports import Dot
            vitem: Dot
            obj.set_coord(vitem.points.box.center[:2])
        else:
            log.warning(f"Object {obj.name} has been register for updater. But {type(obj).__name__} is not a support update type")

    def update_node(self, vitem: VItem, obj: BaseGeometry):
        """被约束对象 Updater，读取约束更改后信息应用到 Mobject"""

        if not self.start_update:
            return
        
        # 更新状态自动机并自动处理错误对象
        self.state_manager.update(obj, vitem)

        # 更新对象位置
        # log.debug(f"adapt: {obj.name} -> {obj.coord if isinstance(obj, Point) else ""}")
        self._adapt_vitems(obj, vitem)