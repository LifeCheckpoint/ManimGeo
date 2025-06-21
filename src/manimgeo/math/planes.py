from .base import close, array2float, Number
from typing import Tuple
from logging import getLogger
import numpy as np

logger = getLogger(__name__)

@array2float
def plane_get_ABCD(point1: np.ndarray, point2: np.ndarray, point3: np.ndarray, constant: Number = 1) -> Tuple[float, float, float]:
    """
    根据平面上的三点计算平面的系数，满足方程：

    .. equation:: Ax + By + Cz = constant

    Returns: `Tuple[float, float, float]`, 表示 A、B、C
    """
    # 构建线性方程组矩阵
    # 每个点 (x, y, z) 对应方程 Ax + By + Cz = constant
    matrix = np.array([
        [point1[0], point1[1], point1[2]],
        [point2[0], point2[1], point2[2]],
        [point3[0], point3[1], point3[2]]
    ])

    # 右侧常数向量都是 constant
    constants = np.array([constant, constant, constant])

    # 求解线性方程组得到 A, B, C
    try:
        A, B, C = np.linalg.solve(matrix, constants)
        return A, B, C
    except np.linalg.LinAlgError:
        logger.warning(f"三个点可能共线或不定义唯一平面: {point1}, {point2}, {point3}")
        raise ValueError("三个点可能共线或不定义唯一平面")