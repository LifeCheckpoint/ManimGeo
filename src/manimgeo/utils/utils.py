from typing import Sequence, Iterable, Dict, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from manimgeo.components import *

class GeoUtils:
    GEO_PRINT_EXC: bool = False
    
    @staticmethod
    def check_params(objs: Sequence, *expected_types):
        """检查参数数量与类型"""
        if len(objs) != len(expected_types):
            raise ValueError(f"Invalid Param number, expected {len(expected_types)} but got {len(objs)}")
        
        for i, (obj, expected_type) in enumerate(zip(objs, expected_types)):
            if expected_type is not None and not isinstance(obj, expected_type):
                raise ValueError(f"Invalid Param {i}, expected {expected_type.__name__} but got {type(obj).__name__}")
            
    @staticmethod
    def check_params_batch(op_type_map: Dict[str, Sequence], op: str, objs: Sequence):
        """批量检查参数数量与类型"""
        GeoUtils.check_params(objs, *op_type_map[op])

    @staticmethod
    def get_name(default_name: str, obj, construct_type: str):
        """以统一方式设置几何对象名称"""
        if default_name != "":
            return default_name
        else:
            return f"{type(obj).__name__}[{construct_type}]@{id(obj)%10000}"

    @staticmethod
    def flatten(iterable: Iterable):
        """展平对象"""
        for item in iterable:
            if isinstance(item, list):
                yield from GeoUtils.flatten(item)
            else:
                yield item

    @staticmethod
    def print_dependencies(root, depth=0, max_depth=20, visited=None):
        """绘制依赖关系"""
        from manimgeo.utils.output import color_text, generate_color_from_id
        
        if root is None:
            print("  "*depth + "· None")
            return
            
        if depth > max_depth:
            print("  "*depth + "· ... (max depth reached)")
            return
        
        name_str = f" - ({root.name})" if hasattr(root, 'name') and root.name else ""
        print("  "*depth + f"· {color_text(type(root).__name__, *generate_color_from_id(root))}{name_str}")
        
        if not hasattr(root, 'dependents'):
            return
            
        for dep in root.dependents:
            GeoUtils.print_dependencies(dep, depth+1, max_depth, visited)

    @staticmethod
    def set_debug(debug: bool = True):
        """输出错误信息"""
        GeoUtils.GEO_PRINT_EXC = debug