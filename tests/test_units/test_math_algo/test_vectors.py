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

@pytest.mark.parametrize(
    "normal, expected_exc",
    [
        pytest.param(np.array([1, 0, 0]), None, id="Normal_X_Axis"),
        pytest.param(np.array([-1, 0, 0]), None, id="Normal_NegX_Axis"),
        pytest.param(np.array([0, 1, 0]), None, id="Normal_Y_Axis"),
        pytest.param(np.array([0, -1, 0]), None, id="Normal_NegY_Axis"),
        pytest.param(np.array([0, 0, 1]), None, id="Normal_Z_Axis"),
        pytest.param(np.array([0, 0, -1]), None, id="Normal_NegZ_Axis"),
        pytest.param(np.array([1, 1, 1]), None, id="Normal_Diagonal_Pos"),
        pytest.param(np.array([-1, -1, -1]), None, id="Normal_Diagonal_Neg"),
        pytest.param(np.array([1, -1, 1]), None, id="Normal_Diagonal_Mixed"),
        pytest.param(np.array([1, 1, 0]), None, id="Normal_XY_Plane"),
        pytest.param(np.array([1, 0, 1]), None, id="Normal_XZ_Plane"),
        pytest.param(np.array([0, 1, 1]), None, id="Normal_YZ_Plane"),
        pytest.param(np.array([1, 2, 3]), None, id="Normal_Arbitrary_Pos"),
        pytest.param(np.array([-3, 2, -1]), None, id="Normal_Arbitrary_Mixed"),
        pytest.param(np.array([100, 0, 0]), None, id="Normal_LargeMagnitude_X"),
        pytest.param(np.array([0.001, 0.001, 0.001]), None, id="Normal_SmallMagnitude_Diagonal"),
        pytest.param(np.array([1e5, 2e5, 3e5]), None, id="Normal_VeryLargeMagnitude"),
        pytest.param(np.array([1e-5, 2e-5, 3e-5]), None, id="Normal_VerySmallMagnitude"),
        pytest.param(np.array([0, 0, 0]), ValueError, id="Normal_ZeroVector"),
    ]
)
def test_get_two_vector_from_normal(normal, expected_exc):
    """
    Tests the properties of the two orthogonal vectors generated from a normal.
    """
    if expected_exc is None:
        v1, v2 = get_two_vector_from_normal(normal)
        # 1. Check if v1 and v2 are numpy arrays of correct shape
        assert isinstance(v1, np.ndarray) and v1.shape == (3,), f"v1 is not a 3D numpy array"
        assert isinstance(v2, np.ndarray) and v2.shape == (3,), f"v2 is not a 3D numpy array"
        # Calculate unit normal for comparison
        unit_normal = normal / np.linalg.norm(normal)
        # 2. Check Orthogonality
        # v1 should be orthogonal to normal
        assert close(np.dot(v1, unit_normal), 0), f"v1 not orthogonal to normal. Dot product: {np.dot(v1, unit_normal)}"
        # v2 should be orthogonal to normal
        assert close(np.dot(v2, unit_normal), 0), f"v2 not orthogonal to normal. Dot product: {np.dot(v2, unit_normal)}"
        # v1 should be orthogonal to v2
        assert close(np.dot(v1, v2), 0), f"v1 not orthogonal to v2. Dot product: {np.dot(v1, v2)}"
        # 3. Check Unit Length
        assert close(float(np.linalg.norm(v1)), 1), f"v1 is not a unit vector. Norm: {np.linalg.norm(v1)}"
        assert close(float(np.linalg.norm(v2)), 1), f"v2 is not a unit vector. Norm: {np.linalg.norm(v2)}"
        # 4. Check Right-Handed System (v1, v2, normal)
        # cross(v1, v2) should be equal to unit_normal
        assert close(np.cross(v1, v2), unit_normal), f"(v1, v2, normal) do not form a right-handed system: {v1}, {v2}, {unit_normal}"
    else:
        with pytest.raises(expected_exc):
            get_two_vector_from_normal(normal)