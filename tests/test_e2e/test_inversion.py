import numpy as np
from manimgeo.components import *
from manimgeo.utils.utils import print_dependencies

def test_inversion():
    # 使用两点构造法创建反演圆（圆心O，半径2）
    O = Point.Free(np.array([0, 0, 0]), "O")
    R = Point.Free(np.array([2, 0, 0]), "R")
    inversion_circle = Circle.PP(O, R, name="InversionCircle")

    # 构造点P并计算反演点
    P = Point.Free(np.array([3, 0, 0]), "P")
    Q = Point.InversionPCir(P, inversion_circle, name="Q")

    # 打印依赖关系
    print("Dependencies of O:")
    print_dependencies(O)
    print("")

    # 验证反演
    OQ = np.linalg.norm(O.coord - Q.coord)
    assert np.allclose(OQ, 4/3)