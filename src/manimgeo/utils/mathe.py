# class GeoMathe:
#     _atol = 1e-9       # 绝对容差
#     _rtol = 1e-9       # 相对容差
#     _epsilon = 1e-3    # 自定义操作容差
    

#     @staticmethod
#     def intersection_line_cir(
#             l_start: np.ndarray, l_end: np.ndarray, 
#             center: np.ndarray, radius: float, 
#             line_type: Literal["LineSegment", "Ray", "InfinityLine"]
#         ) -> List[np.ndarray]:
#         """计算线段、射线或无限直线与圆的交点"""
#         x1, y1 = l_start[0], l_start[1]
#         x2, y2 = l_end[0], l_end[1]
#         a, b = center[0], center[1]
#         dx = x2 - x1
#         dy = y2 - y1

#         # 处理线段退化为点的情况
#         if GeoMathe.close(dx, 0) and GeoMathe.close(dy, 0):
#             distance_sq = (x1 - a)**2 + (y1 - b)**2
#             if GeoMathe.close(distance_sq, radius**2):
#                 return [np.array([x1, y1])]
#             else:
#                 return []

#         # 计算二次方程系数
#         A = dx**2 + dy**2
#         B = 2 * ((x1 - a) * dx + (y1 - b) * dy)
#         C = (x1 - a)**2 + (y1 - b)**2 - radius**2

#         # 计算判别式
#         delta = B**2 - 4 * A * C
#         intersections = []

#         if delta < -GeoMathe._epsilon:
#             return []
#         if -GeoMathe._epsilon < delta < 0:
#             delta = 0

#         sqrt_delta = np.sqrt(delta)
#         t_values = []
#         if GeoMathe.close(delta, 0):
#             t = -B / (2 * A)
#             t_values.append(t)
#         else:
#             t1 = (-B - sqrt_delta) / (2 * A)
#             t2 = (-B + sqrt_delta) / (2 * A)
#             t_values.extend([t1, t2])

#         # 根据线类型筛选有效t值
#         valid_ts = []
#         for t in t_values:
#             if line_type == "LineSegment":
#                 if 0 <= t <= 1:
#                     valid_ts.append(t)
#             elif line_type == "Ray":
#                 if t >= 0:
#                     valid_ts.append(t)
#             elif line_type == "InfinityLine":
#                 valid_ts.append(t)

#         # 计算交点并去重
#         for t in valid_ts:
#             x = x1 + t * dx
#             y = y1 + t * dy
#             point = np.array([x, y])

#             is_duplicate = False
#             for existing_point in intersections:
#                 if GeoMathe.close(point, existing_point):
#                     is_duplicate = True
#                     break
#             if not is_duplicate:
#                 intersections.append(point)

#         return intersections
                
#     @staticmethod
#     def intersection_cir_cir(center1: np.ndarray, radius1: Number, center2: np.ndarray, radius2: Number) -> list[np.ndarray]:
#         """
#         计算两个圆的交点
        
#         return:
        
#         交点列表，可能为 (True, [intersections]), (True, None) 或 (False, None)，表示交点、无穷交点、无交点

#         [intersections] 可能为 [point] 或 [point1, point2]
#         """
#         EPSILON = 1e-8   # 浮点容差

#         # 计算圆心距离
#         delta = center2 - center1
#         d = np.linalg.norm(delta)
        
#         # 处理同心圆情况
#         if GeoMathe.close(d, 0):
#             # 同心圆但半径不同，无交点；半径相同则重合
#             return (True, None)
        
#         # 无交点情形
#         if d > radius1 + radius2 + EPSILON:  # 两圆分离
#             return (False, None)
#         if d < abs(radius1 - radius2) - EPSILON:  # 一圆包含另一圆
#             return (False, None)
        
#         # 计算方向向量
#         u = delta / d
        
#         # 中间参数计算
#         a = (radius1**2 - radius2**2 + d**2) / (2*d)
#         h_squared = radius1**2 - a**2
        
#         # 处理浮点误差
#         if h_squared < -EPSILON:
#             return (False, None)
#         elif abs(h_squared) < EPSILON:  # 相切
#             point = center1 + a * u
#             return (True, [point])
#         else:  # 两个交点
#             h = np.sqrt(h_squared)
#             v_perp = np.array([-u[1], u[0]])  # 垂直单位向量
#             point1 = center1 + a*u + h*v_perp
#             point2 = center1 + a*u - h*v_perp
#             return (True, [point1, point2])
        
#     @staticmethod
#     def find_tangent_points(coord: np.ndarray, center: np.ndarray, radius: float) -> List[np.ndarray]:
#         dx = coord[0] - center[0]
#         dy = coord[1] - center[1]
#         d_squared = dx**2 + dy**2
        
