import numpy as np
import pytest

from manimgeo.components import *

def test_PP():
    # 通过两点构造向量
    start = Point.Free(np.array([1, 2, 0]))
    end = Point.Free(np.array([4, 6, 0]))
    vector = Vector.PP(start=start, end=end)
    assert np.allclose(vector.vec, np.array([3, 4, 0]))

def test_L():
    # 通过线段构造向量
    start = Point.Free(np.array([1, 2, 0]))
    end = Point.Free(np.array([4, 6, 0]))
    line = LineSegment.PP(start=start, end=end)
    vector = Vector.L(line=line)
    assert np.allclose(vector.vec, np.array([3, 4, 0]))

def test_N():
    # （数值）构造向量
    vec = np.array([3, 4, 0])
    vector = Vector.N(vec=vec)
    assert np.allclose(vector.vec, vec)

def test_NPP():
    # 通过两点（数值）构造向量
    start = np.array([1, 2, 0])
    end = np.array([4, 6, 0])
    vector = Vector.NPP(start=start, end=end)
    assert np.allclose(vector.vec, np.array([3, 4, 0]))

def test_NNormDirection():
    # 通过模长与方向构造向量
    norm = 5
    direction = np.array([3, 4, 0])
    vector = Vector.NNormDirection(norm=norm, direction=direction)
    expected_vec = (norm / np.linalg.norm(direction)) * direction
    assert np.allclose(vector.vec, expected_vec)

def test_Add():
    # 向量加法测试
    vec1 = Vector.N(np.array([1, 2, 0]))
    vec2 = Vector.N(np.array([3, 4, 0]))
    result = vec1 + vec2
    assert np.allclose(result.vec, np.array([4, 6, 0]))

def test_Sub():
    # 向量减法测试
    vec1 = Vector.N(np.array([5, 6, 0]))
    vec2 = Vector.N(np.array([3, 4, 0]))
    result = vec1 - vec2
    assert np.allclose(result.vec, np.array([2, 2, 0]))

def test_Scale():
    # 向量缩放测试
    vec = Vector.N(np.array([1, 2, 0]))
    scale_factor = 3
    result = vec * scale_factor
    assert np.allclose(result.vec, np.array([3, 6, 0]))