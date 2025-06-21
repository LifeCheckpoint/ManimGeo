"""
交点相关计算
"""

from .base import close, array2float
from logging import getLogger
import numpy as np
from typing import Literal

logger = getLogger(__name__)

import numpy as np
from typing import Literal, Optional
from .base import close

@array2float
def intersection_line_line(
    line1_start: np.ndarray, 
    line1_end: np.ndarray, 
    line2_start: np.ndarray, 
    line2_end: np.ndarray, 
    line1_type: Literal["LineSegment", "Ray", "InfinityLine"], 
    line2_type: Literal["LineSegment", "Ray", "InfinityLine"], 
    as_infinty: bool = False
) -> Optional[np.ndarray]:
    """
    计算两条线在三维空间中的交点。支持线段、射线和无限长直线
    
    - `line1_start`, `line1_end`: 第一条线的起点和终点
    - `line2_start`, `line2_end`: 第二条线的起点和终点
    - `line1_type`, line2_type: 线类型 ("LineSegment", "Ray", "InfinityLine")
    - `as_infinty`: 如果为True，将所有线视为无限长直线
    
    Returns: `Optional[np.ndarray]`, 交点坐标 (np.ndarray) 或 None（无交点），如果线有重叠（非单点），抛 ValueError
    """
    from .lines import get_parameter_t_on_line, check_paramerized_line_range
    tol = 1e-10  # 数值扰动

    # 处理退化线（起点终点重合）
    if close(line1_start, line1_end):
        line1_end = line1_start + np.array([tol, tol, tol])  # 轻微扰动避免零向量
    if close(line2_start, line2_end):
        line2_end = line2_start + np.array([tol, tol, tol])

    # 计算方向向量
    D1 = line1_end - line1_start
    D2 = line2_end - line2_start

    # 如果启用as_infinty，则将所有线视为无限长
    if as_infinty:
        line1_type = "InfinityLine"
        line2_type = "InfinityLine"

    # 计算连接两条线起点的向量
    P1P2 = line2_start - line1_start

    # 检查平行性 (D1 × D2 ≈ 0)
    cross_D1D2 = np.cross(D1, D2)
    if close(float(np.linalg.norm(cross_D1D2)), 0):

        # 检查是否共线 (P1P2 × D1 ≈ 0)
        if close(float(np.linalg.norm(np.cross(P1P2, D1))), 0):

            # 共线情况 - 计算参数范围
            t1_start = 0.0
            t1_end = 1.0

            # 获取第二条线端点在第一条线上的参数
            t2_start = get_parameter_t_on_line(line2_start, line1_start, line1_end)
            t2_end = get_parameter_t_on_line(line2_end, line1_start, line1_end)
            
            # 确定第一条线的参数范围
            if line1_type == "LineSegment":
                range1 = (t1_start, t1_end)
            elif line1_type == "Ray":
                range1 = (t1_start, float('inf'))
            else:  # InfinityLine
                range1 = (-float('inf'), float('inf'))
            
            # 确定第二条线的参数范围
            if line2_type == "LineSegment":
                range2 = (min(t2_start, t2_end), max(t2_start, t2_end))
            elif line2_type == "Ray":
                # 确定射线方向与D1的关系
                dot_sign = np.sign(np.dot(D2, D1))
                if dot_sign >= 0:
                    range2 = (min(t2_start, t2_end), float('inf'))
                else:
                    range2 = (-float('inf'), max(t2_start, t2_end))
            else:  # InfinityLine
                range2 = (-float('inf'), float('inf'))
            
            # 计算参数范围交集
            low = max(range1[0], range2[0])
            high = min(range1[1], range2[1])
            
            # 检查交集类型
            if close(low, high):
                # 单点交集
                return line1_start + low * D1
            elif low < high:
                # 有重叠段
                raise ValueError("Lines have overlapping segments")
            else:
                # 无交集
                return None
        else:
            # 平行但不共线
            return None

    # 非平行线 - 检查共面性 (P1P2 ⊥ (D1 × D2))
    if not close(np.dot(P1P2, cross_D1D2), 0):
        return None  # 异面直线

    # 解参数方程: line1_start + t*D1 = line2_start + s*D2
    # 构造方程组: [D1, -D2] * [t, s]^T = P1P2
    A = np.array([
        [D1[0], -D2[0]],
        [D1[1], -D2[1]]
    ])
    b = P1P2[:2]
    
    # 处理可能的奇异矩阵
    if close(np.linalg.det(A), 0):
        # 尝试使用其他坐标平面
        A = np.array([[D1[0], -D2[0]], [D1[2], -D2[2]]])
        b = np.array([P1P2[0], P1P2[2]])
        if close(np.linalg.det(A), 0):
            A = np.array([[D1[1], -D2[1]], [D1[2], -D2[2]]])
            b = np.array([P1P2[1], P1P2[2]])
    
    try:
        t, s = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return None  # 方程组无解

    # 验证第三个坐标
    z1 = line1_start[2] + t * D1[2]
    z2 = line2_start[2] + s * D2[2]
    if not close(z1, z2):
        return None  # 不满足三维方程

    # 检查参数范围
    if not check_paramerized_line_range(t, line1_type) or not check_paramerized_line_range(s, line2_type):
        return None

    return line1_start + t * D1
