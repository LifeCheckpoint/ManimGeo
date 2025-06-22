import numpy as np
import pytest

from manimgeo.math import *

@pytest.mark.parametrize(
    "origin_center, origin_radius, origin_normal, base_center, base_radius, base_normal, expected_result, expected_exc",
    [
        pytest.param(np.array([5, 0, 0]), 1, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 2, np.array([0, 0, 1]),
                     (np.array([0.8, 0, 0]), 0.2, np.array([0, 0, 1])), None, id="InvCirc_2D_Basic"),
        pytest.param(np.array([5, 0, 0]), 1, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 2, np.array([0, 0, 1]),
                     (np.array([5/6, 0, 0]), 1/6, np.array([0, 0, 1])), None, id="InvCirc_2D_Basic_Corrected"),
        pytest.param(np.array([7, 0, 0]), 1, np.array([0, 0, 1]),
                     np.array([2, 0, 0]), 2, np.array([0, 0, 1]),
                     (np.array([2 + 5/6, 0, 0]), 1/6, np.array([0, 0, 1])), None, id="InvCirc_2D_OffsetBase"),
        pytest.param(np.array([5, 0, 0]), 1, np.array([0, 1, 0]), # Normal in Y direction
                     np.array([0, 0, 0]), 2, np.array([0, 1, 0]),
                     (np.array([5/6, 0, 0]), 1/6, np.array([0, 1, 0])), None, id="InvCirc_3D_Basic"),
        pytest.param(np.array([10, 0, 0]), 2, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 5, np.array([0, 0, 1]),
                     (np.array([5**2 * (1/(10-2) + 1/(10+2))/2, 0, 0]), 5**2 * (1/(10-2) - 1/(10+2))/2, np.array([0, 0, 1])), None, id="InvCirc_2D_DiffRadii"),
        pytest.param(np.array([10, 0, 0]), 2, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 5, np.array([0, 0, 1]),
                     (np.array([125/48, 0, 0]), 25/48, np.array([0, 0, 1])), None, id="InvCirc_2D_DiffRadii_Corrected"),
        pytest.param(np.array([-5, 0, 0]), 1, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 2, np.array([0, 0, 1]),
                     (np.array([-5/6, 0, 0]), 1/6, np.array([0, 0, 1])), None, id="InvCirc_2D_NegativeCoords"),
        pytest.param(np.array([5, 0, 0]), 1, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 2, np.array([0, 0, -1]), # base_normal is opposite
                     (np.array([5/6, 0, 0]), 1/6, np.array([0, 0, 1])), None, id="InvCirc_NormalOpposite"),
        pytest.param(np.array([5, 0, 0]), 1, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 2, np.array([1, 0, 0]), # Perpendicular normal
                     None, ValueError, id="InvCirc_Error_NormalsNotCollinear"),
        pytest.param(np.array([2, 0, 0]), 2, np.array([0, 0, 1]), # d=2, r=2
                     np.array([0, 0, 0]), 5, np.array([0, 0, 1]),
                     None, ValueError, id="InvCirc_Error_OriginPassesThroughBaseCenter"),
        pytest.param(np.array([1, 0, 0]), 2, np.array([0, 0, 1]), # d=1, r=2
                     np.array([0, 0, 0]), 5, np.array([0, 0, 1]),
                     None, ValueError, id="InvCirc_Error_OriginContainsBaseCenter"),
        pytest.param(np.array([0, 0, 0]), 2, np.array([0, 0, 1]), # d=0, r=2
                     np.array([0, 0, 0]), 5, np.array([0, 0, 1]),
                     None, ValueError, id="InvCirc_Error_OriginCenterIsBaseCenter"),
        pytest.param(np.array([1 + 1e-8, 0, 0]), 1, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 2, np.array([0, 0, 1]),
                     (np.array([2**2 * (1/(1e-8) + 1/(2+1e-8))/2, 0, 0]), 2**2 * (1/(1e-8) - 1/(2+1e-8))/2, np.array([0, 0, 1])), None, id="InvCirc_Edge_d_min_close_to_0"),
        pytest.param(np.array([1 + 1e-8, 0, 0]), 1, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 2, np.array([0, 0, 1]),
                     (np.array([2.0000000000000004e+08, 0.0, 0.0]), 2.0000000000000004e+08, np.array([0, 0, 1])), None, id="InvCirc_Edge_d_min_close_to_0_Corrected"),
    ]
)
def test_inverse_circle(
    origin_center, origin_radius, origin_normal,
    base_center, base_radius, base_normal,
    expected_result, expected_exc
):
    if expected_exc is None:
        inv_center, inv_radius, inv_normal = inverse_circle(
            origin_center, origin_radius, origin_normal,
            base_center, base_radius, base_normal
        )
        assert close(inv_center, expected_result[0]), "Center mismatch"
        assert close(inv_radius, expected_result[1]), "Radius mismatch"
        assert close(inv_normal, expected_result[2]), "Normal mismatch"
    else:
        with pytest.raises(expected_exc):
            inverse_circle(origin_center, origin_radius, origin_normal,
                           base_center, base_radius, base_normal)
                           
