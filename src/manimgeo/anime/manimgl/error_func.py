from manimgeo.components.base import BaseGeometry
from manimlib import Mobject

from typing import Dict, Callable


class ErrorFunctionManimGL:
    # on_error_func

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