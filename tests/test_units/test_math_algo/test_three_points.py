import numpy as np
import pytest

from manimgeo.math import *

@pytest.mark.parametrize(
    "p1, p2, p3, expected_r, expected_c, expected_exc",
    [
        pytest.param(
            [3, 4, 5], [-2, -3, -4], [1, 1, 3],
            0.6076209623726777, [1.19206634, 1.36998733, 2.53696382],
            None, id="smoke"
        ),
        pytest.param(
            [114, 514, 1919], [810, -893, -1145], [141, -981, 894],
            453.1170104859469, [296.98470303, -525.74055997, 692.07169173],
            None, id="smoke"
        ),
        pytest.param(
            [0, 0, 0], [0, 0, 0], [0, 0, 0],
            0.0, [0, 0, 0],
            None, id="degenerate_all_identical_origin"
        ),
        pytest.param(
            [10, -5, 20], [10, -5, 20], [10, -5, 20],
            0.0, [10, -5, 20],
            None, id="degenerate_all_identical_non_origin"
        ),
        pytest.param(
            [1, 0, 0], [1, 0, 0], [0, 0, 0],
            0.0, [2/3, 0, 0], # (2*p1 + p3)/3
            None, id="degenerate_two_identical"
        ),
        pytest.param(
            [5, 5, 5], [10, 10, 10], [10, 10, 10],
            0.0, [25/3, 25/3, 25/3], # (p1 + 2*p2)/3
            None, id="degenerate_two_identical_order_changed"
        ),
        pytest.param(
            [0, 0, 0], [1, 0, 0], [2, 0, 0],
            0.0, [1, 0, 0], # (0+1+2)/3 = 1
            None, id="degenerate_collinear_x_axis"
        ),
        pytest.param(
            [1, 1, 1], [2, 2, 2], [3, 3, 3],
            0.0, [2, 2, 2],
            None, id="degenerate_collinear_diagonal"
        ),
        pytest.param(
            [0, 0, 0], [0, 1, 0], [0, 2, 0],
            0.0, [0, 1, 0],
            None, id="degenerate_collinear_y_axis"
        ),
        pytest.param(
            [0, 0, 0], [0, 0, 1], [0, 0, 2],
            0.0, [0, 0, 1],
            None, id="degenerate_collinear_z_axis"
        ),
        pytest.param(
            [0, 0, 0], [1, 0, 0], [0.5, np.sqrt(3)/2, 0],
            np.sqrt(3)/6, [0.5, np.sqrt(3)/6, 0],
            None, id="equilateral_2d_xy"
        ),
        pytest.param(
            [1, 0, 0], [0, 1, 0], [0, 0, 1],
            1/np.sqrt(6), [1/3, 1/3, 1/3],
            None, id="equilateral_3d"
        ),
        pytest.param(
            [0, 0, 0], [3, 0, 0], [0, 4, 0],
            1.0, [1, 1, 0], # r = (3+4-5)/2 = 1; c = (5*p1 + 4*p2 + 3*p3)/12 = (0 + [12,0,0] + [0,12,0])/12 = [1,1,0]
            None, id="right_angled_3_4_5"
        ),
        pytest.param(
            [0, 0, 0], [5, 0, 0], [0, 12, 0],
            2.0, [2, 2, 0], # r = (5+12-13)/2 = 2; c = (13*p1 + 12*p2 + 5*p3)/30 = (0 + [60,0,0] + [0,60,0])/30 = [2,2,0]
            None, id="right_angled_5_12_13"
        ),
        pytest.param(
            [0, 0, 0], [1e-7, 0, 0], [0, 1e-7, 0],
            1e-7 * (2 - np.sqrt(2)) / 2, # r = (a+b-c)/2 for right triangle
            [1e-7 * (2 - np.sqrt(2)) / 2, 1e-7 * (2 - np.sqrt(2)) / 2, 0],
            None, id="very_small_triangle"
        ),
        pytest.param(
            [0, 0, 0], [1e6, 0, 0], [0, 1e6, 0],
            1e6 * (2 - np.sqrt(2)) / 2,
            [1e6 * (2 - np.sqrt(2)) / 2, 1e6 * (2 - np.sqrt(2)) / 2, 0],
            None, id="very_large_triangle"
        ),
    ]
)
def test_inscribed_r_c(p1, p2, p3, expected_r, expected_c, expected_exc):
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    p3 = np.array(p3, dtype=float)
    expected_r = float(expected_r)
    expected_c = np.array(expected_c, dtype=float)

    if not expected_exc:
        r, c = inscribed(p1, p2, p3)
        assert close(r, expected_r), f"Expected {expected_r}, got {r} for inputs {p1}, {p2}, {p3}" # type: ignore
        assert close(c, expected_c), f"Expected {expected_c}, got {c} for inputs {p1}, {p2}, {p3}" # type: ignore

