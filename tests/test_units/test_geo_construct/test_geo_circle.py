import numpy as np
import pytest
from manimgeo.components import *
from manimgeo.math import close

def test_cnr_construction():
    center = Point.Free(coord=np.array([1.0, 2.0, 3.0]))
    normal = Vector.N(vec=np.array([0.0, 0.0, 1.0]))
    radius = 5.0
    circle = Circle.CNR(center, normal, radius)

    assert close(circle.center, center.coord)
    assert close(circle.normal, normal.vec)
    assert np.isclose(circle.radius, radius)


def test_pr_construction_with_normal():
    center = Point.Free(coord=np.array([1.0, 1.0, 1.0]))
    radius = 2.0
    normal = Vector.N(vec=np.array([0.0, 1.0, 0.0])) # YZ plane
    circle = Circle.PR(center, radius, normal=normal)

    assert close(circle.center, center.coord)
    assert np.isclose(circle.radius, radius)
    assert close(circle.normal, normal.vec)

def test_pr_construction_without_normal():
    center = Point.Free(coord=np.array([1.0, 1.0, 1.0]))
    radius = 2.0
    circle = Circle.PR(center, radius) # Should default to [0,0,1]

    assert close(circle.center, center.coord)
    assert np.isclose(circle.radius, radius)
    assert close(circle.normal, np.array([0.0, 0.0, 1.0]))

def test_ppp_construction_normal():
    p1 = Point.Free(coord=np.array([1.0, 0.0, 0.0]))
    p2 = Point.Free(coord=np.array([0.0, 1.0, 0.0]))
    p3 = Point.Free(coord=np.array([0.0, 0.0, 0.0])) # Origin
    circle = Circle.PPP(p1, p2, p3)

    # The plane formed by (1,0,0), (0,1,0), (0,0,0) is the XY plane, normal should be [0,0,1] or [-0,-0,-1]
    expected_normal = np.array([0.0, 0.0, 1.0])
    # Allow for normal to be in opposite direction
    assert close(circle.normal, expected_normal) or close(circle.normal, -expected_normal)

def test_inverse_cir_cir_normal():
    # Base circle in XY plane
    base_circle = Circle.CNR(Point.Free(np.array([0.0, 0.0, 0.0])), Vector.N(np.array([0.0, 0.0, 1.0])), 1.0)
    # Circle to invert, also in XY plane
    circle_to_invert = Circle.CNR(Point.Free(np.array([2.0, 0.0, 0.0])), Vector.N(np.array([0.0, 0.0, 1.0])), 0.5)

    inverted_circle = Circle.InverseCirCir(circle_to_invert, base_circle)

    # The normal of the inverted circle should be the same as the original circle's normal
    assert close(inverted_circle.normal, circle_to_invert.normal)

def test_translation_cir_v_normal():
    original_circle = Circle.CNR(Point.Free(np.array([0.0, 0.0, 0.0])), Vector.N(np.array([1.0, 1.0, 0.0])), 1.0)
    translation_vector = Vector.N(vec=np.array([10.0, 10.0, 10.0]))

    translated_circle = Circle.TranslationCirV(original_circle, translation_vector)

    # The normal of the translated circle should be the same as the original circle's normal
    assert close(translated_circle.normal, original_circle.normal)