from .base import close, array2float, Number
from typing import Tuple
from logging import getLogger
import numpy as np

logger = getLogger(__name__)

@array2float
def inverse_circle(
    origin_circle_center: np.ndarray, origin_circle_radius: Number, origin_circle_normal: np.ndarray,
    base_circle_center: np.ndarray, base_circle_r: Number, base_circle_normal: np.ndarray
) -> Tuple[np.ndarray, Number, np.ndarray]:
    """
    计算 origin_circle 关于 base_circle 的反演圆

    - `origin_circle_center`: 原圆圆心坐标
    - `origin_circle_radius`: 原圆半径
    - `origin_circle_normal`: 原圆法向量
    - `base_circle_center`: 基准圆圆心坐标
    - `base_circle_r`: 基准圆半径
    - `base_circle_normal`: 基准圆法向量

    Returns: `Tuple[np.ndarray, Number, np.ndarray]`, 反演圆圆心坐标、半径和法向量，法向量方向与原圆一致

    如果原圆包含基准圆圆心或原圆经过基准圆圆心，则抛出 `ValueError`
    """
    # 检查法向量是否共线
    cross_product = np.cross(origin_circle_normal, base_circle_normal)
    if not close(float(np.linalg.norm(cross_product)), 0):
        logger.warning(f"反演的原圆与基圆法向量不共线: {origin_circle_normal}, {base_circle_normal}")
        raise ValueError(f"反演的原圆与基圆法向量不共线: {origin_circle_normal}, {base_circle_normal}")
    
    # 确保法向量方向一致
    if np.dot(origin_circle_normal, base_circle_normal) < 0:
        base_circle_normal = -base_circle_normal
    
    # 计算圆心到基准圆心的向量
    center_diff = origin_circle_center - base_circle_center
    
    # 计算圆心到基准圆心的距离
    d = np.linalg.norm(center_diff)
    
    # 如果原圆经过基准圆圆心，反演后为直线
    if close(float(d), 0):
        logger.warning(f"原圆经过基准圆圆心，反演后为直线: {base_circle_center}")
        raise ValueError(f"原圆经过基准圆圆心，反演后为直线: {base_circle_center}")
    
    # 基准圆半径的平方
    R_squared = base_circle_r ** 2
    
    # 原圆上最近点和最远点到基准圆心的距离
    d_min = d - origin_circle_radius
    d_max = d + origin_circle_radius
    
    # 如果原圆包含基准圆圆心
    if d_min <= 0:
        raise ValueError("Origin circle contains the base circle center")
    
    # 反演后的最近点和最远点距离
    inv_d_min = R_squared / d_max
    inv_d_max = R_squared / d_min
    
    # 反演圆半径和圆心
    inv_radius = (inv_d_max - inv_d_min) / 2
    inv_center_distance = (inv_d_max + inv_d_min) / 2
    
    # 反演圆心坐标
    unit_direction = center_diff / d
    inv_center = base_circle_center + inv_center_distance * unit_direction
    
    return inv_center, float(inv_radius), origin_circle_normal

@array2float
def inverse_circle_to_line(
    origin_circle_center: np.ndarray, origin_circle_radius: Number, origin_circle_normal: np.ndarray,
    base_circle_center: np.ndarray, base_circle_r: Number, base_circle_normal: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    计算过基准圆圆心的原圆关于基准圆的反演直线

    - `origin_circle_center`: 原圆圆心坐标
    - `origin_circle_radius`: 原圆半径
    - `origin_circle_normal`: 原圆法向量
    - `base_circle_center`: 基准圆圆心坐标
    - `base_circle_r`: 基准圆半径
    - `base_circle_normal`: 基准圆法向量

    Returns: `Tuple[np.ndarray, np.ndarray]`, 反演直线上的两点

    如果原圆不经过基准圆圆心，则抛出 `ValueError`
    """
    # 检查法向量是否共线
    cross_product = np.cross(origin_circle_normal, base_circle_normal)
    if not close(float(np.linalg.norm(cross_product)), 0):
        logger.warning(f"反演的原圆与基圆法向量不共线: {origin_circle_normal}, {base_circle_normal}")
        raise ValueError(f"反演的原圆与基圆法向量不共线: {origin_circle_normal}, {base_circle_normal}")
    
    # 确保法向量方向一致
    if np.dot(origin_circle_normal, base_circle_normal) < 0:
        base_circle_normal = -base_circle_normal
    
    # 计算圆心到基准圆心的向量
    center_diff = origin_circle_center - base_circle_center
    
    # 计算圆心到基准圆心的距离
    d = np.linalg.norm(center_diff)
    
    # 检查原圆是否经过基准圆圆心
    if not close(float(d), float(origin_circle_radius)):
        logger.warning(f"原圆不经过基准圆圆心: 圆心距离 {d}, 原圆半径 {origin_circle_radius}")
        raise ValueError(f"原圆不经过基准圆圆心: 圆心距离 {d}, 原圆半径 {origin_circle_radius}")
    
    # 基准圆半径的平方
    R_squared = base_circle_r ** 2
    
    # 计算原圆上除基准圆心外的另一个特殊点（圆心的对径点）
    unit_direction = center_diff / d
    opposite_point = origin_circle_center + origin_circle_radius * unit_direction
    
    # 反演该点
    opposite_distance = np.linalg.norm(opposite_point - base_circle_center)
    inv_opposite_distance = R_squared / opposite_distance
    inv_opposite_point = base_circle_center + inv_opposite_distance * (opposite_point - base_circle_center) / opposite_distance
    
    # 反演直线垂直于连接基准圆心和原圆心的直线
    # 直线过反演点，方向垂直于unit_direction
    # 在原圆平面内找两个垂直于unit_direction的向量
    if len(origin_circle_normal) == 3:
        # 三维空间
        # 找一个与unit_direction和origin_circle_normal都垂直的向量
        perpendicular1 = np.cross(unit_direction, origin_circle_normal)
        perpendicular1 = perpendicular1 / np.linalg.norm(perpendicular1)
        
        # 找另一个垂直向量（在原圆平面内）
        perpendicular2 = np.cross(origin_circle_normal, perpendicular1)
        perpendicular2 = perpendicular2 / np.linalg.norm(perpendicular2)
    else:
        # 二维空间
        perpendicular1 = np.array([-unit_direction[1], unit_direction[0]])
        perpendicular2 = perpendicular1
    
    # 直线上的两点
    line_point1 = inv_opposite_point + perpendicular1
    line_point2 = inv_opposite_point - perpendicular1
    
    return line_point1, line_point2