@pytest.mark.parametrize(
    "p1, p2, p3, expected_r, expected_c, expected_exc",
    [
        pytest.param(
            [0, 0, 0], [3, 0, 0], [0, 4, 0],
            2.5, [1.5, 2, 0],
            None, id="smoke_right_angled_3_4_5"
        ),
        pytest.param(
            [0, 0, 0], [1, 0, 0], [0.5, np.sqrt(3)/2, 0],
            1/np.sqrt(3), [0.5, np.sqrt(3)/6, 0],
            None, id="smoke_equilateral_2d"
        ),
        pytest.param(
            [0, 0, 0], [1, 0, 0], [2, 0, 0],
            None, None, ValueError, id="degenerate_collinear_x_axis"
        ),
        pytest.param(
            [1, 1, 1], [2, 2, 2], [3, 3, 3],
            None, None, ValueError, id="degenerate_collinear_diagonal"
        ),
        pytest.param(
            [0, 0, 0], [0, 1, 0], [0, 2, 0],
            None, None, ValueError, id="degenerate_collinear_y_axis"
        ),
        pytest.param(
            [1, 0, 0], [1, 0, 0], [0, 0, 0],
            None, None, ValueError, id="degenerate_two_identical"
        ),
        pytest.param(
            [5, 5, 5], [10, 10, 10], [10, 10, 10],
            None, None, ValueError, id="degenerate_two_identical_order_changed"
        ),
        pytest.param(
            [0, 0, 0], [0, 0, 0], [0, 0, 0],
            None, None, ValueError, id="degenerate_all_identical_origin"
        ),
        pytest.param(
            [10, -5, 20], [10, -5, 20], [10, -5, 20],
            None, None, ValueError, id="degenerate_all_identical_non_origin"
        ),
        pytest.param(
            [1, 0, 0], [0, 1, 0], [0, 0, 1],
            np.sqrt(6)/3, [1/3, 1/3, 1/3], # R = a / np.sqrt(3) where a = np.sqrt(2)
            None, id="equilateral_3d"
        ),
        pytest.param(
            [1, 1, 1], [1, 4, 1], [5, 1, 1], # Right angle at [1,1,1]
            2.5, [3, 2.5, 1], # Hypotenuse from [1,4,1] to [5,1,1] is length 5. Midpoint is (1+5)/2, (4+1)/2, (1+1)/2
            None, id="right_angled_3d_shifted"
        ),
        pytest.param(
            [0, 0, 0], [3, 0, 0], [0, 0, 4], # Right angle at origin, in XZ plane
            2.5, [1.5, 0, 2],
            None, id="right_angled_3_4_5_xz_plane"
        ),
        pytest.param(
            [0, 0, 0], [5, 0, 0], [2.5, 4, 0],
            2.78125, [2.5, 1.21875, 0], # R = a*b*c / (4*Area), C = (2.5, (y_v^2 - (base/2)^2) / (2*y_v), 0)
            None, id="isosceles_non_equilateral_non_right"
        ),
        pytest.param(
            [0, 0, 0], [1e-7, 0, 0], [0, 1e-7, 0],
            np.sqrt(2) * 1e-7 / 2, [0.5e-7, 0.5e-7, 0],
            None, id="very_small_triangle"
        ),
        pytest.param(
            [0, 0, 0], [1e6, 0, 0], [0, 1e6, 0],
            np.sqrt(2) * 1e6 / 2, [0.5e6, 0.5e6, 0],
            None, id="very_large_triangle"
        ),
        pytest.param(
            [-1, -1, -1], [-4, -1, -1], [-1, -4, -1], # Right angle at [-1,-1,-1]
            2.121320343559642, [-2.5, -2.5, -1],
            None, id="negative_coordinates_right_angled"
        ),
        pytest.param(
            [10, 20, 30], [5, 15, 25], [12, 8, 18],
            9.06228448019593, [14, 14.25, 24.25],
            None, id="general_triangle_3d"
        ),
    ]
)
def test_circumcenter_r_c(p1, p2, p3, expected_r, expected_c, expected_exc):
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    p3 = np.array(p3, dtype=float)
    expected_r = float(expected_r) if expected_r is not None else None
    expected_c = np.array(expected_c, dtype=float) if expected_c is not None else None

    if not expected_exc:
        r, c = circumcenter(p1, p2, p3)
        assert close(r, expected_r), f"Expected {expected_r}, got {r} for inputs {p1}, {p2}, {p3}" # type: ignore
        assert close(c, expected_c), f"Expected {expected_c}, got {c} for inputs {p1}, {p2}, {p3}" # type: ignore
    else:
        with pytest.raises(expected_exc):
            circumcenter(p1, p2, p3)


