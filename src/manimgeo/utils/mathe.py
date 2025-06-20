from typing import Tuple, Literal, List, Union, overload
import numpy as np
Number = Union[float, int]

__all__ = ["GeoMathe"]

class GeoMathe:
    _atol = 1e-9       # 绝对容差
    _rtol = 1e-9       # 相对容差
    _epsilon = 1e-3    # 自定义操作容差

    @classmethod
    def close(cls, a: np.ndarray | Number, b: np.ndarray | Number) -> bool:
        """判断两个数值是否相等"""
        if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
            return np.allclose(a, b, atol=GeoMathe._atol, rtol=GeoMathe._rtol)
        elif isinstance(a, Number) and isinstance(b, Number):
            return np.isclose(a, b, atol=GeoMathe._atol, rtol=GeoMathe._rtol)
        else:
            raise ValueError(f"Arguments must be either np.ndarray or Number, get {type(a)} and {type(b)}")

    @classmethod
    def set_precision(
        cls,
        atol: float = None,
        rtol: float = None,
        epsilon: float = None
    ):
        """
        设置精度参数
        `atol`: 绝对容差
        `rtol`: 相对容差
        `epsilon`: 自定义操作容差（如范围检查）
        """
        if atol is not None:
            cls._atol = atol
        if rtol is not None:
            cls._rtol = rtol
        if epsilon is not None:
            cls._epsilon = epsilon
            
    @staticmethod
    def unit_direction_vector(start: np.ndarray, end: np.ndarray):
        """计算单位方向向量"""
        if GeoMathe.close(start, end):
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
        return GeoMathe.close(GeoMathe.point_to_line_distance(p, l_start, l_end), 0)
    
    @staticmethod
    def point_to_line_distance(p: np.ndarray, l_start: np.ndarray, l_end: np.ndarray):
        """计算点到直线距离"""
        direction = l_end - l_start
        norm_val = np.linalg.norm(direction)
        if GeoMathe.close(norm_val, 0):
            return np.linalg.norm(p - l_start)
        cross_product = np.cross(direction, p - l_start)
        return np.abs(cross_product) / norm_val
    
    @staticmethod
    def vertical_point_to_line(p: np.ndarray, l_start: np.ndarray, l_end: np.ndarray):
        """计算给定点，给定直线的垂足点"""
        if GeoMathe.is_point_on_infinite_line(p, l_start, l_end):
            return p.copy()
        else:
            v = l_end - l_start
            v_squared_norm = float(np.dot(v, v))
            if GeoMathe.close(v_squared_norm, 0):
                return l_start.copy()
            projection_scalar_alt = np.dot(p - l_start, v) / v_squared_norm
            return l_start + projection_scalar_alt * v
        
    @staticmethod
    def vertical_line_unit_direction(l_start: np.ndarray, l_end: np.ndarray):
        """计算给定直线的垂线方向向量"""
        direction = GeoMathe.unit_direction_vector(l_start, l_end)
        return np.array([-direction[1], direction[0]])
    
    @staticmethod
    def inscribed_r_c(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> Tuple[float, np.ndarray]:
        """三点内接圆，计算半径与圆心"""
        a = np.linalg.norm(p2 - p3)
        b = np.linalg.norm(p3 - p1)
        c = np.linalg.norm(p1 - p2)
        coord = (a * p1 + b * p2 + c * p3) / (a + b + c)
        p = (a + b + c) / 2
        r = np.sqrt((p - a) * (p - b) * (p - c) / p)
        return r, coord
    
    @staticmethod
    def circumcenter_r_c(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> Tuple[float, np.ndarray]:
        """三点外接圆，计算半径与圆心"""
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
    def orthocenter(a, b, c):
        """计算三点垂心坐标"""
        x1, y1 = a[0], a[1]
        x2, y2 = b[0], b[1]
        x3, y3 = c[0], c[1]
        
        # 计算方程组系数
        a1 = x3 - x2
        b1 = y3 - y2
        c1 = a1 * x1 + b1 * y1  # (x3-x2)*x1 + (y3-y2)*y1
        
        a2 = x2 - x1
        b2 = y2 - y1
        c2 = a2 * x3 + b2 * y3  # (x2-x1)*x3 + (y2-y1)*y3
        
        # 计算分母
        denominator = a1 * b2 - a2 * b1
        if GeoMathe.close(denominator, 0):
            raise ValueError("Three points are degenerated")
        
        # 克拉默法则求解
        x0 = (c1 * b2 - c2 * b1) / denominator
        y0 = (a1 * c2 - a2 * c1) / denominator
        
        return np.array([x0, y0])
    
    @staticmethod
    def inversion_point(p: np.ndarray, center: np.ndarray, r: Number):
        """计算反演点"""
        op = p - center
        d_squared = np.dot(op, op)
        if GeoMathe.close(d_squared, 0):
            raise ValueError("Point p coincides with the center, inversion undefined.")
        k = (r ** 2) / d_squared
        return center + op * k
    
    def check_line_range(
            t: Number,
            line_type: Literal["LineSegment", "Ray", "InfinityLine"]
        ) -> bool:
        """线对象参数范围检查"""
        EPSILON = 1e-8

        if line_type == "LineSegment":
            return -EPSILON <= t <= 1 + EPSILON
        elif line_type == "Ray":
            return t >= -EPSILON
        elif line_type == "InfinityLine":
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

        if GeoMathe.close(u, np.zeros(2)):
            raise ValueError("Line 1 is degenerate")
        if GeoMathe.close(v, np.zeros(2)):
            raise ValueError("Line 2 is degenerate")

        cross = np.cross(u, v)
        sqrlen_u = np.dot(u, u)
        sqrlen_v = np.dot(v, v)

        if not GeoMathe.close(cross, np.zeros(2)):
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
            if not GeoMathe.close(cross_diff_u, np.zeros(2)):
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
                    if l1_type == "LineSegment":
                        l1_min, l1_max = 0.0, 1.0
                    elif l1_type == "Ray":
                        l1_min, l1_max = 0.0, np.inf
                    elif l1_type == "InfinityLine":
                        l1_min, l1_max = -np.inf, np.inf
                    else:
                        raise ValueError(f"Invalid l1_type: {l1_type}")

                    # 确定线l2的参数范围
                    if l2_type == "LineSegment":
                        l2_min, l2_max = min(t2_start, t2_end), max(t2_start, t2_end)
                    elif l2_type == "Ray":
                        if k > 0:
                            l2_min, l2_max = t2_start, np.inf
                        else:
                            l2_min, l2_max = -np.inf, t2_start
                    elif l2_type == "InfinityLine":
                        l2_min, l2_max = -np.inf, np.inf
                    else:
                        raise ValueError(f"Invalid l2_type: {l2_type}")

                    # 判断参数范围是否有交集
                    has_overlap = not (l1_max < l2_min or l2_max < l1_min)
                    return (True, None) if has_overlap else (False, None)

    @staticmethod
    def intersection_line_cir(
            l_start: np.ndarray, l_end: np.ndarray, 
            center: np.ndarray, radius: float, 
            line_type: Literal["LineSegment", "Ray", "InfinityLine"]
        ) -> List[np.ndarray]:
        """计算线段、射线或无限直线与圆的交点"""
        x1, y1 = l_start[0], l_start[1]
        x2, y2 = l_end[0], l_end[1]
        a, b = center[0], center[1]
        dx = x2 - x1
        dy = y2 - y1

        # 处理线段退化为点的情况
        if GeoMathe.close(dx, 0) and GeoMathe.close(dy, 0):
            distance_sq = (x1 - a)**2 + (y1 - b)**2
            if GeoMathe.close(distance_sq, radius**2):
                return [np.array([x1, y1])]
            else:
                return []

        # 计算二次方程系数
        A = dx**2 + dy**2
        B = 2 * ((x1 - a) * dx + (y1 - b) * dy)
        C = (x1 - a)**2 + (y1 - b)**2 - radius**2

        # 计算判别式
        delta = B**2 - 4 * A * C
        intersections = []

        if delta < -GeoMathe._epsilon:
            return []
        if -GeoMathe._epsilon < delta < 0:
            delta = 0

        sqrt_delta = np.sqrt(delta)
        t_values = []
        if GeoMathe.close(delta, 0):
            t = -B / (2 * A)
            t_values.append(t)
        else:
            t1 = (-B - sqrt_delta) / (2 * A)
            t2 = (-B + sqrt_delta) / (2 * A)
            t_values.extend([t1, t2])

        # 根据线类型筛选有效t值
        valid_ts = []
        for t in t_values:
            if line_type == "LineSegment":
                if 0 <= t <= 1:
                    valid_ts.append(t)
            elif line_type == "Ray":
                if t >= 0:
                    valid_ts.append(t)
            elif line_type == "InfinityLine":
                valid_ts.append(t)

        # 计算交点并去重
        for t in valid_ts:
            x = x1 + t * dx
            y = y1 + t * dy
            point = np.array([x, y])

            is_duplicate = False
            for existing_point in intersections:
                if GeoMathe.close(point, existing_point):
                    is_duplicate = True
                    break
            if not is_duplicate:
                intersections.append(point)

        return intersections
                
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
        if GeoMathe.close(d, 0):
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
    def find_tangent_points(coord: np.ndarray, center: np.ndarray, radius: float) -> List[np.ndarray]:
        dx = coord[0] - center[0]
        dy = coord[1] - center[1]
        d_squared = dx**2 + dy**2
        
        if GeoMathe.close(d_squared, 0):  # 点与圆心重合，无切点
            return []
        if d_squared < radius**2:  # 点在圆内，无切点
            return []
        
        d = np.sqrt(d_squared)
        r = radius
        if GeoMathe.close(d, r):  # 点在圆上，切点即自身
            return [coord.copy()]
        
        # 计算切点坐标
        sqrt_term = np.sqrt(d_squared - r**2)
        factor = r / d_squared
        term1_x = dx * r
        term1_y = dy * r
        term2_x = -dy * sqrt_term
        term2_y = dx * sqrt_term
        
        t1 = np.array([
            center[0] + factor * (term1_x + term2_x),
            center[1] + factor * (term1_y + term2_y)
        ])
        
        t2 = np.array([
            center[0] + factor * (term1_x - term2_x),
            center[1] + factor * (term1_y - term2_y)
        ])
        
        return [t1, t2]

    @staticmethod
    def angle_3p_countclockwise(start: np.ndarray, center: np.ndarray, end: np.ndarray) -> float:
        """计算三点逆时针角度"""
        vec1 = np.array(start) - np.array(center)
        vec2 = np.array(end) - np.array(center)
        
        dot = np.dot(vec1, vec2)
        det = np.cross(vec1, vec2)
        
        angle_rad = np.arctan2(det, dot)
        angle_rad = angle_rad if angle_rad >= 0 else angle_rad + 2 * np.pi
        
        return angle_rad

    @staticmethod
    def compute_tangent_point(A, B, C, center, r):
        """计算直线Ax + By + C = 0与圆心为center、半径为r的切点"""
        x0, y0 = center
        denominator = A**2 + B**2
        
        # 处理分母为零
        if GeoMathe.close(denominator, 0):
            raise ValueError("Invalid line equation: A and B cannot both be zero.")
        
        # 计算垂足点坐标
        x = (B**2 * x0 - A*B*y0 - A*C) / denominator
        y = (-A*B*x0 + A**2*y0 - B*C) / denominator
        
        return np.array([x, y])

    @staticmethod
    def external_tangents(
            center1: np.ndarray, 
            r1: Number, 
            center2: np.ndarray, 
            r2: Number
        ) -> List[Tuple[np.ndarray, np.ndarray]]:
        """返回两圆的外公切线切点对列表"""
        x1, y1 = center1
        x2, y2 = center2
        dx, dy = x2 - x1, y2 - y1
        d_sq = dx**2 + dy**2
        
        # 计算外切线判别式
        deta = d_sq - (r1 - r2)**2
        if deta < 0 or GeoMathe.close(deta, 0):
            return []
        
        sqrt_d = np.sqrt(deta)
        p1 = r1 * (x2**2 + y2**2 - x1*x2 - y1*y2)
        p2 = r2 * (x1**2 + y1**2 - x1*x2 - y1*y2)
        q = x1*y2 - x2*y1
        
        # 生成两条外切线的参数
        tangents = []
        for sign in [1, -1]:
            A = dx*(r1 - r2) - dy*sqrt_d*sign
            B = dy*(r1 - r2) + dx*sqrt_d*sign
            C = -p1 - p2 + q*sqrt_d*sign
            
            # 计算切点并验证
            try:
                pt1 = GeoMathe.compute_tangent_point(A, B, C, center1, r1)
                pt2 = GeoMathe.compute_tangent_point(A, B, C, center2, r2)
                tangents.append((pt1, pt2))
            except ValueError:
                continue
        
        return tangents

    @staticmethod
    def internal_tangents(
            center1: np.ndarray, 
            r1: Number, 
            center2: np.ndarray, 
            r2: Number
        ) -> List[Tuple[np.ndarray, np.ndarray]]:
        """返回两圆的内公切线切点对列表"""
        x1, y1 = center1
        x2, y2 = center2
        dx, dy = x2 - x1, y2 - y1
        d_sq = dx**2 + dy**2
        
        # 计算内切线判别式
        deta = d_sq - (r1 + r2)**2
        if deta < 0 or GeoMathe.close(deta, 0):
            return []
        
        sqrt_d = np.sqrt(deta)
        p1 = r1 * (x2**2 + y2**2 - x1*x2 - y1*y2)
        p2 = r2 * (x1**2 + y1**2 - x1*x2 - y1*y2)
        q = x1*y2 - x2*y1
        
        # 生成两条内切线的参数
        tangents = []
        for sign in [1, -1]:
            A = dx*(r1 + r2) - dy*sqrt_d*sign
            B = dy*(r1 + r2) + dx*sqrt_d*sign
            C = -p1 + p2 + q*sqrt_d*sign
            
            # 计算切点并验证
            try:
                pt1 = GeoMathe.compute_tangent_point(A, B, C, center1, r1)
                pt2 = GeoMathe.compute_tangent_point(A, B, C, center2, r2)
                tangents.append((pt1, pt2))
            except ValueError:
                continue
        
        return tangents
    
    @staticmethod
    def inverse_circle(
            circle_center: np.ndarray, r_circle: Number, 
            base_circle_center: np.ndarray, r_base_circle: Number
        ) -> Tuple[np.ndarray, Number]:
        """计算 circle 关于 base_circle 的反形圆圆心坐标和半径"""
        x_A = circle_center[0]
        y_A = circle_center[1]
        x_B = base_circle_center[0]
        y_B = base_circle_center[1]
        
        # 平移坐标系，使圆B的圆心位于原点
        a = x_A - x_B
        b = y_A - y_B
        
        # 计算分母D
        D = a**2 + b**2 - r_circle**2
        
        # 计算反形圆心（平移后坐标系）
        inv_center_x_translated = a * r_base_circle**2 / D
        inv_center_y_translated = b * r_base_circle**2 / D
        
        # 转换回原坐标系
        inv_center_x = inv_center_x_translated + x_B
        inv_center_y = inv_center_y_translated + y_B
        
        # 计算反形半径
        inv_radius = (r_circle * r_base_circle**2) / np.abs(D)
        
        return np.array((inv_center_x, inv_center_y)), inv_radius