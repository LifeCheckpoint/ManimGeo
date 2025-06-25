import numpy as np
import pytest
from manimgeo.components import *
from manimgeo.math import close

def test_PP():
    line = LineSegment.PP(
        Point.Free(coord=np.array([0.0, 0.0, 0.0])),
        Point.Free(coord=np.array([1.0, 1.0, 1.0]))
    )
    assert close(line.start, np.array([0.0, 0.0, 0.0]))
    assert close(line.end, np.array([1.0, 1.0, 1.0]))
    assert close(line.length, np.sqrt(3))
    assert close(line.unit_direction, np.array([1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)]))

def test_TranslationLV():
    line_seg = LineSegment.PP(
        Point.Free(coord=np.array([0.0, 0.0, 0.0])),
        Point.Free(coord=np.array([1.0, 1.0, 1.0]))
    )
    translation_vector = Vector.N(vec=np.array([1.0, 0.0, 0.0]))

    trans_seg = LineSegment.TranslationLV(line_seg, translation_vector)
    trans_ray = Ray.TranslationLV(line_seg, translation_vector)
    trans_infinity = InfinityLine.TranslationLV(line_seg, translation_vector)

    assert isinstance(trans_seg, LineSegment)
    assert isinstance(trans_ray, Ray)
    assert isinstance(trans_infinity, InfinityLine)
    assert trans_seg.start[0] == 1.0
    assert trans_seg.end[0] == 2.0
    assert trans_ray.start[0] == 1.0
    assert trans_ray.end[0] == 2.0
    assert trans_infinity.start[0] == 1.0
    assert trans_infinity.end[0] == 2.0

def test_PV():
    line = LineSegment.PV(
        Point.Free(coord=np.array([0.0, 0.0, 0.0])),
        Vector.N(vec=np.array([1.0, 1.0, 1.0]))
    )
    assert close(line.start, np.array([0.0, 0.0, 0.0]))
    assert close(line.end, np.array([1.0, 1.0, 1.0]))
    assert close(line.length, np.sqrt(3))
    assert close(line.unit_direction, np.array([1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)]))

def test_VerticalPL():
    base_line = LineSegment.PP(
        Point.Free(coord=np.array([0.0, 0.0, 0.0])),
        Point.Free(coord=np.array([1.0, 1.0, 0.0]))
    )
    point = Point.Free(coord=np.array([0.5, 0.0, 0.0]))
    vertical_line = Ray.VerticalPL(point, base_line) 
    assert close(vertical_line.start, np.array([0.25, 0.25, 0.0]))
    assert close(vertical_line.unit_direction, np.array([1/np.sqrt(2), -1/np.sqrt(2), 0]))

def test_ParallelPL():
    base_line = LineSegment.PP(
        Point.Free(coord=np.array([0.0, 0.0, 0.0])),
        Point.Free(coord=np.array([1.0, 1.0, 0.0]))
    )
    point = Point.Free(coord=np.array([1.0, 0.0, 0.0]))
    parallel_line = Ray.ParallelPL(point, base_line)
    assert close(parallel_line.start, np.array([1.0, 0.0, 0.0]))
    assert close(parallel_line.unit_direction, np.array([1/np.sqrt(2), 1/np.sqrt(2), 0]))