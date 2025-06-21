import pytest
import numpy as np
from manimgeo.math import *

@pytest.mark.parametrize(
    "t, line_type, expected_result, expected_exc",
    [
        pytest.param(0.5, "LineSegment", True, None, id="LineSegment_t_in_range"),
        pytest.param(0.0, "LineSegment", True, None, id="LineSegment_t_at_0_exact"), # Covered by close(t,0)
        pytest.param(1.0, "LineSegment", True, None, id="LineSegment_t_at_1_exact"), # Covered by close(t,1)
        pytest.param(1e-10, "LineSegment", True, None, id="LineSegment_t_close_to_0"), # Covered by close(t,0)
        pytest.param(1 - 1e-10, "LineSegment", True, None, id="LineSegment_t_close_to_1"), # Covered by close(t,1)
        pytest.param(-0.1, "LineSegment", False, None, id="LineSegment_t_out_of_range_negative"),
        pytest.param(1.1, "LineSegment", False, None, id="LineSegment_t_out_of_range_positive"),
        pytest.param(0.001, "LineSegment", True, None, id="LineSegment_t_just_inside_0"),
        pytest.param(0.999, "LineSegment", True, None, id="LineSegment_t_just_inside_1"),
        pytest.param(2.0, "LineSegment", False, None, id="LineSegment_t_far_out_of_range"),
        pytest.param(0.5, "Ray", True, None, id="Ray_t_in_range"),
        pytest.param(5.0, "Ray", True, None, id="Ray_t_positive_large"),
        pytest.param(0.0, "Ray", True, None, id="Ray_t_at_0_exact"), # Covered by close(t,0)
        pytest.param(1e-10, "Ray", True, None, id="Ray_t_close_to_0"), # Covered by close(t,0)
        pytest.param(-0.1, "Ray", False, None, id="Ray_t_negative"),
        pytest.param(-1e-10, "Ray", True, None, id="Ray_t_negative_close_to_0"),
        pytest.param(0.5, "InfinityLine", True, None, id="InfinityLine_t_positive"),
        pytest.param(-1.0, "InfinityLine", True, None, id="InfinityLine_t_negative"),
        pytest.param(100.0, "InfinityLine", True, None, id="InfinityLine_t_large"),
        pytest.param(0.0, "InfinityLine", True, None, id="InfinityLine_t_at_0_exact"), # Covered by close(t,0)
        pytest.param(1.0, "InfinityLine", True, None, id="InfinityLine_t_at_1_exact"), # Covered by close(t,1)
        pytest.param(1e-10, "InfinityLine", True, None, id="InfinityLine_t_close_to_0"), # Covered by close(t,0)
        pytest.param(0.5, "InvalidType", None, ValueError, id="Invalid_line_type"),
        pytest.param(0.5, "Line", None, ValueError, id="Invalid_line_type_similar_name"),
        pytest.param(0.5, "", None, ValueError, id="Invalid_line_type_empty_string"),
    ]
)
def test_check_paramerized_line_range(t, line_type, expected_result, expected_exc):
    if expected_exc is None:
        result = check_paramerized_line_range(t, line_type)
        assert result == expected_result, \
            f"For t={t}, line_type='{line_type}', expected {expected_result}, but got {result}"
    else:
        with pytest.raises(expected_exc):
            check_paramerized_line_range(t, line_type)

