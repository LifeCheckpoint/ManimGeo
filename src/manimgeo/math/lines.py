from .base import close, array2float, Number
from typing import Literal
from logging import getLogger
import numpy as np

logger = getLogger(__name__)

def check_paramerized_line_range(t: Number, line_type: Literal["LineSegment", "Ray", "InfinityLine"]):
    """
    检查参数化直线的范围是否符合要求
    - `t`: 参数值
    - `line_type`: 直线类型，可为 "LineSegment", "Ray", "InfinityLine"
    """
    # 检查端点，如果接近则认为符合
    if close(t, 0) or close(t, 1):
        return True

    if line_type == "LineSegment":
        return 0 <= t <= 1
    elif line_type == "Ray":
        return t >= 0
    elif line_type == "InfinityLine":
        return True
    else:
        logger.error(f"未知的直线类型: {line_type}")
        raise ValueError(f"未知的直线类型: {line_type}")

@array2float
def vertical_line_unit_direction(line_start: np.ndarray, line_end: np.ndarray, turn: Literal["clockwise", "counterclockwise"] = "counterclockwise") -> np.ndarray:
    """计算给定直线的垂线方向向量"""
    from .vectors import unit_direction_vector
    direction = unit_direction_vector(line_start, line_end)
    direction[0], direction[1] = -direction[1], direction[0]
    return direction if turn == "counterclockwise" else -direction

@array2float
def point_to_line_distance(point: np.ndarray, line_start: np.ndarray, line_end: np.ndarray):
    """
    计算点到直线的距离

    - `point`: 要计算距离的点
    - `line_start`: 直线起点
    - `line_end`: 直线终点

    Returns: `float`, 点到直线的距离
    """
    direction = line_end - line_start
    norm_val = float(np.linalg.norm(direction))

    # 直线退化为一点
    if close(norm_val, 0):
        return np.linalg.norm(point - line_start) # 点到点的距离
    
    # 向量 AP，从直线上一点到点 P
    vec_ap = point - line_start
    # 叉积
    cross_product_result = np.cross(direction, vec_ap)
    cross_product_magnitude = np.linalg.norm(cross_product_result)
    
    return cross_product_magnitude / norm_val

@array2float
def get_parameter_t_on_line(point: np.ndarray, line_start: np.ndarray, line_end: np.ndarray) -> float:
    """
    计算点 p 在参数化直线 l_start + t * (l_end - l_start) 上的参数 t 值，假设点 p 已经在直线上。

    - `point`: 要计算的点
    - `line_start`: 直线起点
    - `line_end`: 直线终点
    """
    direction = line_end - line_start
    norm_sq = np.dot(direction, direction) # direction 向量模长的平方
    
    if close(norm_sq, 0):
        logger.warning(f"无法计算参数 t，直线退化为点 (l_start 和 l_end 重合): {line_start}, {line_end}")
        raise ValueError(f"无法计算参数 t，直线退化为点 (l_start 和 l_end 重合): {line_start}, {line_end}")
    
    vec_ap = point - line_start
    t = np.dot(vec_ap, direction) / norm_sq
    return t

@array2float
def is_point_on_line(point: np.ndarray, line_start: np.ndarray, line_end: np.ndarray, line_type: Literal["LineSegment", "Ray", "InfinityLine"] = "InfinityLine") -> bool:
    """
    判断点是否在线上

    - `point`: 要判断的点
    - `line_start`: 线起点
    - `line_end`: 线终点
    - `line_type`: 线类型，可为 "LineSegment", "Ray", "InfinityLine"
    """
    # 首先判断点是否在无限直线上
    distance = float(point_to_line_distance(point, line_start, line_end))

    if not close(distance, 0):
        return False # 点不在直线上
    
    # 如果直线退化为点，特殊处理
    direction = line_end - line_start
    norm_val = float(np.linalg.norm(direction))

    if close(norm_val, 0):
        # 直线退化为点，此时只有当 p 恰好是 l_start (或 l_end) 时才算在上面
        return close(float(np.linalg.norm(point - line_start)), 0)
    
    # 计算参数 t
    t = get_parameter_t_on_line(point, line_start, line_end)
    return check_paramerized_line_range(t, line_type)