from .base import close, array2float
from logging import getLogger
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