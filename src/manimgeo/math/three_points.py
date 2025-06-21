from .base import close, array2float
from logging import getLogger
from typing import Tuple
import numpy as np

logger = getLogger(__name__)

@array2float
def inscribed(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> Tuple[float, np.ndarray]:
    """
    计算三维空间中三点构成的三角形的内切圆半径和内切圆圆心，内切圆和圆心位于这三点定义的平面内

    - Returns: `Tuple[float, np.ndarray]`, 内切圆半径和内切圆圆心坐标
    """
    a_len = np.linalg.norm(p2 - p3)
    b_len = np.linalg.norm(p3 - p1)
    c_len = np.linalg.norm(p1 - p2)

    # 三点重合退化
    perimeter = float(a_len + b_len + c_len)
    if close(perimeter, 0):
        logger.warning("三点退化为一点，无法形成有效三角形：{}, {}, {}".format(p1, p2, p3))
        return 0.0, (p1 + p2 + p3) / 3.0

    # 半周长
    s = perimeter / 2.0

    # 海伦公式
    area_squared_term = float(s * (s - a_len) * (s - b_len) * (s - c_len))

    if close(area_squared_term, 0):
        logger.warning("三点共线退化，无法形成有效三角形：{}, {}, {}".format(p1, p2, p3))
        return 0.0, (p1 + p2 + p3) / 3.0

    r = np.sqrt(area_squared_term) / s
    incenter = (a_len * p1 + b_len * p2 + c_len * p3) / perimeter
    
    return r, incenter

@array2float
def circumcenter(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> Tuple[float, np.ndarray]:
    """
    计算三维空间中三点构成的三角形的外接圆半径和外接圆圆心，外接圆和圆心位于这三点定义的平面内

    Returns: `Tuple[float, np.ndarray]`, 外接圆半径和外接圆圆心坐标。
    """
    v1 = p2 - p1
    v2 = p3 - p1

    dot_v1_v1 = np.dot(v1, v1) # |v1|^2
    dot_v1_v2 = np.dot(v1, v2) # v1.v2
    dot_v2_v2 = np.dot(v2, v2) # |v2|^2

    # 构建 2x2 矩阵 A 和右侧向量 B
    A = np.array([
        [2 * dot_v1_v1, 2 * dot_v1_v2],
        [2 * dot_v1_v2, 2 * dot_v2_v2]
    ])
    B = np.array([dot_v1_v1, dot_v2_v2])

    # 求解线性方程组 Ax = B 得到 x, y
    # np.linalg.solve 会检查 A 是否奇异，如果奇异会抛出 LinAlgError
    try:
        coeffs = np.linalg.solve(A, B)
    except np.linalg.LinAlgError:
        logger.warning("三点共线退化，无法计算外接圆：{}, {}, {}".format(p1, p2, p3))
        raise ValueError("三点共线，无法计算外接圆")

    x, y = coeffs[0], coeffs[1]

    # 计算圆心坐标
    circumcenter = p1 + x * v1 + y * v2

    # 计算半径：圆心到任意一个顶点的距离
    r = float(np.linalg.norm(circumcenter - p1))
    
    return r, circumcenter

@array2float
def orthocenter(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> np.ndarray:
    """
    计算三维空间中三点构成的三角形的垂心坐标，垂心位于这三点定义的平面内

    Returns: `np.ndarray`, 垂心坐标。
    """
    v1 = p2 - p1
    v2 = p3 - p1
    v_p2p3 = p3 - p2

    area_vec = np.cross(v1, v2)
    if np.linalg.norm(area_vec) < 1e-9: # Use a small tolerance for floating point comparison
        logger.warning("三点共线退化，无法计算垂心：{}, {}, {}".format(p1, p2, p3))
        raise ValueError("三点共线，无法计算垂心")

    dot_v1_v_p2p3 = np.dot(v1, v_p2p3)
    dot_v2_v_p2p3 = np.dot(v2, v_p2p3)
    dot_v1_v2 = np.dot(v1, v2)
    dot_v2_v2 = np.dot(v2, v2) # |v2|^2
    A = np.array([
        [dot_v1_v_p2p3, dot_v2_v_p2p3],
        [dot_v1_v2, dot_v2_v2]
    ])
    B = np.array([0, dot_v1_v2]) # Right-hand side of the 2x2 system

    try:
        coeffs = np.linalg.solve(A, B)
    except np.linalg.LinAlgError:
        logger.warning("无法求解垂心方程组，可能存在数值问题：{}, {}, {}".format(p1, p2, p3))
        raise ValueError("无法求解垂心方程组，可能存在数值问题")

    x, y = coeffs[0], coeffs[1]
    orthocenter = p1 + x * v1 + y * v2
    return orthocenter
