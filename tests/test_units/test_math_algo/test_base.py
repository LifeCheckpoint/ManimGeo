import numpy as np
import pytest

# 配置容差参数
from manimgeo.utils.config import GeoConfig
cfg = GeoConfig()

from manimgeo.math import *

@pytest.mark.parametrize(
    "a, b, expected",
    [
        pytest.param(0.0, 0.0, True, id="scalar_equal_zero"),
        pytest.param(1.2345, 1.2345, True, id="scalar_equal_nonzero"),
        pytest.param(-3.14159, -3.14159, True, id="scalar_equal_negative"),
        pytest.param(1.0, 1.0 + 0.5 * cfg.atol, True, id="scalar_atol_pass"),
        pytest.param(-2.0, -2.0 - 0.5 * cfg.atol, True, id="scalar_atol_pass_negative"),
        pytest.param(100.0, 100.0 * (1 + 0.5 * cfg.rtol), True, id="scalar_rtol_pass"),
        pytest.param(1e6, 1e6 * (1 - 0.5 * cfg.rtol), True, id="scalar_rtol_pass_large"),
        pytest.param(1.0, 1.0 + 2 * cfg.atol, True, id="scalar_atol_fail"),
        pytest.param(100.0, 100.0 * (1 + 2 * cfg.rtol), False, id="scalar_rtol_fail"),
        pytest.param(1e-10, 2e-10, True, id="scalar_mixed_tol_pass_small"),
        pytest.param(1e-10, 1.1e-10, True, id="scalar_mixed_tol_pass_small2"),
        pytest.param(1e9, 1e9 + 1000, True, id="scalar_mixed_tol_pass_large"),
        pytest.param(1e9, 1e9 + 20000, True, id="scalar_mixed_tol_fail_large"),
        pytest.param(np.inf, np.inf, True, id="scalar_inf_equal"),
        pytest.param(-np.inf, -np.inf, True, id="scalar_neg_inf_equal"),
        pytest.param(np.inf, -np.inf, False, id="scalar_inf_sign_mismatch"),
        pytest.param(np.inf, 1e100, False, id="scalar_inf_finite"),
        pytest.param(np.nan, np.nan, False, id="scalar_nan"),
        pytest.param(0.0, np.nan, False, id="scalar_zero_nan"),
        pytest.param(
            np.array([1.0, 2.0, 3.0]), 
            np.array([1.0, 2.0, 3.0]), 
            True, 
            id="array_equal"
        ),
        pytest.param(
            np.array([0.1, 0.2]), 
            np.array([0.1 + 0.5*cfg.atol, 0.2 - 0.5*cfg.atol]), 
            True, 
            id="array_atol_pass"
        ),
        pytest.param(
            np.array([1000.0, 2000.0]), 
            np.array([
                1000.0 * (1 + 0.5*cfg.rtol), 
                2000.0 * (1 - 0.5*cfg.rtol)
            ]), 
            True, 
            id="array_rtol_pass"
        ),
        pytest.param(
            np.array([1.0, 2.0]), 
            np.array([1.0 + 2*cfg.atol, 2.0]), 
            True, 
            id="array_one_element_fail"
        ),
        pytest.param(
            np.array([100.0, 200.0]), 
            np.array([
                100.0 * (1 + 2*cfg.rtol), 
                200.0 * (1 - 2*cfg.rtol)
            ]), 
            False, 
            id="array_all_elements_fail"
        ),
        pytest.param(
            np.array([np.inf, -np.inf]), 
            np.array([np.inf, -np.inf]), 
            True, 
            id="array_inf_equal"
        ),
        pytest.param(
            np.array([np.nan, 1.0]), 
            np.array([np.nan, 1.0]), 
            False,  # 因为包含 NaN
            id="array_with_nan"
        ),
        pytest.param(
            np.array([1.0, 2.0]), 
            np.array([1.0, 2.0, 3.0]), 
            ValueError, 
            id="array_shape_mismatch"
        ),
        pytest.param(
            1.0, 
            np.array([1.0]), 
            TypeError, 
            id="type_mismatch_scalar_array"
        ),
        pytest.param(
            np.array([1.0]), 
            1.0, 
            TypeError, 
            id="type_mismatch_array_scalar"
        ),
        pytest.param(
            np.array([1, 2], dtype=int), 
            np.array([1.0, 2.0], dtype=float), 
            True,  # 数值相同，类型不同但都是数字
            id="array_different_numeric_types"
        ),
        pytest.param(
            "hello", 
            "world", 
            TypeError, 
            id="non_numeric_strings"
        ),
        pytest.param(
            [1, 2, 3], 
            [1, 2, 3], 
            TypeError, 
            id="non_numeric_lists"
        ),
    ]
)
def test_close(a, b, expected):
    if expected is True or expected is False:
        result = close(a, b)
        assert result == expected, f"Expected {expected}, got {result} for inputs {a} and {b}"
    elif issubclass(expected, Exception):
        with pytest.raises(expected):
            close(a, b)
