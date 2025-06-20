from .base import close, array2float, Number
from logging import getLogger
import numpy as np

logger = getLogger(__name__)

@array2float
def axisymmetric_point(point: np.ndarray, line_start: np.ndarray, line_end: np.ndarray) -> np.ndarray:
    """
    计算点 point 关于线 (line_start, line_end) 的对称点

    - `p`: 要计算对称点的原始点
    - `l_start`: 直线起点
    - `l_end`: 直线终点

    Returns: `np.ndarray`, 对称点坐标。
    """
    from .vectors import unit_direction_vector
    u = unit_direction_vector(line_start, line_end)
    
    # 直线基点
    base = line_start
    vector_base_to_p = point - base
    projection_length = np.dot(vector_base_to_p, u)
    q = base + projection_length * u
    
    # 检查原始点 point 是否已在直线上
    # 如果 p 已经在直线上，则其对称点就是它本身
    if close(float(np.linalg.norm(point - q)), 0):
        return point.copy()
    
    # p' = 2q - p
    symmetric_point = 2 * q - point
    return symmetric_point

@array2float
def inversion_point(point: np.ndarray, center: np.ndarray, r: Number) -> np.ndarray:
    """
    计算反演点
    
    - `p`: 要计算反演点的原始点
    - `center`: 圆心
    - `r`: 圆的半径
    """
    op = point - center
    d_squared = np.dot(op, op)
    
    if close(d_squared, 0):
        logger.warning("point 与 center 过于接近，无法计算反演")
        raise ValueError("point 与 center 过于接近，无法计算反演")
        
    k = (r ** 2) / d_squared
    return center + op * k