@pytest.mark.parametrize(
    "line_start, line_end, turn, expected_vec, expected_exc",
    [
        pytest.param(
            [0, 0], [1, 0], "counterclockwise",
            [0, 1],
            None, id="2D_CCW_X_axis"
        ),
        pytest.param(
            [0, 0], [0, 1], "counterclockwise",
            [-1, 0],
            None, id="2D_CCW_Y_axis"
        ),
        pytest.param(
            [0, 0], [1, 1], "counterclockwise",
            [-1/np.sqrt(2), 1/np.sqrt(2)],
            None, id="2D_CCW_Diagonal_Pos"
        ),
        pytest.param(
            [0, 0], [-1, 1], "counterclockwise",
            [-1/np.sqrt(2), -1/np.sqrt(2)], # Original unit: [-1/np.sqrt(2), 1/np.sqrt(2)], Rotated: [-1/np.sqrt(2), -1/np.sqrt(2)]
            None, id="2D_CCW_Diagonal_Neg_X"
        ),
        pytest.param(
            [1, 2], [4, 6], "counterclockwise", # Vector (3,4), Unit (0.6, 0.8)
            [-0.8, 0.6],
            None, id="2D_CCW_Arbitrary_Shifted"
        ),
        # --- 2D Clockwise Tests ---
        pytest.param(
            [0, 0], [1, 0], "clockwise",
            [0, -1],
            None, id="2D_CW_X_axis"
        ),
        pytest.param(
            [0, 0], [0, 1], "clockwise",
            [1, 0],
            None, id="2D_CW_Y_axis"
        ),
        pytest.param(
            [0, 0], [1, 1], "clockwise",
            [1/np.sqrt(2), -1/np.sqrt(2)],
            None, id="2D_CW_Diagonal_Pos"
        ),
        pytest.param(
            [1, 2], [4, 6], "clockwise", # Vector (3,4), Unit (0.6, 0.8)
            [0.8, -0.6],
            None, id="2D_CW_Arbitrary_Shifted"
        ),
        pytest.param(
            [0, 0, 0], [1, 0, 0], "counterclockwise",
            [0, 1, 0], # Original unit: [1,0,0], Rotated: [-0,1,0] then append original z (0)
            None, id="3D_CCW_X_axis_Z_zero"
        ),
        pytest.param(
            [0, 0, 0], [0, 1, 0], "counterclockwise",
            [-1, 0, 0], # Original unit: [0,1,0], Rotated: [-1,0,0] then append original z (0)
            None, id="3D_CCW_Y_axis_Z_zero"
        ),
        pytest.param(
            [0, 0, 0], [0, 0, 1], "counterclockwise", # Line along Z-axis
            [0, 0, 1], # Original unit: [0,0,1], Rotated: [-0,0,1] then append original z (1) -> [0,0,1]
            None, id="3D_CCW_Z_axis_no_XY_change"
        ),
        pytest.param(
            [0, 0, 0], [1, 1, 1], "counterclockwise", # Original unit: [1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)]
            [-1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)], # Rotated XY: [-1/np.sqrt(3), 1/np.sqrt(3)], Z unchanged
            None, id="3D_CCW_Diagonal_with_Z"
        ),
        pytest.param(
            [0, 0, 0], [1, 1, 1], "clockwise", # Original unit: [1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)]
            [1/np.sqrt(3), -1/np.sqrt(3), -1/np.sqrt(3)], # Rotated XY: [1/np.sqrt(3), -1/np.sqrt(3)], Z negated
            None, id="3D_CW_Diagonal_with_Z"
        ),
        pytest.param(
            [0, 0], [0, 0], "counterclockwise",
            None, ValueError, id="Degenerate_Identical_2D"
        ),
        pytest.param(
            [1, 2, 3], [1, 2, 3], "clockwise",
            None, ValueError, id="Degenerate_Identical_3D"
        ),
        pytest.param(
            [0, 0], [1e-10, 0], "counterclockwise",
            None, ValueError, id="Degenerate_Very_Close_2D"
        ),
        pytest.param(
            [0, 0], [1, 0], "invalid_turn_string",
            None, 
            ValueError, id="Invalid_Turn_String_Default_to_CW"
        ),
        pytest.param(
            [0, 0], [1, 0], "invalid_turn_string",
            None,
            ValueError, id="Invalid_Turn_String_Behaves_like_CW"
        ),
    ]
)
def test_vertical_line_unit_direction(line_start, line_end, turn, expected_vec, expected_exc):
    line_start_arr = np.array(line_start, dtype=float)
    line_end_arr = np.array(line_end, dtype=float)
    
    if expected_exc is None:
        expected_vec_arr = np.array(expected_vec, dtype=float)
        result_vec = vertical_line_unit_direction(line_start_arr, line_end_arr, turn)
        
        # 1. Check if the result is a unit vector (magnitude close to 1)
        # This is crucial for unit direction vectors.
        assert close(float(np.linalg.norm(result_vec)), 1.0), \
            f"Result vector {result_vec} does not have unit magnitude for inputs {line_start_arr}, {line_end_arr}, turn='{turn}'"
        
        # 2. Check if the direction is correct
        assert close(result_vec, expected_vec_arr), \
            f"Expected {expected_vec_arr}, got {result_vec} for inputs {line_start_arr}, {line_end_arr}, turn='{turn}'"
    else:
        with pytest.raises(expected_exc):
            vertical_line_unit_direction(line_start_arr, line_end_arr, turn)

