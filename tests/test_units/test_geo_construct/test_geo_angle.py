import numpy as np
import pytest

from manimgeo.components import *

def test_AngleN():
    # 测试通过角度值构造角
    angle_rad = Angle.N(np.pi / 2)
    assert np.isclose(angle_rad.angle, np.pi / 2)
    assert angle_rad.turn == "Counterclockwise"

    angle_deg = Angle.N(90, name="test_angle_deg")
    assert np.isclose(angle_deg.angle, 90)
    assert angle_deg.turn == "Counterclockwise"
    assert angle_deg.name == "test_angle_deg"

    angle_clockwise = Angle.N(np.pi / 4, turn="Clockwise")
    assert np.isclose(angle_clockwise.angle, np.pi / 4)
    assert angle_clockwise.turn == "Clockwise"

def test_AnglePPP():
    # 测试通过三点构造角
    p1 = Point.Free(np.array([1, 0, 0]))
    center = Point.Free(np.array([0, 0, 0]))
    p2 = Point.Free(np.array([0, 1, 0]))
    angle = Angle.PPP(p1, center, p2)
    assert np.isclose(angle.angle, np.pi / 2)
    assert angle.turn == "Counterclockwise"

    p3 = Point.Free(np.array([-1, 0, 0]))
    angle2 = Angle.PPP(p1, center, p3)
    assert np.isclose(angle2.angle, np.pi)

    # 测试顺时针方向
    angle3 = Angle.PPP(p2, center, p1)
    assert np.isclose(angle3.angle, np.pi / 2)

def test_AngleLL():
    # 测试通过两条线构造角
    line1 = InfinityLine.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([1, 0, 0]))) # x轴
    line2 = InfinityLine.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([0, 1, 0]))) # y轴
    angle = Angle.LL(line1, line2)
    assert np.isclose(angle.angle, np.pi / 2)
    assert angle.turn == "Counterclockwise"

    line3 = InfinityLine.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([1, 1, 0]))) # y=x
    angle2 = Angle.LL(line1, line3)
    assert np.isclose(angle2.angle, np.pi / 4)

def test_AngleLP():
    # 测试通过一条线和一个点构造角
    line = LineSegment.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([1, 0, 0])))
    point = Point.Free(np.array([1, 1, 0]))
    angle = Angle.LP(line, point)
    assert np.isclose(angle.angle, np.pi / 4)

    line2 = LineSegment.PP(Point.Free(np.array([0, 0, 0])), Point.Free(np.array([0, 1, 0])))
    point2 = Point.Free(np.array([1, 0, 0]))
    angle2 = Angle.LP(line2, point2)
    assert np.isclose(angle2.angle, np.pi / 2)

def test_AngleTurnA():
    # 测试反转角旋转方向
    angle1 = Angle.N(np.pi / 3, turn="Counterclockwise")
    turned_angle = Angle.TurnA(angle1)
    assert np.isclose(turned_angle.angle, 2 * np.pi - np.pi / 3)
    assert turned_angle.turn == "Clockwise"

    angle2 = Angle.N(np.pi / 6, turn="Clockwise")
    turned_angle2 = Angle.TurnA(angle2)
    assert np.isclose(turned_angle2.angle, 2 * np.pi - np.pi / 6)
    assert turned_angle2.turn == "Counterclockwise"

def test_AngleArithmetic():
    # 测试角度的加减乘
    angle1 = Angle.N(np.pi / 4)
    angle2 = Angle.N(np.pi / 2)

    # 加法
    sum_angle = angle1 + angle2
    assert np.isclose(sum_angle.angle, 3 * np.pi / 4)

    # 减法
    diff_angle = angle2 - angle1
    assert np.isclose(diff_angle.angle, np.pi / 4)

    # 乘法
    mul_angle = angle1 * 2
    assert np.isclose(mul_angle.angle, np.pi / 2)

    mul_angle2 = angle2 * 0.5
    assert np.isclose(mul_angle2.angle, np.pi / 4)