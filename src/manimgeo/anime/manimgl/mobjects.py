from manimgeo.components import *

from manimlib import Mobject
from typing import Dict

dim_23 = lambda x: np.append(x, 0)

class GeoMapManager:
    """管理几何对象到 Mobject 映射"""
    maps: Dict[BaseGeometry, Mobject]
    reverse_maps: Dict[Mobject, BaseGeometry]

    def __init__(self):
        self.maps = {}
        self.reverse_maps = {}

    def create_mobject_from_geometry(
            self,
            obj: Union[
                    PointLike, LineLike, CirclePPP, CirclePP, CircleP,
                    EllipseAB, EllipseCE, HyperbolaAB, HyperbolaCE, ParabolaPP
                ],
            /,
            infinity_line_scale: float = 114
        ):
        """
        通过几何对象创建 Mobject，并自动关联
        """

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
                        dim_23(obj.start.coord + infinity_line_scale*(obj.end.coord - obj.start.coord))
                    )
                elif isinstance(obj, InfinityLinePP):
                    mobject = MLine(
                        dim_23(obj.end.coord + infinity_line_scale*(obj.start.coord - obj.end.coord)),
                        dim_23(obj.start.coord + infinity_line_scale*(obj.end.coord - obj.start.coord))
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
            
        self.maps.update({obj: mobject})
        self.reverse_maps = {v: k for k, v in self.maps.items()}
        return mobject
    
    def bond(self, obj: Dict[BaseGeometry, Mobject]):
        """
        关联
        """
        self.maps.update(obj)
        self.reverse_maps = {v: k for k, v in self.maps.items()}
            
    def release(self, obj: Union[BaseGeometry, List[BaseGeometry]]):
        """
        解除关联
        """
        if isinstance(obj, list):
            for o in obj:
                self.release(o)
        else:
            if isinstance(self.maps.pop(obj, False), bool):
                print(f"Cannot release object: {obj}")
    
    def release_all(self):
        """
        解除所有关联
        """
        self.maps.clear()

    def update_coord(self, p: Mobject):
        """根据 Mobject 更新反向更新对应 FreePoint 坐标，并传递到各个依赖"""

        # 更新叶子
        self.reverse_maps[p].coord = p.get_center()[:2]

        # 将自动更新的坐标值设置到部件上
        def update_mobject(obj: BaseGeometry, /, infinity_line_scale: float = 114):
            # 获取所有依赖
            dependences = obj.dependents

            for dependence in dependences:
                dependence_mobject = self.maps[dependence]

                # 注意匹配父子顺序
                match dependence:
                    case PointLike():
                        dependence_mobject.move_to(dim_23(dependence.coord))

                    case LineLike():
                        from manimlib import Line as MLine
                        dependence_mobject: MLine

                        if isinstance(dependence, LineSegmentPP):
                            dependence_mobject.set_points_by_ends(dim_23(dependence.start.coord), dim_23(dependence.end.coord))

                        elif isinstance(dependence, RayPP):
                            dependence_mobject.set_points_by_ends(
                                dim_23(dependence.start.coord), 
                                dim_23(dependence.start.coord + infinity_line_scale*(dependence.end.coord - dependence.start.coord))
                            )

                        elif isinstance(dependence, InfinityLinePP):
                            dependence_mobject.set_points_by_ends(
                                dim_23(dependence.end.coord + infinity_line_scale*(dependence.start.coord - dependence.end.coord)),
                                dim_23(dependence.start.coord + infinity_line_scale*(dependence.end.coord - dependence.start.coord))
                            )

                    case CircleP() | CirclePP():
                        from manimlib import Circle as MCircle
                        dependence_mobject: MCircle

                        # 需要通过半径计算实际相对缩放
                        r = dependence_mobject.get_radius()
                        dependence_mobject.scale(dependence.radius/r).move_to(dim_23(dependence.center_point.coord))

                    case CirclePPP():
                        from manimlib import Circle as MCircle
                        dependence_mobject: MCircle

                        # 需要通过半径计算实际相对缩放
                        r = dependence_mobject.get_radius()
                        dependence_mobject.scale(dependence.radius/r).move_to(dim_23(dependence.center))

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
                    
                # 当前物件完成更新，对其依赖进行更新
                update_mobject(dependence)

        # 从当前叶子节点开始更新
        update_mobject(self.reverse_maps[p])

    def __enter__(self):
        """
        通过叶子节点追踪所有部件几何运动

        叶子节点:
         - `FreePoint`
         - ...
        """

        # 反向查找推导
        self.reverse_maps = {v: k for k, v in self.maps.items()}

        for obj, mobject in self.maps.items():
            obj: BaseGeometry
            mobject: Mobject

            if isinstance(obj, FreePoint):
                mobject.add_updater(self.update_coord)

    def __exit__(self, exc_type, exc_value, traceback):
        """
        结束 Trace，清理
        """

        for obj, mobject in self.maps.items():
            obj: BaseGeometry
            mobject: Mobject

            if isinstance(obj, FreePoint):
                mobject.remove_updater(self.update_coord)