@pytest.mark.parametrize(
    "point, line_start, line_end, expected_foot",
    [
        pytest.param(
            np.array([0, 1]), np.array([0, 0]), np.array([1, 0]), np.array([0, 0]),
            id="2D_point_above_horizontal_line_segment_projection_on_start"
        ),
        pytest.param(
            np.array([0.5, 1]), np.array([0, 0]), np.array([1, 0]), np.array([0.5, 0]),
            id="2D_point_above_horizontal_line_segment_projection_in_middle"
        ),
        pytest.param(
            np.array([2, 1]), np.array([0, 0]), np.array([1, 0]), np.array([2, 0]),
            id="2D_point_above_horizontal_line_segment_projection_outside_end"
        ),
        pytest.param(
            np.array([0, -1]), np.array([0, 0]), np.array([1, 0]), np.array([0, 0]),
            id="2D_point_below_horizontal_line_segment_projection_on_start"
        ),
        pytest.param(
            np.array([1, 0]), np.array([0, 0]), np.array([2, 0]), np.array([1, 0]),
            id="2D_point_on_line_segment"
        ),
        pytest.param(
            np.array([0, 0]), np.array([0, 0]), np.array([2, 0]), np.array([0, 0]),
            id="2D_point_is_line_start"
        ),
        pytest.param(
            np.array([2, 0]), np.array([0, 0]), np.array([2, 0]), np.array([2, 0]),
            id="2D_point_is_line_end"
        ),
        pytest.param(
            np.array([1, 1]), np.array([0, 0]), np.array([1, 1]), np.array([1, 1]),
            id="2D_point_on_diagonal_line_segment_is_end"
        ),
        pytest.param(
            np.array([0.5, 0.5]), np.array([0, 0]), np.array([1, 1]), np.array([0.5, 0.5]),
            id="2D_point_on_diagonal_line_segment_in_middle"
        ),
        pytest.param(
            np.array([1, 0]), np.array([0, 0]), np.array([1, 1]), np.array([0.5, 0.5]),
            id="2D_point_off_diagonal_line_segment"
        ),
        pytest.param(
            np.array([-1, 1]), np.array([0, 0]), np.array([0, 1]), np.array([0, 1]),
            id="2D_point_left_of_vertical_line_segment_projection_on_end"
        ),
        pytest.param(
            np.array([1, 0.5]), np.array([0, 0]), np.array([0, 1]), np.array([0, 0.5]),
            id="2D_point_right_of_vertical_line_segment_projection_in_middle"
        ),
        pytest.param(
            np.array([1, 1]), np.array([0, 0]), np.array([0, 0]), np.array([0, 0]),
            id="Degenerate_line_point_far_away"
        ),
        pytest.param(
            np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), np.array([0, 0]),
            id="Degenerate_line_point_is_line_start"
        ),
        pytest.param(
            np.array([100, -50]), np.array([10, 20]), np.array([10, 20]), np.array([10, 20]),
            id="Degenerate_line_with_non_origin_point"
        ),
        # --- 3D 测试用例 ---
        pytest.param(
            np.array([0, 0, 1]), np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 0, 0]),
            id="3D_point_above_xy_plane_line_segment"
        ),
        pytest.param(
            np.array([0.5, 0.5, 0.5]), np.array([0, 0, 0]), np.array([1, 1, 1]), np.array([0.5, 0.5, 0.5]),
            id="3D_point_on_diagonal_line_segment"
        ),
        pytest.param(
            np.array([1, 0, 0]), np.array([0, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 0]),
            id="3D_point_on_axis_line_segment_projection_on_start"
        ),
        pytest.param(
            np.array([1, 1, 1]), np.array([0, 0, 0]), np.array([2, 2, 2]), np.array([1, 1, 1]),
            id="3D_point_on_line_segment_in_middle"
        ),
        pytest.param(
            np.array([3, 3, 3]), np.array([0, 0, 0]), np.array([2, 2, 2]), np.array([3, 3, 3]),
            id="3D_point_outside_line_segment"
        ),
        pytest.param(
            np.array([0, 0, 5]), np.array([0, 0, 0]), np.array([0, 0, 10]), np.array([0, 0, 5]),
            id="3D_point_on_z_axis_line"
        ),
        pytest.param(
            np.array([1, 1, 0]), np.array([0, 0, 0]), np.array([0, 0, 1]), np.array([0, 0, 0]),
            id="3D_point_off_z_axis_line"
        ),
        pytest.param(
            np.array([-1, -1]), np.array([-2, 0]), np.array([0, 0]), np.array([-1, 0]),
            id="2D_negative_coords_point_below_line"
        ),
        pytest.param(
            np.array([-5, -5]), np.array([-10, -10]), np.array([-1, -1]), np.array([-5, -5]),
            id="2D_negative_coords_point_on_line"
        ),
        pytest.param(
            np.array([-1, 1, -1]), np.array([-2, 0, 0]), np.array([0, 0, 0]), np.array([-1, 0, 0]),
            id="3D_negative_coords_point_off_line"
        ),
        pytest.param(
            np.array([1e-10, 1e-10]), np.array([0, 0]), np.array([1, 0]), np.array([1e-10, 0]),
            id="2D_very_small_numbers"
        ),
        pytest.param(
            np.array([1e5, 1e5]), np.array([0, 0]), np.array([1e6, 0]), np.array([1e5, 0]),
            id="2D_very_large_numbers"
        ),
        pytest.param(
            np.array([0.0000000001, 0.0000000001]), np.array([0, 0]), np.array([0.0000000002, 0.0000000002]), np.array([0.0000000001, 0.0000000001]),
            id="2D_tiny_line_segment_and_point"
        ),
    ]
)
def test_vertical_point_to_line(point, line_start, line_end, expected_foot):
    """
    测试 vertical_point_to_line 函数计算垂足点的正确性。
    """
    result_foot = vertical_point_to_line(point, line_start, line_end)
    assert close(result_foot, expected_foot), f"Expected: {expected_foot}, Got: {result_foot}"


