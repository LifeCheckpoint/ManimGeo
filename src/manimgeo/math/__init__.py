"""
math 模块实现了具体几何计算相关的函数
"""

from .angles import (
    angle_3p_countclockwise,
)

from .base import (
    close,
    array2float,
)

from .circles import (
    inverse_circle,
    inverse_circle_to_line,
)

from .intersections import (
    intersection_line_line,
)

from .lines import (
    check_paramerized_line_range,
    vertical_point_to_line,
    vertical_line_unit_direction,
    point_to_line_distance,
    get_parameter_t_on_line,
    is_point_on_line,
)

from .planes import (
    plane_get_ABCD,
)

from .points import (
    axisymmetric_point,
    inversion_point,
)

from .three_points import (
    inscribed, 
    circumcenter, 
    orthocenter,
)

from .vectors import (
    unit_direction_vector,
    get_two_vector_from_normal,
)