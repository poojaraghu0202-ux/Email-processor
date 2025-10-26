from abc import ABC, abstractmethod
from typing import Any, Dict

class Condition(ABC):
    """Abstract base class for all conditions"""
    
    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value
    
    @abstractmethod
    def evaluate(self, email: Dict[str, Any]) -> bool:
        """Evaluate condition against email"""
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}(field={self.field}, value={self.value})"