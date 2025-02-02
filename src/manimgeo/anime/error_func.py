from manimgeo.components.base import BaseGeometry
from typing import Dict, Callable

class ErrorFunctionManimGL:
    """ManimGL 几何对象错误处理"""
    from manimlib import Mobject

    @staticmethod
    def set_visible_by_state(state_info: Dict, obj: BaseGeometry, mobj: Mobject):
        match state_info["state"]:
            case "Init":
                return
            case "Normal" | "Restore":
                mobj.set_stroke(opacity=1)
            case "Error":
                mobj.set_stroke(opacity=0)

    @staticmethod
    def func_by_state(state_info: Dict, obj: BaseGeometry, mobj: Mobject, func: Callable):
        on_error = state_info["state"] == "Error"
        func(on_error, obj, mobj)

class ErrorFunctionJAnim:
    """JAnim 几何对象错误处理"""
    from janim.imports import VItem

    @staticmethod
    def set_visible_by_state(state_info: Dict, obj: BaseGeometry, vitem: VItem):
        match state_info["state"]:
            case "Init":
                return
            case "Normal" | "Restore":
                vitem.stroke.set(alpha=1)
            case "Error":
                vitem.stroke.set(alpha=0)

    @staticmethod
    def func_by_state(state_info: Dict, obj: BaseGeometry, vitem: VItem, func: Callable):
        on_error = state_info["state"] == "Error"
        func(on_error, obj, vitem)