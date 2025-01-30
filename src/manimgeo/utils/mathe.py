from typing import Tuple, Literal
from numbers import Number
import numpy as np

class GeoMathe:
    @staticmethod
    def unit_direction_vector(start: np.ndarray, end: np.ndarray):
        """计算单位方向向量"""
        if np.allclose(start, end):
            raise ValueError("Start point and end point cannot be the same.")
        return (end - start) / np.linalg.norm(end - start)

    @staticmethod
    def axisymmetric_point(p: np.ndarray, l_start: np.ndarray, l_end: np.ndarray):
        """计算对称点"""
        if GeoMathe.is_point_on_infinite_line(p, l_start, l_end):
            return p.copy()

        u = GeoMathe.unit_direction_vector(l_start, l_end)
        base = l_start # 基点
        ap = p - base
        projection_length = np.dot(ap, u) # 计算投影长度
        proj_vec = projection_length * u # 投影向量
        q = base + proj_vec # 投影点坐标
        return 2 * q - p # 对称点坐标为投影点向量的两倍减去原坐标
    
    @staticmethod
    def is_point_on_infinite_line(p: np.ndarray, l_start: np.ndarray, l_end: np.ndarray):
        """判断点是否在直线上"""
        return np.allclose(GeoMathe.point_to_line_distance(p, l_start, l_end), 0)
    
    @staticmethod
    def point_to_line_distance(p: np.ndarray, l_start: np.ndarray, l_end: np.ndarray):
        """计算点到直线距离"""
        direction = l_end - l_start
        norm_val = np.linalg.norm(direction)
        if norm_val == 0:
            return np.linalg.norm(p - l_start)
        cross_product = np.cross(direction, p - l_start)
        return np.abs(cross_product) / norm_val
    
    @staticmethod
    def vertical_point_to_line(p: np.ndarray, l_start: np.ndarray, l_end: np.ndarray):
        """计算给定点，给定直线的垂足点"""
        if GeoMathe.is_point_on_infinite_line(p, l_start, l_end):
            return p.copy()
        else:
            direction = GeoMathe.unit_direction_vector(l_start, l_end)
            projection_scalar = np.dot(p - l_start, direction)
            return l_start + projection_scalar * direction
        
    @staticmethod
    def vertical_line(l_start: np.ndarray, l_end: np.ndarray):
        direction = GeoMathe.unit_direction_vector(l_start, l_end)
        return np.array([-direction[1], direction[0]])
    
    @staticmethod
    def three_points_circle_r_c(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> Tuple[float, float]:
        """三点内接圆，计算半径与圆心"""
        a = np.linalg.norm(p2 - p3)
        b = np.linalg.norm(p1 - p3)
        c = np.linalg.norm(p1 - p2)
        s = (a + b + c) / 2
        r = a * b * c / (4 * np.sqrt(s * (s - a) * (s - b) * (s - c)))

        if np.linalg.matrix_rank(np.array([p2 - p3, p1 - p3])) == 1:
            raise ValueError("Matrix is singular, points are collinear")

        # 计算圆心
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        # 构造垂直平分线的方程组
        A = np.array([
            [2 * (x2 - x1), 2 * (y2 - y1)],
            [2 * (x3 - x2), 2 * (y3 - y2)]
        ])
        B = np.array([
            x2**2 + y2**2 - x1**2 - y1**2,
            x3**2 + y3**2 - x2**2 - y2**2
        ])

        center = np.linalg.solve(A, B)
        return r, center
    
    @staticmethod
    def inversion_point(p: np.ndarray, center: np.ndarray, r: Number):
        """计算反演点"""
        op = p - center
        d_squared = np.dot(op, op)
        if np.allclose(d_squared, 0):
            raise ValueError("Point p coincides with the center, inversion undefined.")
        k = (r ** 2) / d_squared
        return center + op * k
    
    def check_line_range(
            t: Number,
            line_type: Literal["LineSegment", "Ray", "InfinityLine"]
        ) -> bool:
        """线对象参数范围检查"""
        EPSILON = 1e-8

        if line_type is "LineSegment":
            return -EPSILON <= t <= 1 + EPSILON
        elif line_type is "Ray":
            return t >= -EPSILON
        elif line_type is "InfinityLine":
            return True
        
        raise ValueError(f"{line_type} is not a valid line type")
    
    @staticmethod
    def intersection_line_line(
            l1_start: np.ndarray, l1_end: np.ndarray, 
            l2_start: np.ndarray, l2_end: np.ndarray, 
            l1_type: Literal["LineSegment", "Ray", "InfinityLine"], 
            l2_type: Literal["LineSegment", "Ray", "InfinityLine"], 
            as_infinty=False
        ) -> Tuple[bool, np.ndarray]:
        """计算两直线交点

        `as_infinity`: 是否将线视作无穷长线
        
        return:
         - 无交点: (False, None)
         - 有一交点: (True, np.ndarray)
         - 无穷交点: (True, None)
        """
        u = l1_end - l1_start
        v = l2_end - l2_start
        diff = l2_start - l1_start

        if np.allclose(u, 0):
            raise ValueError("Line 1 is degenerate")
        if np.allclose(v, 0):
            raise ValueError("Line 2 is degenerate")

        cross = np.cross(u, v)
        sqrlen_u = np.dot(u, u)
        sqrlen_v = np.dot(v, v)

        if not np.allclose(cross, 0):
            # 两线不平行，计算参数t和s
            t = np.cross(diff, v) / cross
            s = np.cross(diff, u) / cross

            if as_infinty:
                point = l1_start + t * u
                return (True, point)
            else:
                # 检查参数有效性
                valid_l1 = GeoMathe.check_line_range(t, l1_type)
                valid_l2 = GeoMathe.check_line_range(s, l2_type)

                if valid_l1 and valid_l2:
                    point = l1_start + t * u
                    return (True, point)
                else:
                    return (False, None)
        else:
            # 处理平行或共线情况
            cross_diff_u = np.cross(diff, u)
            if not np.allclose(cross_diff_u, 0):
                # 平行但不共线
                return (False, None)
            else:
                # 共线
                if as_infinty:
                    return (True, None)
                else:
                    # 计算线l2在线l1上的参数范围
                    t2_start = np.dot(l2_start - l1_start, u) / sqrlen_u
                    t2_end = np.dot(l2_end - l1_start, u) / sqrlen_u
                    k = np.dot(v, u) / sqrlen_u

                    # 确定线l1的参数范围
                    if l1_type is "LineSegment":
                        l1_min, l1_max = 0.0, 1.0
                    elif l1_type is "Ray":
                        l1_min, l1_max = 0.0, np.inf
                    elif l1_type is "InfinityLine":
                        l1_min, l1_max = -np.inf, np.inf
                    else:
                        raise ValueError(f"Invalid l1_type: {l1_type}")

                    # 确定线l2的参数范围
                    if l2_type is "LineSegment":
                        l2_min, l2_max = min(t2_start, t2_end), max(t2_start, t2_end)
                    elif l2_type is "Ray":
                        if k > 0:
                            l2_min, l2_max = t2_start, np.inf
                        else:
                            l2_min, l2_max = -np.inf, t2_start
                    elif l2_type is "InfinityLine":
                        l2_min, l2_max = -np.inf, np.inf
                    else:
                        raise ValueError(f"Invalid l2_type: {l2_type}")

                    # 判断参数范围是否有交集
                    has_overlap = not (l1_max < l2_min or l2_max < l1_min)
                    return (True, None) if has_overlap else (False, None)
                
    @staticmethod
    def intersection_cir_cir(center1: np.ndarray, radius1: Number, center2: np.ndarray, radius2: Number) -> list[np.ndarray]:
        """
        计算两个圆的交点
        
        return:
        
        交点列表，可能为 (True, [intersections]), (True, None) 或 (False, None)，表示交点、无穷交点、无交点

        [intersections] 可能为 [point] 或 [point1, point2]
        """
        EPSILON = 1e-8   # 浮点容差

        # 计算圆心距离
        delta = center2 - center1
        d = np.linalg.norm(delta)
        
        # 处理同心圆情况
        if np.isclose(d, 0):
            # 同心圆但半径不同，无交点；半径相同则重合
            return (True, None)
        
        # 无交点情形
        if d > radius1 + radius2 + EPSILON:  # 两圆分离
            return (False, None)
        if d < abs(radius1 - radius2) - EPSILON:  # 一圆包含另一圆
            return (False, None)
        
        # 计算方向向量
        u = delta / d
        
        # 中间参数计算
        a = (radius1**2 - radius2**2 + d**2) / (2*d)
        h_squared = radius1**2 - a**2
        
        # 处理浮点误差
        if h_squared < -EPSILON:
            return (False, None)
        elif abs(h_squared) < EPSILON:  # 相切
            point = center1 + a * u
            return (True, [point])
        else:  # 两个交点
            h = np.sqrt(h_squared)
            v_perp = np.array([-u[1], u[0]])  # 垂直单位向量
            point1 = center1 + a*u + h*v_perp
            point2 = center1 + a*u - h*v_perp
            return (True, [point1, point2])

    @staticmethod
    def angle_3p_countclockwise(start: np.ndarray, center: np.ndarray, end: np.ndarray):
        """计算三点逆时针角度"""
        vec1 = np.array(start) - np.array(center)
        vec2 = np.array(end) - np.array(center)
        
        dot = np.dot(vec1, vec2)
        det = np.cross(vec1, vec2)
        
        angle_rad = np.arctan2(det, dot)
        angle_rad = angle_rad if angle_rad >= 0 else angle_rad + 2 * np.pi
        
        return angle_rad