@pytest.mark.parametrize(
    "p1, p2, p3, expected_c, expected_exc",
    [
        pytest.param(
            [0, 0, 0], [4, 0, 0], [2, 3, 0],
            [2, 4/3, 0], # Calculated: x=2, y=4/3
            None, id="smoke_acute_triangle"
        ),
        pytest.param(
            [0, 0, 0], [1, 0, 0], [0.1, 0.5, 0], # Angle at p1 is obtuse
            [0.1, 0.18, 0], # Calculated: x=0.1, y=0.18
            None, id="smoke_obtuse_triangle"
        ),
        pytest.param(
            [0, 0, 0], [1, 0, 0], [2, 0, 0],
            None, ValueError, id="degenerate_collinear_x_axis"
        ),
        pytest.param(
            [1, 1, 1], [2, 2, 2], [3, 3, 3],
            None, ValueError, id="degenerate_collinear_diagonal"
        ),
        pytest.param(
            [0, 0, 0], [0, 1, 0], [0, 2, 0],
            None, ValueError, id="degenerate_collinear_y_axis"
        ),
        pytest.param(
            [1, 0, 0], [1, 0, 0], [0, 0, 0],
            None, ValueError, id="degenerate_two_identical"
        ),
        pytest.param(
            [5, 5, 5], [10, 10, 10], [10, 10, 10],
            None, ValueError, id="degenerate_two_identical_order_changed"
        ),
        pytest.param(
            [0, 0, 0], [0, 0, 0], [0, 0, 0],
            None, ValueError, id="degenerate_all_identical_origin"
        ),
        pytest.param(
            [10, -5, 20], [10, -5, 20], [10, -5, 20],
            None, ValueError, id="degenerate_all_identical_non_origin"
        ),
        pytest.param(
            [0, 0, 0], [3, 0, 0], [0, 4, 0], # Right angle at p1
            [0, 0, 0],
            None, id="right_angled_3_4_5_at_origin"
        ),
        pytest.param(
            [1, 1, 1], [1, 4, 1], [5, 1, 1], # Right angle at p1
            [1, 1, 1],
            None, id="right_angled_3d_shifted"
        ),
        pytest.param(
            [0, 0, 0], [5, 0, 0], [0, 12, 0], # Right angle at p1
            [0, 0, 0],
            None, id="right_angled_5_12_13_at_origin"
        ),
        pytest.param(
            [0, 0, 0], [1, 0, 0], [0.5, np.sqrt(3)/2, 0],
            [0.5, np.sqrt(3)/6, 0], # Centroid of equilateral triangle
            None, id="equilateral_2d_xy"
        ),
        pytest.param(
            [1, 0, 0], [0, 1, 0], [0, 0, 1],
            [1/3, 1/3, 1/3], # Centroid of equilateral triangle
            None, id="equilateral_3d"
        ),
        pytest.param(
            [0, 0, 0], [5, 0, 0], [2.5, 4, 0],
            [2.5, 1.5625, 0], # Calculated: x=2.5, y=1.5625
            None, id="isosceles_non_equilateral_non_right"
        ),
        pytest.param(
            [0, 0, 0], [1e6, 0, 0], [0, 1e6, 0], # Right angle at origin
            [0, 0, 0],
            None, id="very_large_triangle"
        ),
        pytest.param(
            [-1, -1, -1], [-4, -1, -1], [-1, -4, -1], # Right angle at [-1,-1,-1]
            [-1, -1, -1],
            None, id="negative_coordinates_right_angled"
        ),
    ]
)
def test_orthocenter_r_c(p1, p2, p3, expected_c, expected_exc):
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    p3 = np.array(p3, dtype=float)
    expected_c = np.array(expected_c, dtype=float) if expected_c is not None else None

    if not expected_exc:
        c = orthocenter(p1, p2, p3)
        assert close(c, expected_c), f"Expected {expected_c}, got {c} for inputs {p1}, {p2}, {p3}" # type: ignore
    else:
        with pytest.raises(expected_exc):
            orthocenter(p1, p2, p3)