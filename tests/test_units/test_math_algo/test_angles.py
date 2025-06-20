import numpy as np
import pytest

from manimgeo.math import *

@pytest.mark.parametrize(
    "start, center, end, expected",
    [
        pytest.param([-1, -2, -3], [4, -2, 4], [3, -1, 5], 1.705433938408147, id="smoke"),
        pytest.param([4, 8, 11], [-3, -5, -6], [0, -1, 0], 0.098979197413858, id="smoke"),
        pytest.param([-114, -514, 114], [1919, 810, 893], [114, 514, 191], 0.39474593536022, id="smoke"),
        pytest.param([0, 0, 0], [0, 0, 0], [1, 0, 0], None, id="error_start_center_same"),
        pytest.param([1, 0, 0], [0, 0, 0], [0, 0, 0], None, id="error_center_end_same"),
        pytest.param([0, 0, 0], [1, 0, 0], [0, 0, 0], 0, id="error_start_end_same"),
        pytest.param([0, 0, 0], [0, 0, 0], [0, 0, 0], None, id="error_all_same"),
        pytest.param([0, 0, 0], [1, 0, 0], [2, 0, 0], np.pi, id="collinear_180_degrees"),
        pytest.param([2, 0, 0], [1, 0, 0], [0, 0, 0], np.pi, id="collinear_180_degrees_reversed"),
        pytest.param([5, 5, 5], [10, 10, 10], [15, 15, 15], np.pi, id="collinear_180_degrees_offset"),
        pytest.param([0, 1, 0], [0, 0, 0], [1, 0, 0], np.pi / 2, id="right_angle_90_degrees_xy"),
        pytest.param([0, 0, 1], [0, 0, 0], [1, 0, 0], np.pi / 2, id="right_angle_90_degrees_xz"),
        pytest.param([1, 1, 0], [1, 0, 0], [2, 0, 0], np.pi / 2, id="right_angle_90_degrees_offset"),
        pytest.param([1, 0, 0], [0, 0, 0], [0, -1, 0], np.pi / 2, id="right_angle_90_degrees"),
        pytest.param([1, 0, 0], [0, 0, 0], [-1, -1, 0], 3 * np.pi / 4, id="angle_135_degrees"),
        pytest.param([1, 1, 0], [0, 0, 0], [1, 0, 0], np.pi / 4, id="acute_angle_45_degrees"),
        pytest.param([1, 0.001, 0], [0, 0, 0], [1, 0, 0], np.arctan(0.001), id="small_acute_angle"),
        pytest.param([-1, 1, 0], [0, 0, 0], [1, 0, 0], 3 * np.pi / 4, id="obtuse_angle_135_degrees"),
        pytest.param([-1, 0.001, 0], [0, 0, 0], [1, 0, 0], np.pi - np.arctan(0.001), id="large_obtuse_angle"),
        pytest.param([0, 1e9, 0], [0, 0, 0], [1e9, 0, 0], np.pi / 2, id="large_coords_90_degrees"),
        pytest.param([0, 0, 0], [1e9, 0, 0], [2e9, 0, 0], np.pi, id="large_coords_180_degrees"),
        pytest.param([-1, -1, -1], [0, 0, 0], [1, 1, 1], np.pi, id="mixed_sign_coords_180"),
        pytest.param([1, -1, 0], [0, 0, 0], [-1, 1, 0], np.pi, id="mixed_sign_coords_180_diagonal"),
        pytest.param([1, 0, 0], [0, 0, 0], [0, 1, 0], np.pi / 2, id="mixed_sign_coords_90"),
        pytest.param([0, 1, 0], [0, 0, 0], [0, 1, 0], 0.0, id="same_y_axis_90_degrees"),
    ]
)
def test_angle_3p_countclockwise(start, center, end, expected):
    start = np.array(start, dtype=float)
    center = np.array(center, dtype=float)
    end = np.array(end, dtype=float)

    if isinstance(expected, float):
        result = angle_3p_countclockwise(start, center, end)
        assert close(result, expected), f"Expected {expected}, got {result}"
    elif expected is None:
        try:
            result = angle_3p_countclockwise(start, center, end)
            pytest.fail(f"Expected ValueError but no exception was raised. get {result}")
        except ValueError:
            pass