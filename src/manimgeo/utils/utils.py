import numpy as np
from typing import Sequence

class GeoUtils:
    @staticmethod
    def normalize(data: np.ndarray) -> np.ndarray:
        """获取单位向量"""
        norm = np.sum(data)
        if norm < 1e-10:  # 防止除以0
            return np.zeros_like(data)
        return data / norm
    
    @staticmethod
    def cross_product(v1, v2):
        """计算二维向量叉积"""
        return v1[0] * v2[1] - v1[1] * v2[0]
    
    @staticmethod
    def line_circle_intersection(start: np.ndarray, end: np.ndarray, center: np.ndarray, radius: float) -> list[np.ndarray]:
        """
        计算直线与圆的交点
        return: 交点列表，可能为 []、[point] 或 [point1, point2]
        """
        tol = 1e-8   # 浮点容差

        dir_vec = end - start  # 直线的方向向量
        op = start - center    # 起点到圆心的向量
        
        e = np.dot(dir_vec, dir_vec)
        if np.abs(e) < tol:
            # 起点和终点重合，直线退化为点
            return []
        
        d = np.dot(op, dir_vec)
        f = np.dot(op, op) - radius**2
        
        discriminant = d**2 - e * f
        
        if discriminant < -tol:
            # 无实交点
            return []
        elif np.abs(discriminant) < tol:
            # 相切，一个交点
            t = -d / e
            return [start + t * dir_vec]
        else:
            # 两个交点
            sqrt_discriminant = np.sqrt(discriminant)
            t1 = (-d + sqrt_discriminant) / e
            t2 = (-d - sqrt_discriminant) / e
            p1 = start + t1 * dir_vec
            p2 = start + t2 * dir_vec
            return [p1, p2]
        
    
        
    @staticmethod
    def calculate_angle(O: np.ndarray, A: np.ndarray, B: np.ndarray) -> float:
        """
        计算两条射线之间的夹角
        """
        # 方向向量
        v = A - O
        w = B - O
        
        # 点积和模长
        dot_product = np.dot(v, w)
        norm_v = np.linalg.norm(v)
        norm_w = np.linalg.norm(w)
        
        if norm_v == 0 or norm_w == 0:
            raise ValueError("Get zero vector.")
        
        cos_theta = dot_product / (norm_v * norm_w)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        
        return np.arccos(cos_theta)

    @staticmethod
    def check_params(objs: Sequence, *expected_types):
        """检查参数数量与类型"""
        if len(objs) != len(expected_types):
            raise ValueError(f"Invalid Param number, expected {len(expected_types)} but got {len(objs)}")
        
        for i, (obj, expected_type) in enumerate(zip(objs, expected_types)):
            if not isinstance(obj, expected_type) and expected_type is not None:
                raise ValueError(f"Invalid Param {i}, expected {expected_type.__name__} but got {type(obj).__name__}")

    @staticmethod
    def get_name(default_name: str, obj, construct_type: str):
        """以统一方式设置几何对象名称"""
        if default_name is not "":
            return default_name
        else:
            return f"{type(obj).__name__}[{construct_type}]@{id(obj)%10000}"
