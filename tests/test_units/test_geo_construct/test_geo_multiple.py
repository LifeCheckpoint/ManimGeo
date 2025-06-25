import numpy as np
import pytest
import numpy as np
from typing import List, cast

from manimgeo.components import *

def test_Multiple():
    p1 = Point.Free(np.array([1, 2, 3]))
    p2 = Point.Free(np.array([4, 5, 6]))
    p3 = Point.Free(np.array([7, 8, 9]))
    points = MultipleComponents.Multiple(
        geometry_objects=[p1, p2, p3],
        name="test_multiple"
    )
    assert isinstance(points, MultipleComponents)
    assert points.name == "test_multiple"
    assert len(points.geometry_objects) == 3
    getting_point = points.geometry_objects[1]
    getting_point = cast(Point, getting_point)
    assert np.allclose(getting_point.coord, np.array([4, 5, 6]))
    
    p2.set_coord(np.array([10, 11, 12]))
    assert np.allclose(getting_point.coord, np.array([10, 11, 12]))

def test_FilteredMultiple():
    p1 = Point.Free(np.array([1, 2, 3]))
    p2 = Point.Free(np.array([4, 5, 6]))
    p3 = Point.Free(np.array([7, 8, 9]))
    
    def filter_func(points: List[BaseGeometry]) -> List[bool]:
        return [True, False, True]
    
    points = MultipleComponents.FilteredMultiple(
        geometry_objects=[p1, p2, p3],
        filter_func=filter_func,
        name="test_filtered_multiple"
    )
    
    assert isinstance(points, MultipleComponents)
    assert points.name == "test_filtered_multiple"
    assert len(points.geometry_objects) == 2
    getting_point = points.geometry_objects[0]
    getting_point = cast(Point, getting_point)
    assert np.allclose(getting_point.coord, np.array([1, 2, 3]))

def test_FilteredMultipleMono():
    p1 = Point.Free(np.array([1, 2, 3]))
    p2 = Point.Free(np.array([4, 5, 6]))
    p3 = Point.Free(np.array([7, 8, 9]))
    
    def filter_func(point: BaseGeometry) -> bool:
        point = cast(Point, point)
        return point.coord[0] > 3
    
    points = MultipleComponents.FilteredMultipleMono(
        geometry_objects=[p1, p2, p3],
        filter_func=filter_func,
        name="test_filtered_multiple_mono"
    )
    
    assert isinstance(points, MultipleComponents)
    assert points.name == "test_filtered_multiple_mono"
    assert len(points.geometry_objects) == 2
    getting_point = points.geometry_objects[0]
    getting_point = cast(Point, getting_point)
    assert np.allclose(getting_point.coord, np.array([4, 5, 6]))

def test_Union():
    p1 = Point.Free(np.array([1, 2, 3]))
    p2 = Point.Free(np.array([4, 5, 6]))
    p3 = Point.Free(np.array([7, 8, 9]))
    
    points1 = MultipleComponents.Multiple(
        geometry_objects=[p1, p2],
        name="test_union_1"
    )
    points2 = MultipleComponents.Multiple(
        geometry_objects=[p2, p3],
        name="test_union_2"
    )
    
    union_points = MultipleComponents.Union(
        multiples=[points1, points2],
        name="test_union"
    )
    
    assert isinstance(union_points, MultipleComponents)
    assert union_points.name == "test_union"
    assert len(union_points.geometry_objects) == 3

def test_Intersection():
    p1 = Point.Free(np.array([1, 2, 3]))
    p2 = Point.Free(np.array([4, 5, 6]))
    p3 = Point.Free(np.array([7, 8, 9]))
    
    points1 = MultipleComponents.Multiple(
        geometry_objects=[p1, p2],
        name="test_intersection_1"
    )
    points2 = MultipleComponents.Multiple(
        geometry_objects=[p2, p3],
        name="test_intersection_2"
    )
    
    intersection_points = MultipleComponents.Intersection(
        multiples=[points1, points2],
        name="test_intersection"
    )
    
    assert isinstance(intersection_points, MultipleComponents)
    assert intersection_points.name == "test_intersection"
    assert len(intersection_points.geometry_objects) == 1
    getting_point = intersection_points.geometry_objects[0]
    getting_point = cast(Point, getting_point)
    assert np.allclose(getting_point.coord, np.array([4, 5, 6]))

def test_AddAndSub():
    p1 = Point.Free(np.array([1, 2, 3]))
    p2 = Point.Free(np.array([4, 5, 6]))
    p3 = Point.Free(np.array([7, 8, 9]))
    
    points1 = MultipleComponents.Multiple(
        geometry_objects=[p1, p2],
        name="test_add_sub_1"
    )
    points2 = MultipleComponents.Multiple(
        geometry_objects=[p2, p3],
        name="test_add_sub_2"
    )
    
    added_points = points1 + points2
    assert isinstance(added_points, MultipleComponents)
    assert len(added_points.geometry_objects) == 3
    
    subtracted_points = points1 - points2
    assert isinstance(subtracted_points, MultipleComponents)
    assert len(subtracted_points.geometry_objects) == 1
    getting_point = subtracted_points.geometry_objects[0]
    getting_point = cast(Point, getting_point)
    assert np.allclose(getting_point.coord, np.array([1, 2, 3]))