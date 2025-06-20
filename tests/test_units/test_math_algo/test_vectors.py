import numpy as np
import pytest

from manimgeo.math import *

@pytest.mark.parametrize(
    "start, end, expected_vec, expected_exc",
    [
        pytest.param(
            [0, 0], [1, 0],
            [1, 0],
            None, id="2d_positive_x_axis"
        ),
        pytest.param(
            [0, 0], [0, 1],
            [0, 1],
            None, id="2d_positive_y_axis"
        ),
        pytest.param(
            [0, 0], [1, 1],
            [1/np.sqrt(2), 1/np.sqrt(2)],
            None, id="2d_diagonal"
        ),
        pytest.param(
            [1, 1], [2, 2], # Shifted diagonal
            [1/np.sqrt(2), 1/np.sqrt(2)],
            None, id="2d_diagonal_shifted"
        ),
        pytest.param(
            [0, 0, 0], [1, 0, 0],
            [1, 0, 0],
            None, id="3d_positive_x_axis"
        ),
        pytest.param(
            [0, 0, 0], [1, 1, 1],
            [1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)],
            None, id="3d_main_diagonal"
        ),
        pytest.param(
            [1, 2, 3], [4, 5, 6], # Arbitrary 3D points
            [1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)], # (3,3,3) normalized
            None, id="3d_arbitrary_points"
        ),
        pytest.param(
            [0, 0], [-1, 0], # Negative direction
            [-1, 0],
            None, id="2d_negative_x_axis"
        ),
        pytest.param(
            [1, 1, 1], [0, 0, 0], # Reverse direction
            [-1/np.sqrt(3), -1/np.sqrt(3), -1/np.sqrt(3)],
            None, id="3d_reverse_direction"
        ),
        # --- Edge Cases: Degenerate (should raise ValueError) ---
        pytest.param(
            [0, 0, 0], [0, 0, 0],
            None, ValueError, id="degenerate_identical_origin"
        ),
        pytest.param(
            [10, -5, 20], [10, -5, 20],
            None, ValueError, id="degenerate_identical_non_origin"
        ),
        pytest.param(
            [0, 0, 0], [1e-10, 0, 0], # Very close points (assuming close tolerance is around 1e-9)
            None, ValueError, id="degenerate_very_close_x_axis"
        ),
        pytest.param(
            [1, 1, 1], [1 + 1e-10, 1, 1],
            None, ValueError, id="degenerate_very_close_shifted"
        ),
        # --- Numerical Stability ---
        pytest.param(
            [0, 0, 0], [1e6, 0, 0], # Large coordinates
            [1, 0, 0],
            None, id="numerical_large_coordinates"
        ),
        pytest.param(
            [0, 0, 0], [1e-5, 0, 0], # Small but non-zero difference
            [1, 0, 0],
            None, id="numerical_small_coordinates"
        ),
        pytest.param(
            [-100, -200, -300], [-100, -200, -299], # Negative and mixed coordinates
            [0, 0, 1],
            None, id="numerical_negative_mixed_coordinates"
        ),
    ]
)
def test_unit_direction_vector(start, end, expected_vec, expected_exc):
    start_arr = np.array(start, dtype=float)
    end_arr = np.array(end, dtype=float)
    
    if expected_exc is None:
        expected_vec_arr = np.array(expected_vec, dtype=float)
        result_vec = unit_direction_vector(start_arr, end_arr)
        
        # Check if the result is a unit vector (magnitude close to 1)
        assert close(float(np.linalg.norm(result_vec)), 1.0), \
            f"Result vector {result_vec} does not have unit magnitude for inputs {start_arr}, {end_arr}"
        
        # Check if the direction is correct
        assert close(result_vec, expected_vec_arr), \
            f"Expected {expected_vec_arr}, got {result_vec} for inputs {start_arr}, {end_arr}"
    else:
        with pytest.raises(expected_exc):
            unit_direction_vector(start_arr, end_arr)