@pytest.mark.parametrize(
    "point, line_start, line_end, expected_t, expected_exc",
    [
        pytest.param(
            np.array([0, 0]), np.array([0, 0]), np.array([1, 0]), 0.0, None,
            id="2D_point_is_line_start"
        ),
        pytest.param(
            np.array([1, 0]), np.array([0, 0]), np.array([1, 0]), 1.0, None,
            id="2D_point_is_line_end"
        ),
        pytest.param(
            np.array([0.5, 0]), np.array([0, 0]), np.array([1, 0]), 0.5, None,
            id="2D_point_in_middle"
        ),
        pytest.param(
            np.array([-1, 0]), np.array([0, 0]), np.array([1, 0]), -1.0, None,
            id="2D_point_before_start"
        ),
        pytest.param(
            np.array([2, 0]), np.array([0, 0]), np.array([1, 0]), 2.0, None,
            id="2D_point_after_end"
        ),
        pytest.param(
            np.array([0.5, 0.5]), np.array([0, 0]), np.array([1, 1]), 0.5, None,
            id="2D_diagonal_point_in_middle"
        ),
        pytest.param(
            np.array([0, 0]), np.array([0, 0]), np.array([1, 1]), 0.0, None,
            id="2D_diagonal_point_is_start"
        ),
        pytest.param(
            np.array([1, 1]), np.array([0, 0]), np.array([1, 1]), 1.0, None,
            id="2D_diagonal_point_is_end"
        ),
        pytest.param(
            np.array([0, 0.5]), np.array([0, 0]), np.array([0, 1]), 0.5, None,
            id="2D_vertical_point_in_middle"
        ),
        pytest.param(
            np.array([0, -1]), np.array([0, 0]), np.array([0, 1]), -1.0, None,
            id="2D_vertical_point_before_start"
        ),
        pytest.param(
            np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([1, 1, 1]), 0.0, None,
            id="3D_point_is_line_start"
        ),
        pytest.param(
            np.array([1, 1, 1]), np.array([0, 0, 0]), np.array([1, 1, 1]), 1.0, None,
            id="3D_point_is_line_end"
        ),
        pytest.param(
            np.array([0.5, 0.5, 0.5]), np.array([0, 0, 0]), np.array([1, 1, 1]), 0.5, None,
            id="3D_point_in_middle"
        ),
        pytest.param(
            np.array([-1, -1, -1]), np.array([0, 0, 0]), np.array([1, 1, 1]), -1.0, None,
            id="3D_point_before_start"
        ),
        pytest.param(
            np.array([2, 2, 2]), np.array([0, 0, 0]), np.array([1, 1, 1]), 2.0, None,
            id="3D_point_after_end"
        ),
        pytest.param(
            np.array([0, 0, 5]), np.array([0, 0, 0]), np.array([0, 0, 10]), 0.5, None,
            id="3D_point_on_z_axis_line"
        ),
        pytest.param(
            np.array([-5, -5]), np.array([-10, -10]), np.array([-1, -1]), 0.5555555555555556, None, # ( -5 - (-10) ) / ( -1 - (-10) ) = 5/9
            id="2D_negative_coords_point_in_middle"
        ),
        pytest.param(
            np.array([-10, -10, -10]), np.array([-10, -10, -10]), np.array([-1, -1, -1]), 0.0, None,
            id="3D_negative_coords_point_is_start"
        ),
        pytest.param(
            np.array([0.3333333333333333, 0.3333333333333333]), np.array([0, 0]), np.array([1, 1]), 0.3333333333333333, None,
            id="2D_floating_point_precision_t_not_exact"
        ),
        pytest.param(
            np.array([1e-9, 0]), np.array([0, 0]), np.array([1, 0]), 1e-9, None,
            id="2D_very_small_t"
        ),
        pytest.param(
            np.array([1e5, 0]), np.array([0, 0]), np.array([1, 0]), 1e5, None,
            id="2D_very_large_t"
        ),
        pytest.param(
            np.array([0.0000000001, 0.0000000001]), np.array([0, 0]), np.array([0.0000000002, 0.0000000002]), None, ValueError,
            id="2D_tiny_line_segment_point_in_middle"
        ),
        pytest.param(
            np.array([0.0000000000000001, 0.0000000000000001]), np.array([0, 0]), np.array([1, 1]), 1e-16, None,
            id="2D_point_very_close_to_start"
        ),
        pytest.param(
            np.array([1, 1]), np.array([0, 0]), np.array([0, 0]), None, ValueError,
            id="Degenerate_line_raises_ValueError"
        ),
        pytest.param(
            np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), None, ValueError,
            id="Degenerate_line_point_is_start_raises_ValueError"
        ),
        pytest.param(
            np.array([5, 5, 5]), np.array([1, 2, 3]), np.array([1, 2, 3]), None, ValueError,
            id="3D_Degenerate_line_raises_ValueError"
        ),
    ]
)
def test_get_parameter_t_on_line(point, line_start, line_end, expected_t, expected_exc):
    """
    测试 get_parameter_t_on_line 函数计算参数 t 的正确性。
    """
    if expected_exc is None:
        result_t = get_parameter_t_on_line(point, line_start, line_end)
        assert close(result_t, expected_t), f"Expected t: {expected_t}, Got t: {result_t}"
    else:
        with pytest.raises(expected_exc):
            get_parameter_t_on_line(point, line_start, line_end)

