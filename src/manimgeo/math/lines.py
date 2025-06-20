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