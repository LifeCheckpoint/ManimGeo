import numpy as np
import pytest
from manimgeo.components import *

def test_point_hash_and_equality():
    # 创建两个内容相同的点实例
    p1 = Point.Free(np.array([1, 2, 0]), name="PointA")
    p2 = Point.Free(np.array([1, 2, 0]), name="PointB")

    # 创建一个引用
    p3 = p1

    # 验证不同实例的哈希值不同
    assert hash(p1) != hash(p2)
    # 验证不同实例不相等
    assert p1 != p2

    # 验证相同实例的哈希值相同
    assert hash(p1) == hash(p3)
    # 验证相同实例相等
    assert p1 == p3

    # 将点实例作为字典的键
    point_dict = {p1: "value1", p2: "value2"} # type: ignore
    assert len(point_dict) == 2
    assert point_dict[p1] == "value1"
    assert point_dict[p2] == "value2"

    # 将点实例作为集合的元素
    point_set = {p1, p2, p3} # type: ignore
    assert len(point_set) == 2 # p3 是 p1 的引用，所以集合中只有两个元素
    assert p1 in point_set
    assert p2 in point_set
    assert p3 in point_set