@pytest.mark.parametrize(
    "point, line_start, line_end, line_type, expected_result, expected_exc",
    [
        pytest.param(np.array([0, 0]), np.array([0, 0]), np.array([1, 0]), "InfinityLine", True, None, id="InfLine_point_is_start"),
        pytest.param(np.array([1, 0]), np.array([0, 0]), np.array([1, 0]), "InfinityLine", True, None, id="InfLine_point_is_end"),
        pytest.param(np.array([0.5, 0]), np.array([0, 0]), np.array([1, 0]), "InfinityLine", True, None, id="InfLine_point_in_middle"),
        pytest.param(np.array([-1, 0]), np.array([0, 0]), np.array([1, 0]), "InfinityLine", True, None, id="InfLine_point_before_start"),
        pytest.param(np.array([2, 0]), np.array([0, 0]), np.array([1, 0]), "InfinityLine", True, None, id="InfLine_point_after_end"),
        pytest.param(np.array([0.5, 0.5]), np.array([0, 0]), np.array([1, 1]), "InfinityLine", True, None, id="InfLine_diagonal_point_in_middle"),
        pytest.param(np.array([-1, -1]), np.array([0, 0]), np.array([1, 1]), "InfinityLine", True, None, id="InfLine_diagonal_point_before_start"),
        pytest.param(np.array([2, 2]), np.array([0, 0]), np.array([1, 1]), "InfinityLine", True, None, id="InfLine_diagonal_point_after_end"),
        pytest.param(np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([1, 1, 1]), "InfinityLine", True, None, id="InfLine_3D_point_is_start"),
        pytest.param(np.array([0.5, 0.5, 0.5]), np.array([0, 0, 0]), np.array([1, 1, 1]), "InfinityLine", True, None, id="InfLine_3D_point_in_middle"),
        pytest.param(np.array([2, 2, 2]), np.array([0, 0, 0]), np.array([1, 1, 1]), "InfinityLine", True, None, id="InfLine_3D_point_after_end"),
        pytest.param(np.array([0, 0]), np.array([0, 0]), np.array([1, 0]), "Ray", True, None, id="Ray_point_is_start"),
        pytest.param(np.array([0.5, 0]), np.array([0, 0]), np.array([1, 0]), "Ray", True, None, id="Ray_point_in_middle"),
        pytest.param(np.array([1, 0]), np.array([0, 0]), np.array([1, 0]), "Ray", True, None, id="Ray_point_is_end"),
        pytest.param(np.array([2, 0]), np.array([0, 0]), np.array([1, 0]), "Ray", True, None, id="Ray_point_after_end"),
        pytest.param(np.array([-0.0000000001, 0]), np.array([0, 0]), np.array([1, 0]), "Ray", True, None, id="Ray_point_just_before_start_close"), # t is close to 0, but slightly negative
        pytest.param(np.array([-0.1, 0]), np.array([0, 0]), np.array([1, 0]), "Ray", False, None, id="Ray_point_before_start_far"),
        pytest.param(np.array([-1, 0]), np.array([0, 0]), np.array([1, 0]), "Ray", False, None, id="Ray_point_before_start_very_far"),
        pytest.param(np.array([0.5, 0.5]), np.array([0, 0]), np.array([1, 1]), "Ray", True, None, id="Ray_diagonal_point_in_middle"),
        pytest.param(np.array([-0.1, -0.1]), np.array([0, 0]), np.array([1, 1]), "Ray", False, None, id="Ray_diagonal_point_before_start"),
        pytest.param(np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([1, 1, 1]), "Ray", True, None, id="Ray_3D_point_is_start"),
        pytest.param(np.array([-0.0000000001, -0.0000000001, -0.0000000001]), np.array([0, 0, 0]), np.array([1, 1, 1]), "Ray", True, None, id="Ray_3D_point_just_before_start_close"), # t is close to 0, but slightly negative
        pytest.param(np.array([0, 0]), np.array([0, 0]), np.array([1, 0]), "LineSegment", True, None, id="LineSeg_point_is_start"),
        pytest.param(np.array([0.5, 0]), np.array([0, 0]), np.array([1, 0]), "LineSegment", True, None, id="LineSeg_point_in_middle"),
        pytest.param(np.array([1, 0]), np.array([0, 0]), np.array([1, 0]), "LineSegment", True, None, id="LineSeg_point_is_end"),
        pytest.param(np.array([-0.0000000001, 0]), np.array([0, 0]), np.array([1, 0]), "LineSegment", True, None, id="LineSeg_point_just_before_start_close"), # t is close to 0, but slightly negative
        pytest.param(np.array([1.0000000001, 0]), np.array([0, 0]), np.array([1, 0]), "LineSegment", True, None, id="LineSeg_point_just_after_end_close"), # t is close to 1, but slightly positive
        pytest.param(np.array([-0.1, 0]), np.array([0, 0]), np.array([1, 0]), "LineSegment", False, None, id="LineSeg_point_before_start_far"),
        pytest.param(np.array([1.1, 0]), np.array([0, 0]), np.array([1, 0]), "LineSegment", False, None, id="LineSeg_point_after_end_far"),
        pytest.param(np.array([0.5, 0.5]), np.array([0, 0]), np.array([1, 1]), "LineSegment", True, None, id="LineSeg_diagonal_point_in_middle"),
        pytest.param(np.array([-0.1, -0.1]), np.array([0, 0]), np.array([1, 1]), "LineSegment", False, None, id="LineSeg_diagonal_point_before_start"),
        pytest.param(np.array([1.1, 1.1]), np.array([0, 0]), np.array([1, 1]), "LineSegment", False, None, id="LineSeg_diagonal_point_after_end"),
        pytest.param(np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([1, 1, 1]), "LineSegment", True, None, id="LineSeg_3D_point_is_start"),
        pytest.param(np.array([1, 1, 1]), np.array([0, 0, 0]), np.array([1, 1, 1]), "LineSegment", True, None, id="LineSeg_3D_point_is_end"),
        pytest.param(np.array([-0.0000000001, -0.0000000001, -0.0000000001]), np.array([0, 0, 0]), np.array([1, 1, 1]), "LineSegment", True, None, id="LineSeg_3D_point_just_before_start_close"), # t is close to 0, but slightly negative
        pytest.param(np.array([0, 1]), np.array([0, 0]), np.array([1, 0]), "InfinityLine", False, None, id="PointOffLine_InfLine_2D"),
        pytest.param(np.array([0, 1]), np.array([0, 0]), np.array([1, 0]), "Ray", False, None, id="PointOffLine_Ray_2D"),
        pytest.param(np.array([0, 1]), np.array([0, 0]), np.array([1, 0]), "LineSegment", False, None, id="PointOffLine_LineSeg_2D"),
        pytest.param(np.array([0, 0, 1]), np.array([0, 0, 0]), np.array([1, 0, 0]), "InfinityLine", False, None, id="PointOffLine_InfLine_3D"),
        pytest.param(np.array([0.5, 0.5, 1]), np.array([0, 0, 0]), np.array([1, 1, 0]), "LineSegment", False, None, id="PointOffLine_LineSeg_3D_diagonal"),
        pytest.param(np.array([0.0001, 0.0001]), np.array([0, 0]), np.array([1, 0]), "InfinityLine", False, None, id="PointOffLine_InfLine_2D_small_dist"), # Small but non-zero distance
        pytest.param(np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), "InfinityLine", True, None, id="Degenerate_point_is_line_point_InfLine"),
        pytest.param(np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), "Ray", True, None, id="Degenerate_point_is_line_point_Ray"),
        pytest.param(np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), "LineSegment", True, None, id="Degenerate_point_is_line_point_LineSeg"),
        pytest.param(np.array([1, 1]), np.array([0, 0]), np.array([0, 0]), "InfinityLine", False, None, id="Degenerate_point_not_line_point_InfLine"),
        pytest.param(np.array([1, 1]), np.array([0, 0]), np.array([0, 0]), "Ray", False, None, id="Degenerate_point_not_line_point_Ray"),
        pytest.param(np.array([1, 1]), np.array([0, 0]), np.array([0, 0]), "LineSegment", False, None, id="Degenerate_point_not_line_point_LineSeg"),
        pytest.param(np.array([10, 20, 30]), np.array([10, 20, 30]), np.array([10, 20, 30]), "InfinityLine", True, None, id="Degenerate_3D_point_is_line_point"),
        pytest.param(np.array([10, 20, 31]), np.array([10, 20, 30]), np.array([10, 20, 30]), "InfinityLine", False, None, id="Degenerate_3D_point_not_line_point"),
        pytest.param(np.array([0.5, 1e-10]), np.array([0, 0]), np.array([1, 0]), "InfinityLine", True, None, id="InfLine_point_very_close_to_line"),
        pytest.param(np.array([0.5, 1e-8]), np.array([0, 0]), np.array([1, 0]), "InfinityLine", True, None, id="InfLine_point_close_to_line"), # 假设 close 容忍度足够大
        pytest.param(np.array([0.5, 1e-3]), np.array([0, 0]), np.array([1, 0]), "InfinityLine", False, None, id="InfLine_point_slightly_off_line"), # 假设超出 close 容忍度
        pytest.param(np.array([1e-10, 0]), np.array([0, 0]), np.array([1, 0]), "LineSegment", True, None, id="LineSeg_t_very_close_to_0"),
        pytest.param(np.array([1 - 1e-10, 0]), np.array([0, 0]), np.array([1, 0]), "LineSegment", True, None, id="LineSeg_t_very_close_to_1"),
        pytest.param(np.array([-1e-10, 0]), np.array([0, 0]), np.array([1, 0]), "LineSegment", True, None, id="LineSeg_t_slightly_negative_close_to_0"), # check_paramerized_line_range handles this
        pytest.param(np.array([1 + 1e-10, 0]), np.array([0, 0]), np.array([1, 0]), "LineSegment", True, None, id="LineSeg_t_slightly_positive_close_to_1"), # check_paramerized_line_range handles this
        pytest.param(np.array([-1e-10, 0]), np.array([0, 0]), np.array([1, 0]), "Ray", True, None, id="Ray_t_slightly_negative_close_to_0"), # check_paramerized_line_range handles this
        pytest.param(np.array([0, 0]), np.array([0, 0]), np.array([1, 0]), "InvalidType", None, ValueError, id="Invalid_line_type"),
        pytest.param(np.array([0, 0]), np.array([0, 0]), np.array([1, 0]), "Line", None, ValueError, id="Invalid_line_type_similar_name"),
        pytest.param(np.array([0, 0]), np.array([0, 0]), np.array([1, 0]), "", None, ValueError, id="Invalid_line_type_empty_string"),
    ]
)
def test_is_point_on_line(point, line_start, line_end, line_type, expected_result, expected_exc):
    """
    测试 is_point_on_line 函数判断点是否在线上的正确性
    """
    if expected_exc is None:
        result = is_point_on_line(point, line_start, line_end, line_type)
        # 简化断言信息
        assert result == expected_result, f"Expected: {expected_result}, Got: {result}"
    else:
        with pytest.raises(expected_exc):
            is_point_on_line(point, line_start, line_end, line_type)