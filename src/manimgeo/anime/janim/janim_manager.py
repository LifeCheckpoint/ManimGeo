from manimgeo.components import *
from manimgeo.anime.manager import GeoManager
from manimgeo.anime.state import StateManager
from manimgeo.anime.error_func import ErrorFunctionJAnim as JAnimError

from janim.imports import VItem
from typing import Sequence, Callable

def dim_23(x: np.ndarray) -> np.ndarray:
    return np.append(x, 0)

class GeoJAnimManager(GeoManager):
    """管理 JAnim Component 和几何对象之间的自动映射"""
    on_error_exec: Union[None, Literal["vis", "stay"], Callable[[bool, BaseGeometry, VItem], None]]
    state_manager = StateManager("janim", JAnimError.set_visible_by_state)

    def __init__(self):
        super().__init__()
        self.on_error_exec = "vis"