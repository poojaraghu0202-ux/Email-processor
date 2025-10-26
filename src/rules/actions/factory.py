from typing import Dict, Type, Any
from .action import Action
from .mark_actions import MarkAsReadAction, MarkAsUnreadAction
from .move_actions import MoveMessageAction

class ActionFactory:
    """Factory for creating action instances"""
    
    _actions: Dict[str, Type[Action]] = {
        'mark_as_read': MarkAsReadAction,
        'mark_as_unread': MarkAsUnreadAction,
        'move_message': MoveMessageAction,
    }
    
    @classmethod
    def create(cls, action_type: str, parameters: Dict[str, Any] = None) -> Action:
        """Create an action instance"""
        action_class = cls._actions.get(action_type.lower())
        if not action_class:
            raise ValueError(f"Unsupported action: {action_type}")
        return action_class(parameters)
    
    @classmethod
    def register_action(cls, name: str, action_class: Type[Action]):
        """Register a new action type"""
        cls._actions[name.lower()] = action_class
    
    @classmethod
    def get_available_actions(cls) -> list:
        """Get list of available actions"""
        return list(cls._actions.keys())