@pytest.mark.parametrize(
    "origin_center, origin_radius, origin_normal, base_center, base_radius, base_normal, expected_result, expected_exc",
    [
        pytest.param(np.array([2, 0]), 2, np.array([0, 0, 1]), # 2D points, 3D normal
                     np.array([0, 0]), 4, np.array([0, 0, 1]),
                     (np.array([4, 4]), np.array([4, -4])), None, id="InvLine_2D_Basic"),
        pytest.param(np.array([2, 0]), 2, np.array([0, 0, 1]), # 2D points, 3D normal
                     np.array([0, 0]), 4, np.array([0, 0, 1]),
                     (np.array([4, 1]), np.array([4, -1])), None, id="InvLine_2D_Basic_Corrected"),
        pytest.param(np.array([2, 0, 0]), 2, np.array([0, 1, 0]), # Normal in Y direction
                     np.array([0, 0, 0]), 4, np.array([0, 1, 0]),
                     (np.array([4, 0, 1]), np.array([4, 0, -1])), None, id="InvLine_3D_Basic"),
        pytest.param(np.array([4, 0, 0]), 2, np.array([0, 0, 1]),
                     np.array([2, 0, 0]), 4, np.array([0, 0, 1]),
                     (np.array([2 + 4, 1]), np.array([2 + 4, -1])), None, id="InvLine_2D_OffsetBase"),
        pytest.param(np.array([2, 0]), 2, np.array([0, 0, 1]),
                     np.array([0, 0]), 4, np.array([0, 0, -1]), # base_normal is opposite
                     (np.array([4, 1]), np.array([4, -1])), None, id="InvLine_NormalOpposite"),
        pytest.param(np.array([1, 1, 0]), np.sqrt(2), np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 2, np.array([0, 0, 1]),
                     (np.array([1, -1, 0]) * (2**2/np.sqrt(2)/2), np.array([-1, 1, 0]) * (2**2/np.sqrt(2)/2)), None, id="InvLine_2D_Diagonal"),
        pytest.param(np.array([1, 1, 0]), np.sqrt(2), np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 2, np.array([0, 0, 1]),
                     (np.array([1+1/np.sqrt(2), 1-1/np.sqrt(2), 0]), np.array([1-1/np.sqrt(2), 1+1/np.sqrt(2), 0])), None, id="InvLine_2D_Diagonal_Corrected"),
        pytest.param(np.array([2, 0, 0]), 2, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 4, np.array([1, 0, 0]),
                     None, ValueError, id="InvLine_Error_NormalsNotCollinear"),
        pytest.param(np.array([3, 0, 0]), 2, np.array([0, 0, 1]), # d=3, r=2 (d > r)
                     np.array([0, 0, 0]), 4, np.array([0, 0, 1]),
                     None, ValueError, id="InvLine_Error_OriginNotPassesThroughBaseCenter_Outside"),
        pytest.param(np.array([1, 0, 0]), 2, np.array([0, 0, 1]), # d=1, r=2 (d < r)
                     np.array([0, 0, 0]), 4, np.array([0, 0, 1]),
                     None, ValueError, id="InvLine_Error_OriginNotPassesThroughBaseCenter_Contains"),
        pytest.param(np.array([0, 0, 0]), 2, np.array([0, 0, 1]), # d=0, r=2 (d != r)
                     np.array([0, 0, 0]), 4, np.array([0, 0, 1]),
                     None, ValueError, id="InvLine_Error_OriginCenterIsBaseCenter"),
        pytest.param(np.array([2 + 1e-9, 0, 0]), 2, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 4, np.array([0, 0, 1]),
                     None, ValueError, id="InvLine_Edge_d_close_to_r_outside"), # Should still fail if not exactly equal
        pytest.param(np.array([2 - 1e-9, 0, 0]), 2, np.array([0, 0, 1]),
                     np.array([0, 0, 0]), 4, np.array([0, 0, 1]),
                     None, ValueError, id="InvLine_Edge_d_close_to_r_inside"), # Should still fail if not exactly equal
    ]
)
def test_inverse_circle_to_line(origin_center, origin_radius, origin_normal,
                                base_center, base_radius, base_normal,
                                expected_result, expected_exc):
    if expected_exc is None:
        line_point1, line_point2 = inverse_circle_to_line(
            origin_center, origin_radius, origin_normal,
            base_center, base_radius, base_normal
        )
        assert close(line_point1, expected_result[0]), "Line Point 1 mismatch"
        assert close(line_point2, expected_result[1]), "Line Point 2 mismatch"
    else:
        with pytest.raises(expected_exc):
            inverse_circle_to_line(origin_center, origin_radius, origin_normal, base_center, base_radius, base_normal)