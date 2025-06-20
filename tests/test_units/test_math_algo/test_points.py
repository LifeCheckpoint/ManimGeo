import numpy as np
import pytest

from manimgeo.math import *

@pytest.mark.parametrize(
    "point, line_start, line_end, expected",
    [
        ([-5, 1, 0], [4, 0, 0], [0, 0, 4], [4, -1, 9]),
        ([0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]),
        ([1, 2, 3], [0, 0, 0], [1, 1, 1], [3, 2, 1]),
        ([2, -3, 5], [-1, -2, -3], [2, 3, 2], [28/59, 381/59, -209/59]),
        ([-1, 3, 2], [-6, -2, -3], [-1, 3, 2], [-1, 3, 2]),
        ([-11, -7, -8], [-6, -2, -3], [-1, 3, 2], [-11, -7, -8]),
    ]
)
def test_axisymmetric_point(point, line_start, line_end, expected):
    point = np.array(point, dtype=float)
    L_start = np.array(line_start, dtype=float)
    L_end = np.array(line_end, dtype=float)
    expected = np.array(expected, dtype=float)

    result = axisymmetric_point(point, L_start, L_end)
    assert close(result, expected), f"Expected {expected}, got {result}"