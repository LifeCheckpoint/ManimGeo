from .base import close, array2float
from logging import getLogger
from typing import Tuple
import numpy as np

logger = getLogger(__name__)

@array2float
def unit_direction_vector(start: np.ndarray, end: np.ndarray) -> np.ndarray:
    """
    计算单位方向向量
    
    Returns: `np.ndarray`, 单位方向向量
    """
    start_float = start.astype(float)
    end_float = end.astype(float)

    direction_vector = end_float - start_float
    norm = np.linalg.norm(direction_vector)
    if close(float(norm), 0):
        logger.warning("start 与 end 过于接近或差为 0")
        raise ValueError("start 与 end 过于接近或差为 0")
    
    return direction_vector / norm

@array2float
def get_two_vector_from_normal(normal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    从法向量生成两个正交向量，三个向量互相正交且生成向量长度为 1

    向量选取的方向将尽可能保证数值稳定，v1, v2, normal 构成右手系
    """
    norm_val = np.linalg.norm(normal)
    if norm_val == 0:
        logger.warning("法向量不能是零向量")
        raise ValueError("法向量不能是零向量")
    
    # 确保法向量是单位向量
    unit_normal = normal / norm_val
        
    # 选择一个健壮的参考向量
    # 选择参考向量的标准，与法向量的分量比较，选择最小的分量对应的轴
    abs_n = np.abs(unit_normal)
    if abs_n[0] <= abs_n[1] and abs_n[0] <= abs_n[2]:
        reference = np.array([1.0, 0.0, 0.0])
    elif abs_n[1] <= abs_n[0] and abs_n[1] <= abs_n[2]:
        reference = np.array([0.0, 1.0, 0.0])
    else:
        reference = np.array([0.0, 0.0, 1.0])
        
    # 生成第一个正交向量
    v1 = np.cross(reference, unit_normal)
    v1 = v1 / np.linalg.norm(v1)
        
    # 生成第二个正交向量
    v2 = np.cross(unit_normal, v1)
    v2 = v2 / np.linalg.norm(v2)
        
    return v1, v2