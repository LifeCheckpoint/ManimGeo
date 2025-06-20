import numpy as np
import pytest

from manimgeo.math import *

@pytest.mark.parametrize(
    "point, line_start, line_end, expected",
    [
        pytest.param([-5, 1, 0], [4, 0, 0], [0, 0, 4], [4, -1, 9], id="smoke"),
        pytest.param([0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], id="smoke"),
        pytest.param([1, 2, 3], [0, 0, 0], [1, 1, 1], [3, 2, 1], id="smoke"),
        pytest.param([2, -3, 5], [-1, -2, -3], [2, 3, 2], [28/59, 381/59, -209/59], id="smoke"),
        pytest.param([-1, 3, 2], [-6, -2, -3], [-1, 3, 2], [-1, 3, 2], id="edge_equal"),
        pytest.param([-11, -7, -8], [-6, -2, -3], [-1, 3, 2], [-11, -7, -8], id="equal"),
    ]
)
def test_axisymmetric_point(point, line_start, line_end, expected):
    point = np.array(point, dtype=float)
    L_start = np.array(line_start, dtype=float)
    L_end = np.array(line_end, dtype=float)
    expected = np.array(expected, dtype=float)

    result = axisymmetric_point(point, L_start, L_end)
    assert close(result, expected), f"Expected {expected}, got {result}"

@pytest.mark.parametrize(
    "point, center, r, expected",
    [
        pytest.param([1, 0, 0], [0, 0, 0], 1, [1, 0, 0], id="on_ball"),
        pytest.param([0, 1, 0], [0, 0, 0], 1, [0, 1, 0], id="on_ball"),
        pytest.param([0, 0, -1], [0, 0, 0], 1, [0, 0, -1], id="on_ball"),
        pytest.param([3, 4, 0], [0, 0, 0], 5, [3, 4, 0], id="on_ball"), # 3^2 + 4^2 = 5^2
        pytest.param([0.5, 0, 0], [0, 0, 0], 1, [2, 0, 0], id="in_ball"), # 0.5 -> 1^2/0.5 = 2
        pytest.param([0, 0.2, 0], [0, 0, 0], 1, [0, 5, 0], id="in_ball"), # 0.2 -> 1^2/0.2 = 5
        pytest.param([1, 0, 0], [0, 0, 0], 2, [4, 0, 0], id="in_ball"),   # 1 -> 2^2/1 = 4
        pytest.param([2, 0, 0], [0, 0, 0], 1, [0.5, 0, 0], id="out_ball"), # 2 -> 1^2/2 = 0.5
        pytest.param([0, 5, 0], [0, 0, 0], 1, [0, 0.2, 0], id="out_ball"), # 5 -> 1^2/5 = 0.2
        pytest.param([4, 0, 0], [0, 0, 0], 2, [1, 0, 0], id="out_ball"),   # 4 -> 2^2/4 = 1
        pytest.param([2, 2, 2], [1, 1, 1], 1, [4/3, 4/3, 4/3], id="on_ball_not_center"), # 距离 [1,1,1] 为 1
        pytest.param([1, 1, 3], [1, 1, 1], 2, [1, 1, 3], id="on_ball_not_center"), # 距离 [1,1,1] 为 2
        pytest.param([1.5, 1, 1], [1, 1, 1], 1, [3, 1, 1], id="in_ball_not_center"), # 距离 0.5 -> 1^2/0.5 = 2, 加上中心 [1,1,1] -> [3,1,1]
        pytest.param([1, 1, 1.5], [1, 1, 1], 2, [1, 1, 9], id="in_ball_not_center"), # Corrected expected value
        pytest.param([3, 1, 1], [1, 1, 1], 1, [1.5, 1, 1], id="out_ball_not_center"), # 距离 2 -> 1^2/2 = 0.5, 加上中心 [1,1,1] -> [1.5,1,1]
        pytest.param([1, 1, 9], [1, 1, 1], 2, [1, 1, 1.5], id="out_ball_not_center"), # 距离 8 -> 2^2/8 = 0.5, 加上中心 [1,1,1] -> [1,1,1.5]
        pytest.param([-0.5, 0, 0], [0, 0, 0], 1, [-2, 0, 0], id="negative"),
        pytest.param([-2, 0, 0], [0, 0, 0], 1, [-0.5, 0, 0], id="negative"),
        pytest.param([-1, -1, -1], [0, 0, 0], np.sqrt(3), [-1, -1, -1], id="negative"), # 在球面上
        pytest.param([0.5, 0, 0], [0, 0, 0], 0.5, [0.5, 0, 0], id="different_r"), # 点在球面上
        pytest.param([0.25, 0, 0], [0, 0, 0], 0.5, [1, 0, 0], id="different_r"),  # 点在球内 (0.25 -> 0.5^2/0.25 = 1)
        pytest.param([1, 0, 0], [0, 0, 0], 0.5, [0.25, 0, 0], id="different_r"),  # 点在球外 (1 -> 0.5^2/1 = 0.25)
        pytest.param([0, 0, 0], [0, 0, 0], 1, None, id="center_point"), # 点与圆心重合
    ]
)
def test_inversion_point(point, center, r, expected):
    point = np.array(point, dtype=float)
    center = np.array(center, dtype=float)
    if expected:
        expected = np.array(expected, dtype=float)
        result = inversion_point(point, center, r)
        assert close(result, expected), f"Expected {expected}, got {result}"
    else:
        try:
            result = inversion_point(point, center, r)
            pytest.fail(f"Expected ValueError but no exception was raised. get {result}")
        except ValueError:
            pass