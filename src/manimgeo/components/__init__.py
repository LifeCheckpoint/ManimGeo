from typing import Protocol

class DependentObject(Protocol):
    """依赖更新协议"""
    def update(self) -> None:
        ...
    
    def add_dependent(self, obj: 'DependentObject') -> None:
        ...