#         if GeoMathe.close(d_squared, 0):  # 点与圆心重合，无切点
#             return []
#         if d_squared < radius**2:  # 点在圆内，无切点
#             return []
        
#         d = np.sqrt(d_squared)
#         r = radius
#         if GeoMathe.close(d, r):  # 点在圆上，切点即自身
#             return [coord.copy()]
        
#         # 计算切点坐标
#         sqrt_term = np.sqrt(d_squared - r**2)
#         factor = r / d_squared
#         term1_x = dx * r
#         term1_y = dy * r
#         term2_x = -dy * sqrt_term
#         term2_y = dx * sqrt_term
        
#         t1 = np.array([
#             center[0] + factor * (term1_x + term2_x),
#             center[1] + factor * (term1_y + term2_y)
#         ])
        
#         t2 = np.array([
#             center[0] + factor * (term1_x - term2_x),
#             center[1] + factor * (term1_y - term2_y)
#         ])
        
#         return [t1, t2]

#     @staticmethod
#     def compute_tangent_point(A, B, C, center, r):
#         """计算直线Ax + By + C = 0与圆心为center、半径为r的切点"""
#         x0, y0 = center
#         denominator = A**2 + B**2
        
#         # 处理分母为零
#         if GeoMathe.close(denominator, 0):
#             raise ValueError("Invalid line equation: A and B cannot both be zero.")
        
#         # 计算垂足点坐标
#         x = (B**2 * x0 - A*B*y0 - A*C) / denominator
#         y = (-A*B*x0 + A**2*y0 - B*C) / denominator
        
#         return np.array([x, y])

#     @staticmethod
#     def external_tangents(
#             center1: np.ndarray, 
#             r1: Number, 
#             center2: np.ndarray, 
#             r2: Number
#         ) -> List[Tuple[np.ndarray, np.ndarray]]:
#         """返回两圆的外公切线切点对列表"""
#         x1, y1 = center1
#         x2, y2 = center2
#         dx, dy = x2 - x1, y2 - y1
#         d_sq = dx**2 + dy**2
        
#         # 计算外切线判别式
#         deta = d_sq - (r1 - r2)**2
#         if deta < 0 or GeoMathe.close(deta, 0):
#             return []
        
#         sqrt_d = np.sqrt(deta)
#         p1 = r1 * (x2**2 + y2**2 - x1*x2 - y1*y2)
#         p2 = r2 * (x1**2 + y1**2 - x1*x2 - y1*y2)
#         q = x1*y2 - x2*y1
        
#         # 生成两条外切线的参数
#         tangents = []
#         for sign in [1, -1]:
#             A = dx*(r1 - r2) - dy*sqrt_d*sign
#             B = dy*(r1 - r2) + dx*sqrt_d*sign
#             C = -p1 - p2 + q*sqrt_d*sign
            
#             # 计算切点并验证
#             try:
#                 pt1 = GeoMathe.compute_tangent_point(A, B, C, center1, r1)
#                 pt2 = GeoMathe.compute_tangent_point(A, B, C, center2, r2)
#                 tangents.append((pt1, pt2))
#             except ValueError:
#                 continue
        
#         return tangents

#     @staticmethod
#     def internal_tangents(
#             center1: np.ndarray, 
#             r1: Number, 
#             center2: np.ndarray, 
#             r2: Number
#         ) -> List[Tuple[np.ndarray, np.ndarray]]:
#         """返回两圆的内公切线切点对列表"""
#         x1, y1 = center1
#         x2, y2 = center2
#         dx, dy = x2 - x1, y2 - y1
#         d_sq = dx**2 + dy**2
        
#         # 计算内切线判别式
#         deta = d_sq - (r1 + r2)**2
#         if deta < 0 or GeoMathe.close(deta, 0):
#             return []
        
#         sqrt_d = np.sqrt(deta)
#         p1 = r1 * (x2**2 + y2**2 - x1*x2 - y1*y2)
#         p2 = r2 * (x1**2 + y1**2 - x1*x2 - y1*y2)
#         q = x1*y2 - x2*y1
        
#         # 生成两条内切线的参数
#         tangents = []
#         for sign in [1, -1]:
#             A = dx*(r1 + r2) - dy*sqrt_d*sign
#             B = dy*(r1 + r2) + dx*sqrt_d*sign
#             C = -p1 + p2 + q*sqrt_d*sign
            
#             # 计算切点并验证
#             try:
#                 pt1 = GeoMathe.compute_tangent_point(A, B, C, center1, r1)
#                 pt2 = GeoMathe.compute_tangent_point(A, B, C, center2, r2)
#                 tangents.append((pt1, pt2))
#             except ValueError:
#                 continue
        
#         return tangents
