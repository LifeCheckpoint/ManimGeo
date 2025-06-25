from __future__ import annotations

from pydantic import Field
from typing import cast

from ..base import GeometryAdapter
from .args import *

class MultipleAdapter(GeometryAdapter[MultipleConstructArgs]):
    geometry_objects = Field(default_factory=list, description="计算多个几何对象", init=False)

    def __call__(self):
        """
        多几何对象具体计算

        具体的参数更新是由下游的几何对象负责
        """

        match self.construct_type:
            case "Multiple":
                args = cast(MultipleArgs, self.args)
                self.geometry_objects = args.geometry_objects

            case "FilteredMultiple":
                args = cast(FilteredMultipleArgs, self.args)
                self.geometry_objects = [obj for obj, keep in zip(args.geometry_objects, args.filter_func(args.geometry_objects)) if keep]

            case "FilteredMultipleMono":
                args = cast(FilteredMultipleMonoArgs, self.args)
                self.geometry_objects = [obj for obj in args.geometry_objects if args.filter_func(obj)]

            case _:
                raise NotImplementedError(f"不支持的构造方式: {self.construct_type}")