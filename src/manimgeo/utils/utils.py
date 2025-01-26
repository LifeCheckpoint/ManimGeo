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
    def circle_circle_intersection(center1: np.ndarray, radius1: float, center2: np.ndarray, radius2: float) -> list[np.ndarray]:
        """
        计算两个圆的交点
        
        return: 交点列表，可能为 []、[point] 或 [point1, point2]
        """
        tol = 1e-8   # 浮点容差

        # 计算圆心距离
        delta = center2 - center1
        d = np.linalg.norm(delta)
        
        # 无交点情形
        if d > radius1 + radius2 + tol:  # 两圆分离
            return []
        if d < np.abs(radius1 - radius2) - tol:  # 一圆包含另一圆
            return []
        if np.isclose(d, 0, atol=tol):  # 同心圆
            return []
        
        # 计算方向向量
        u = delta / d if d > 0 else np.array([1.0, 0.0])
        
        # 中间参数计算
        a = (radius1**2 - radius2**2 + d**2) / (2*d)
        h_squared = radius1**2 - a**2
        
        # 处理浮点误差
        if h_squared < -tol:
            return []
        elif abs(h_squared) < tol:  # 相切
            point = center1 + a * u
            return [point]
        else:  # 两个交点
            h = np.sqrt(h_squared)
            v_perp = np.array([-u[1], u[0]])  # 垂直单位向量
            point1 = center1 + a*u + h*v_perp
            point2 = center1 + a*u - h*v_perp
            return [point1, point2]
        
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
