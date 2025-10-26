from abc import ABC, abstractmethod
from typing import Any, Dict

class Action(ABC):
    """Abstract base class for all actions"""
    
    def __init__(self, parameters: Dict[str, Any] = None):
        self.parameters = parameters or {}
    
    @abstractmethod
    def execute(self, email_provider: Any, email: Dict) -> bool:
        """Execute action on email"""
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}(parameters={self.parameters})"