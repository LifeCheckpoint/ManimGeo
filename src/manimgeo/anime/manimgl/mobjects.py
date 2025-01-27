from manimgeo.components import *

from manimlib import Mobject
from typing import Sequence

dim_23 = lambda x: np.append(x, 0)

class GeoManimGLMap:
    """管理 ManimGL Mobject 和几何对象之间的自动映射"""
    start_update: bool

    def __init__(self):
        self.start_update = False

    def create_mobjects_from_geometry(
            self,
            objs: Sequence[Union[
                    PointLike, LineLike, CirclePPP, CirclePP, CircleP,
                    EllipseAB, EllipseCE, HyperbolaAB, HyperbolaCE, ParabolaPP
                ]],
        ):
        """
        通过几何对象创建 Mobject，并自动关联
        """
        return [self.create_mobject_from_geometry(geo) for geo in objs]

    def create_mobject_from_geometry(
            self,
            obj: Union[
                    PointLike, LineLike, CirclePPP, CirclePP, CircleP,
                    EllipseAB, EllipseCE, HyperbolaAB, HyperbolaCE, ParabolaPP
                ]
        ):
        """
        通过几何对象创建 Mobject，并自动关联
        """
        INFINITY_LINE_SCALE: float = 20

        mobject: Mobject

        # 注意匹配父子顺序
        match obj:
            case PointLike():
                from manimlib import Dot as MDot
                mobject = MDot(dim_23(obj.coord))

            case LineLike():
                from manimlib import Line as MLine
                if isinstance(obj, LineSegmentPP):
                    mobject = MLine(dim_23(obj.start.coord), dim_23(obj.end.coord))
                elif isinstance(obj, RayPP):
                    mobject = MLine(
                        dim_23(obj.start.coord), 
                        dim_23(obj.start.coord + INFINITY_LINE_SCALE*(obj.end.coord - obj.start.coord))
                    )
                elif isinstance(obj, InfinityLinePP):
                    mobject = MLine(
                        dim_23(obj.end.coord + INFINITY_LINE_SCALE*(obj.start.coord - obj.end.coord)),
                        dim_23(obj.start.coord + INFINITY_LINE_SCALE*(obj.end.coord - obj.start.coord))
                    )

            case CircleP() | CirclePP():
                from manimlib import Circle as MCircle
                mobject = MCircle().scale(obj.radius).move_to(dim_23(obj.center_point.coord))

            case CirclePPP():
                from manimlib import Circle as MCircle
                mobject = MCircle().scale(obj.radius).move_to(dim_23(obj.center))

            case EllipseAB() | EllipseCE():
                print("developing")
                pass

            case HyperbolaAB() | HyperbolaCE():
                print("developing")
                pass

            case ParabolaPP():
                print("developing")
                pass

            case _:
                raise NotImplementedError(f"Cannot create mobject from object of type: {type(obj)}")
            
        self.register_updater(obj, mobject)
        return mobject
    
    def bond(self, obj: BaseGeometry, mobj: Mobject):
        """
        关联
        """
        self.register_updater(obj, mobj)

    def register_updater(self, obj: BaseGeometry, mobj: Mobject):
        """
        注册更新器
        """
        if isinstance(obj, (FreePoint, )):
            # 自由点，叶子节点
            mobj.add_updater(lambda mobj: self.update_leaf(mobj, obj))
        else:
            # 非自由对象
            mobj.add_updater(lambda mobj: self.update_node(mobj, obj))


    def update_leaf(self, mobj: Mobject, obj: BaseGeometry):
        """叶子 Updater，读取部件信息并应用至 FreePoint 坐标"""
        
        if not self.start_update:
            return
        
        if isinstance(obj, FreePoint):
            obj.coord = mobj.get_center()[:2]
        else:
            raise NotImplementedError(f"Cannot update object of type: {type(obj)}")

    def update_node(self, mobj: Mobject, obj: BaseGeometry):
        """被约束对象 Updater，读取约束更改后信息应用到 Mobject"""
        INFINITY_LINE_SCALE = 20

        if not self.start_update:
            return

        # 注意匹配父子顺序
        match obj:
            case PointLike():
                mobj.move_to(dim_23(obj.coord))

            case LineLike():
                from manimlib import Line as MLine
                mobj: MLine

                if not np.allclose(obj.start.coord, obj.end.coord, atol=1e-3):
                    if isinstance(obj, LineSegmentPP):
                        mobj.set_points_by_ends(dim_23(obj.start.coord), dim_23(obj.end.coord))

                    elif isinstance(obj, RayPP):
                        mobj.set_points_by_ends(
                            dim_23(obj.start.coord), 
                            dim_23(obj.start.coord + INFINITY_LINE_SCALE*(obj.end.coord - obj.start.coord))
                        )

                    elif isinstance(obj, InfinityLinePP):
                        mobj.set_points_by_ends(
                            dim_23(obj.end.coord + obj*(obj.start.coord - obj.end.coord)),
                            dim_23(obj.start.coord + obj*(obj.end.coord - obj.start.coord))
                        )

            case CircleP() | CirclePP():
                from manimlib import Circle as MCircle
                mobj: MCircle

                # 需要通过半径计算实际相对缩放
                r = mobj.get_radius()
                mobj.scale(obj.radius/r).move_to(dim_23(obj.center_point.coord))

            case CirclePPP():
                from manimlib import Circle as MCircle
                mobj: MCircle

                # 需要通过半径计算实际相对缩放
                r = mobj.get_radius()
                mobj.scale(obj.radius/r).move_to(dim_23(obj.center))

            case EllipseAB() | EllipseCE():
                print("developing")
                pass

            case HyperbolaAB() | HyperbolaCE():
                print("developing")
                pass

            case ParabolaPP():
                print("developing")
                pass

            case _:
                raise NotImplementedError(f"Cannot create mobject from object of type: {type(obj)}")
    
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