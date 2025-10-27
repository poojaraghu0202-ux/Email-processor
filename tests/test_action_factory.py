import pytest
from rules.actions.factory import ActionFactory
from rules.actions.mark_actions import MarkAsReadAction


class TestActionFactory:
    """Test ActionFactory"""
    
    def test_create_mark_as_read_action(self, action_factory):
        """Test creating MarkAsReadAction"""
        action = action_factory.create('mark_as_read')
        assert isinstance(action, MarkAsReadAction)
    
    def test_create_move_action_with_parameters(self, action_factory):
        """Test creating action with parameters"""
        action = action_factory.create('move_message', {'destination': 'Archive'})
        assert action.parameters['destination'] == 'Archive'
    
    def test_create_unsupported_action(self, action_factory):
        """Test creating unsupported action"""
        with pytest.raises(ValueError, match="Unsupported action"):
            action_factory.create('unsupported_action')
    
    def test_get_available_actions(self, action_factory):
        """Test getting available actions"""
        actions = action_factory.get_available_actions()
        assert 'mark_as_read' in actions
        assert 'mark_as_unread' in actions
        assert 'move_message' in actions