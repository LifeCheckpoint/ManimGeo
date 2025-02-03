from manimgeo.components.base import BaseGeometry
from typing import Dict, Callable, Any, Literal

class StateManager:
    states: Dict[BaseGeometry, Dict]
    manage_type: str
    strategy_func: Callable[[Dict, BaseGeometry, Any], None]

    def __init__(self, manage_type: Literal["manimgl"], strategy_func: Callable[[str, BaseGeometry, Any], None]):
        """
        状态管理器

        `manage_type`: 管理对象归属
        `strategy_func`: 策略函数
         - `Dict`: 当前状态信息 Dict
         - `BaseGeometry`: 几何对象
         - `Any`: 其它参数
        """
        self.states = {}
        self.manage_type = manage_type
        self.strategy_func = strategy_func

    def set_strategy_func(self, strategy_func: Callable[[str, BaseGeometry, Any], None]):
        self.strategy_func = strategy_func

    def update(self, obj: BaseGeometry, target_obj: Any):
        """
        更新 obj 的状态信息，并向策略函数传递
        """
        if obj not in self.states.keys():
            self.states[obj] = {"state": "Init", "count": 0}
        
        if not obj.on_error and self.states[obj] != "Error":
            self.states[obj] = {"state": "Normal", "count": self.states[obj]["count"] + 1}

        if not obj.on_error and self.states[obj] == "Error":
            self.states[obj] = {"state": "Restore", "count": self.states[obj]["count"] + 1}

        if obj.on_error:
            self.states[obj] = {"state": "Error", "count": self.states[obj]["count"] + 1}

        # 传递策略
        match self.manage_type:
            case "manimgl" | "janim":
                self.strategy_func(self.states[obj], obj, target_obj)

            case _:
                raise ValueError(f"{self.manage_type} is not a valid managing target")