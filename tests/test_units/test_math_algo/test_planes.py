import pytest
import numpy as np
from manimgeo.math import *

@pytest.mark.parametrize(
    "point1, point2, point3, constant, expected_result, expected_exc",
    [
        pytest.param(np.array([1, 0, 1]), np.array([0, 1, 1]), np.array([0, 0, 1]), 1, (0.0, 0.0, 1.0), None, id="Valid_XY_Plane_Z1_Const1"),
        pytest.param(np.array([1, 1, 0]), np.array([0, 1, 1]), np.array([0, 1, 0]), 1, (0.0, 1.0, 0.0), None, id="Valid_XZ_Plane_Y1_Const1"),
        pytest.param(np.array([1, 1, 0]), np.array([1, 0, 1]), np.array([1, 0, 0]), 1, (1.0, 0.0, 0.0), None, id="Valid_YZ_Plane_X1_Const1"),
        pytest.param(np.array([1, 0, 1]), np.array([0, 1, 1]), np.array([0, 0, 1]), None, (0.0, 0.0, 1.0), None, id="Valid_XY_Plane_Z1_Const_Default"),
        
        # TO_CHECK
        pytest.param(np.array([1, 1, 0]), np.array([0, 1, 1]), np.array([0, 1, 0]), None, (0.0, -1.0, 0.0), None, id="Valid_XZ_Plane_Y1_Const_Default"),

        pytest.param(np.array([1, 1, 0]), np.array([1, 0, 1]), np.array([1, 0, 0]), None, (1.0, 0.0, 0.0), None, id="Valid_YZ_Plane_X1_Const_Default"),
        pytest.param(np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1]), 1, (1.0, 1.0, 1.0), None, id="Valid_XplusYplusZ_Const1"),
        pytest.param(np.array([6, 0, 0]), np.array([0, 4, 0]), np.array([0, 0, 3]), 12, (2.0, 3.0, 4.0), None, id="Valid_2x3y4z_Const12"),
        pytest.param(np.array([-1, -1, -1]), np.array([-1, -2, 0]), np.array([-2, -1, 0]), -3, (1.0, 1.0, 1.0), None, id="Valid_NegativeCoords_ConstNeg3"),
        pytest.param(np.array([0.5, 0.5, 0.5]), np.array([1.0, 0.5, 0.0]), np.array([0.0, 1.0, 0.5]), 1.5, (1.0, 1.0, 1.0), None, id="Valid_FloatCoords_Const1_5"),
        pytest.param(np.array([1e5, 0, 0]), np.array([0, 1e5, 0]), np.array([0, 0, 1e5]), 1e5, (1.0, 1.0, 1.0), None, id="Valid_LargeCoords_Const1e5"),
        pytest.param(np.array([1, 1, 1]), np.array([1, 2, 0]), np.array([2, 1, 0]), 3, (1.0, 1.0, 1.0), None, id="Valid_NonUnitConstant"),
        pytest.param(np.array([1, -1, 0]), np.array([0, 1, -1]), np.array([-1, 0, 1]), 0, (1.0, 1.0, 1.0), None, id="Valid_PassesThroughOrigin_Const0"),
        pytest.param(np.array([1, -1, 0]), np.array([0, 1, -1]), np.array([-1, 0, 1]), 1, None, ValueError, id="InValid_PassesThroughOrigin_Const1"),
        pytest.param(np.array([1, -1, 0]), np.array([0, 1, -1]), np.array([-1, 0, 1]), None, (1.0, 1.0, 1.0), None, id="Valid_PassesThroughOrigin_Const_Default"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([2, 0, 0]), 1, None, ValueError, id="Invalid_Collinear_XAxis"),
        pytest.param(np.array([1, 1, 1]), np.array([2, 2, 2]), np.array([3, 3, 3]), 1, None, ValueError, id="Invalid_Collinear_Diagonal"),
        pytest.param(np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([1, 0, 0]), 1, None, ValueError, id="Invalid_TwoCoincidentPoints"),
        pytest.param(np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0]), 1, None, ValueError, id="Invalid_AllCoincidentPoints"),
        pytest.param(np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([2, 1e-15, 0]), 1, None, ValueError, id="Invalid_AlmostCollinear"),
    ]
)
def test_plane_get_ABCD(point1, point2, point3, constant, expected_result, expected_exc):
    """
    Test cases for plane_get_ABCD function.
    """
    if expected_exc is None:
        result = plane_get_ABCD(point1, point2, point3, constant)
        assert close(np.array(result), np.array(expected_result)), f"Mismatch in A, B, C coefficients: {result} != {expected_result}"
    else:
        with pytest.raises(expected_exc):
            plane_get_ABCD(point1, point2, point3, constant)