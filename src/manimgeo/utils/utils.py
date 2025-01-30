from typing import Sequence, Iterable, Dict

class GeoUtils:

    @staticmethod
    def check_params(objs: Sequence, *expected_types):
        """检查参数数量与类型"""
        if len(objs) != len(expected_types):
            raise ValueError(f"Invalid Param number, expected {len(expected_types)} but got {len(objs)}")
        
        for i, (obj, expected_type) in enumerate(zip(objs, expected_types)):
            if not isinstance(obj, expected_type) and expected_type is not None:
                raise ValueError(f"Invalid Param {i}, expected {expected_type.__name__} but got {type(obj).__name__}")
            
    @staticmethod
    def check_params_batch(op_type_map: Dict[str, Sequence], op: str, objs: Sequence):
        """批量检查参数数量与类型"""
        GeoUtils.check_params(objs, op_type_map[op])

    @staticmethod
    def get_name(default_name: str, obj, construct_type: str):
        """以统一方式设置几何对象名称"""
        if default_name is not "":
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
    def geo_print_dependencies(root, depth=0, max_depth=20, visited=None):
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
            GeoUtils.geo_print_dependencies(dep, depth+1, max_depth, visited)


    # @staticmethod
    # def line_circle_intersection(start: np.ndarray, end: np.ndarray, center: np.ndarray, radius: float) -> list[np.ndarray]:
    #     """
    #     计算直线与圆的交点
    #     return: 交点列表，可能为 []、[point] 或 [point1, point2]
    #     """
    #     tol = 1e-8   # 浮点容差

    #     dir_vec = end - start  # 直线的方向向量
    #     op = start - center    # 起点到圆心的向量
        
    #     e = np.dot(dir_vec, dir_vec)
    #     if np.abs(e) < tol:
    #         # 起点和终点重合，直线退化为点
    #         return []
        
    #     d = np.dot(op, dir_vec)
    #     f = np.dot(op, op) - radius**2
        
    #     discriminant = d**2 - e * f
        
    #     if discriminant < -tol:
    #         # 无实交点
    #         return []
    #     elif np.abs(discriminant) < tol:
    #         # 相切，一个交点
    #         t = -d / e
    #         return [start + t * dir_vec]
    #     else:
    #         # 两个交点
    #         sqrt_discriminant = np.sqrt(discriminant)
    #         t1 = (-d + sqrt_discriminant) / e
    #         t2 = (-d - sqrt_discriminant) / e
    #         p1 = start + t1 * dir_vec
    #         p2 = start + t2 * dir_vec
    #         return [p1, p2]
        
    # @staticmethod
    # def calculate_angle(O: np.ndarray, A: np.ndarray, B: np.ndarray) -> float:
    #     """
    #     计算两条射线之间的夹角
    #     """
    #     # 方向向量
    #     v = A - O
    #     w = B - O
        
    #     # 点积和模长
    #     dot_product = np.dot(v, w)
    #     norm_v = np.linalg.norm(v)
    #     norm_w = np.linalg.norm(w)
        
    #     if norm_v == 0 or norm_w == 0:
    #         raise ValueError("Get zero vector.")
        
    #     cos_theta = dot_product / (norm_v * norm_w)
    #     cos_theta = np.clip(cos_theta, -1.0, 1.0)
        
    #     return np.arccos(cos_theta)
