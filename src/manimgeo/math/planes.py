from .base import close, array2float, Number
from typing import Tuple, Optional
from logging import getLogger
import numpy as np

logger = getLogger(__name__)

@array2float
def plane_get_ABCD(point1: np.ndarray, point2: np.ndarray, point3: np.ndarray, constant: Optional[Number] = None) -> Tuple[float, float, float]:
    """
    根据平面上的三点计算平面的系数，满足方程：

    .. equation:: Ax + By + Cz = constant

    - `point1`, `point2`, `point3`: 三个平面上的点
    - `constant`: 平面方程的常数项，留空则根据是否经过原点设置为 1 或 0

    Returns: `Tuple[float, float, float]`, 表示 A、B、C
    """
    v1 = point2 - point1
    v2 = point3 - point1
    normal_vec = np.cross(v1, v2)
    A_prime, B_prime, C_prime = normal_vec
    
    # 如果法向量的模长接近于零，说明三点共线
    if close(float(np.linalg.norm(normal_vec)), 0):
        logger.warning(f"三个点可能共线或不定义唯一平面: {point1}, {point2}, {point3}")
        raise ValueError("三个点可能共线或不定义唯一平面")

    # 计算 D_prime (对于未缩放的法向量，Ax + By + Cz = D_prime)
    D_prime = A_prime * point1[0] + B_prime * point1[1] + C_prime * point1[2]

    if constant is None:
        # 如果没有提供常数项，则根据 D_prime 的值来决定
        constant = 0.0 if close(D_prime, 0) else D_prime
    else:
        constant = float(constant)

    # 平面通过原点
    if close(D_prime, 0):
        
        if close(constant, 0): # type: ignore
            # 为了返回一个规范的形式，将法向量归一化，使其最大绝对值分量为 1。
            max_abs_comp = np.max(np.abs(normal_vec))
            
            if close(max_abs_comp, 0):
                logger.warning(f"三个点可能共线或不定义唯一平面: {point1}, {point2}, {point3}")
                raise ValueError("三个点可能共线或不定义唯一平面")
            
            scale_factor = 1.0 / max_abs_comp
            A, B, C = normal_vec * scale_factor
            return float(A), float(B), float(C)

        else:
            logger.warning(f"三个点定义了一个通过原点的平面，但请求的常数不为零: {point1}, {point2}, {point3}, constant={constant}")
            raise ValueError("三个点定义了一个通过原点的平面，但请求的常数不为零")
    else:
        # 平面不通过原点 (D_prime != 0)
        # 计算缩放因子 k = constant / D_prime
        k = constant / D_prime
        return float(k * A_prime), float(k * B_prime), float(k * C_prime)