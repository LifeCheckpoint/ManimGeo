import numpy as np

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
    def point_to_line_distance(base_point: np.ndarray, unit_direction: np.ndarray, point: np.ndarray):
        """计算点到直线距离"""
        # 转换为NumPy数组
        base_point = np.array(base_point)
        unit_direction = np.array(unit_direction)
        point = np.array(point)
        # 计算向量 v
        v = point - base_point
        # 计算投影向量
        v_proj = np.dot(v, unit_direction) * unit_direction
        # 计算垂直向量
        v_perp = v - v_proj
        # 返回垂直向量的长度
        return np.linalg.norm(v_perp)
    
    @staticmethod
    def unit_direction_vector(base_point: np.ndarray, target_point: np.ndarray):
        """计算单位方向向量"""
        return (target_point - base_point) / np.linalg.norm(target_point - base_point)
