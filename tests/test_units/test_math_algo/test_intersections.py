import pytest
import numpy as np
from manimgeo.math import *

@pytest.mark.parametrize(
    "line1_start, line1_end, line2_start, line2_end, line1_type, line2_type, as_infinty, expected_result, expected_exc",
    [
        pytest.param(np.array([0, -1, 0]), np.array([0, 1, 0]), np.array([-1, 0, 0]), np.array([1, 0, 0]), "InfinityLine", "InfinityLine", False, np.array([0, 0, 0]), None, id="Basic_InfInf_Perp_Origin"),
        pytest.param(np.array([1, 0, 0]), np.array([1, 2, 0]), np.array([0, 1, 0]), np.array([2, 1, 0]), "InfinityLine", "InfinityLine", False, np.array([1, 1, 0]), None, id="Basic_InfInf_Perp_Offset"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 1, 0]), np.array([0, 1, 0]), np.array([1, 0, 0]), "InfinityLine", "InfinityLine", False, np.array([0.5, 0.5, 0]), None, id="Basic_InfInf_Diagonal"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 1, 1]), np.array([0, 1, 0]), np.array([1, 0, 1]), "InfinityLine", "InfinityLine", False, np.array([0.5, 0.5, 0.5]), None, id="Basic_InfInf_3D"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 1, 0]), np.array([0, 1, 0]), np.array([1, 0, 0]), "LineSegment", "LineSegment", False, np.array([0.5, 0.5, 0]), None, id="Basic_LineSegLineSeg_Intersect"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0.5, -1, 0]), np.array([0.5, 0, 0]), "Ray", "Ray", False, np.array([0.5, 0, 0]), None, id="Basic_RayRay_Intersect"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0.5, -1, 0]), np.array([0.5, 0, 0]), "Ray", "LineSegment", False, np.array([0.5, 0, 0]), None, id="Basic_RayLineSeg_Intersect"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([1, 1, 0]), "InfinityLine", "InfinityLine", False, None, None, id="NoIntersect_Parallel_2D"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 1, 1]), np.array([0, 0, 1]), np.array([1, 1, 2]), "InfinityLine", "InfinityLine", False, None, None, id="NoIntersect_Parallel_3D"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 1, 1]), "InfinityLine", "InfinityLine", False, None, None, id="NoIntersect_Skew"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 1, 0]), np.array([0, 0, 1]), np.array([1, 0, 1]), "InfinityLine", "InfinityLine", False, None, None, id="NoIntersect_Skew_2"),
        pytest.param(np.array([0, 0, 0]), np.array([0.4, 0.4, 0]), np.array([0.6, 0.4, 0]), np.array([0.4, 0.6, 0]), "LineSegment", "LineSegment", False, None, None, id="NoIntersect_LineSeg_OutOfRange"),
        pytest.param(np.array([1, 0, 0]), np.array([2, 0, 0]), np.array([0.5, -1, 0]), np.array([0.5, 0, 0]), "Ray", "LineSegment", False, None, None, id="NoIntersect_Ray_BehindOrigin"),
        pytest.param(np.array([0, 0, 0]), np.array([-1, 0, 0]), np.array([1, 0, 0]), np.array([2, 0, 0]), "Ray", "Ray", False, None, None, id="NoIntersect_RayRay_OppositeDirections"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0.2, 0, 0]), np.array([0.8, 0, 0]), "LineSegment", "LineSegment", False, None, ValueError, id="Collinear_LineSegLineSeg_Overlap"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([-0.5, 0, 0]), np.array([1.5, 0, 0]), "LineSegment", "LineSegment", False, None, ValueError, id="Collinear_LineSegLineSeg_Contains"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0.5, 0, 0]), np.array([1.5, 0, 0]), "Ray", "Ray", False, None, ValueError, id="Collinear_RayRay_Overlap"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0.5, 0, 0]), np.array([2, 0, 0]), "LineSegment", "Ray", False, None, ValueError, id="Collinear_LineSegRay_Overlap"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([2, 0, 0]), np.array([3, 0, 0]), "InfinityLine", "InfinityLine", False, None, ValueError, id="Collinear_InfInf_Overlap"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([-1, 0, 0]), np.array([2, 0, 0]), "InfinityLine", "LineSegment", False, None, ValueError, id="Collinear_InfLineSeg_Overlap"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([1, 0, 0]), np.array([2, 0, 0]), "LineSegment", "LineSegment", False, np.array([1, 0, 0]), None, id="Collinear_LineSegLineSeg_Touch"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([1, 0, 0]), np.array([2, 0, 0]), "LineSegment", "Ray", False, np.array([1, 0, 0]), None, id="Collinear_LineSegRay_Touch"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 0, 0]), np.array([-1, 0, 0]), "LineSegment", "Ray", False, np.array([0, 0, 0]), None, id="Collinear_LineSegRay_Touch_ReversedRay"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([2, 0, 0]), np.array([3, 0, 0]), "LineSegment", "LineSegment", False, None, None, id="Collinear_LineSegLineSeg_NoOverlap"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([-2, 0, 0]), np.array([-1, 0, 0]), "Ray", "LineSegment", False, None, None, id="Collinear_RayLineSeg_NoOverlap"),
        pytest.param(np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([-1, 0, 0]), np.array([1, 0, 0]), "LineSegment", "InfinityLine", False, None, ValueError, id="Degenerate_Line1_Point_Intersect"),
        pytest.param(np.array([0, 1, 0]), np.array([0, 1, 0]), np.array([-1, 0, 0]), np.array([1, 0, 0]), "LineSegment", "InfinityLine", False, None, ValueError, id="Degenerate_Line1_Point_NoIntersect"),
        pytest.param(np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0]), "LineSegment", "LineSegment", False, None, ValueError, id="Degenerate_BothPoints_Same"),
        pytest.param(np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([1, 1, 1]), np.array([1, 1, 1]), "LineSegment", "LineSegment", False, None, ValueError, id="Degenerate_BothPoints_Different"),
        pytest.param(np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([1, 0, 0]), "LineSegment", "Ray", False, None, ValueError, id="Degenerate_Point_Ray_StartsAt"),
        pytest.param(np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([-1, 0, 0]), np.array([1, 0, 0]), "LineSegment", "Ray", False, None, ValueError, id="Degenerate_Point_Ray_PassesThrough"),
        pytest.param(np.array([0, 0, 0]), np.array([0.4, 0.4, 0]), np.array([0.6, 0.4, 0]), np.array([0.4, 0.6, 0]), "LineSegment", "LineSegment", True, np.array([0.5, 0.5, 0]), None, id="AsInf_LineSeg_Intersect"),
        pytest.param(np.array([0, 0, 0]), np.array([-1, 0, 0]), np.array([1, 1, 0]), np.array([2, 3, 0]), "Ray", "Ray", True, np.array([0.5, 0, 0]), None, id="AsInf_RayRay_Intersect"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([1, 1, 0]), "LineSegment", "LineSegment", True, None, None, id="AsInf_Parallel_NoIntersect"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 1, 1]), "LineSegment", "LineSegment", True, None, None, id="AsInf_Skew_NoIntersect"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0.2, 0, 0]), np.array([0.8, 0, 0]), "LineSegment", "LineSegment", True, None, ValueError, id="AsInf_Collinear_Overlap_StillError"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0.9999999999, -1, 0]), np.array([0.9999999999, 1, 0]), "LineSegment", "LineSegment", False, np.array([0.9999999999, 0, 0]), None, id="FP_LineSeg_NearEnd"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([1e-10, -1, 0]), np.array([1e-10, 1, 0]), "Ray", "Ray", False, np.array([1e-10, 0, 0]), None, id="FP_Ray_NearOrigin"),
        pytest.param(np.array([0, 0, 0]), np.array([100, 1, 0]), np.array([0, 1, 0]), np.array([100, 0, 0]), "InfinityLine", "InfinityLine", False, np.array([50, 0.5, 0]), None, id="FP_AlmostParallel_Intersect"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0.5, 0, 1e-9]), np.array([1.5, 0, 1e-9]), "LineSegment", "LineSegment", False, None, ValueError, id="FP_AlmostCollinear_Overlap"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 1, 1]), np.array([1e-10, 1e-10, -1]), np.array([1e-10, 1e-10, 1]), "InfinityLine", "InfinityLine", False, np.array([1e-10, 1e-10, 1e-10]), None, id="FP_TinyIntersection"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([1e5, -1, 0]), np.array([1e5, 1, 0]), "InfinityLine", "InfinityLine", False, np.array([1e5, 0, 0]), None, id="FP_LargeIntersection"),
    ]
)
def test_intersection_line_line(
    line1_start, line1_end, line2_start, line2_end,
    line1_type, line2_type, as_infinty,
    expected_result, expected_exc
):
    """
    Test cases for intersection_line_line function, focusing on boundary conditions.
    """
    if expected_exc is None:
        result = intersection_line_line(
            line1_start, line1_end, line2_start, line2_end,
            line1_type, line2_type, as_infinty
        )
        if expected_result is None:
            assert result is None, f"Expected None, Got {result}"
        else:
            assert result is not None, f"Expected {expected_result}, Got None"
            assert close(result, expected_result)
    else:
        with pytest.raises(expected_exc):
            intersection_line_line(
                line1_start, line1_end, line2_start, line2_end,
                line1_type, line2_type, as_infinty
            )