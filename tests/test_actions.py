import pytest
from src.rules.actions.mark_actions import MarkAsReadAction, MarkAsUnreadAction
from src.rules.actions.move_actions import MoveMessageAction
from src.utils import logger
from tests.conftest import sample_email 
from tests.conftest import mock_gmail_provider


class TestActions:
    """Test action implementations"""
    
    def test_mark_as_read_action(self, mock_gmail_provider, sample_email):
        """Test MarkAsReadAction execution"""
        action = MarkAsReadAction()
        result = action.execute(mock_gmail_provider, sample_email)
       
        assert result is True
        mock_gmail_provider.mark_as_read.assert_called_once_with('test_email_123')
    
    def test_mark_as_unread_action(self, mock_gmail_provider, sample_email):
        """Test MarkAsUnreadAction execution"""
        action = MarkAsUnreadAction()
        result = action.execute(mock_gmail_provider, sample_email)
        
        assert result is True
        mock_gmail_provider.mark_as_unread.assert_called_once_with('test_email_123')
    
    def test_move_message_action(self, mock_gmail_provider, sample_email):
        """Test MoveMessageAction execution"""
        action = MoveMessageAction({'destination': 'Archive'})
        result = action.execute(mock_gmail_provider, sample_email)
        
        assert result is True
        mock_gmail_provider.move_email.assert_called_once_with('test_email_123', 'Archive')
    
    def test_move_message_action_no_destination(self, mock_gmail_provider, sample_email):
        """Test MoveMessageAction without destination parameter"""
        action = MoveMessageAction({})
        result = action.execute(mock_gmail_provider, sample_email)
        
        assert result is False
    
    def test_action_failure(self, mock_gmail_provider, sample_email):
        """Test action when provider fails"""
        mock_gmail_provider.mark_as_read.return_value = False
        action = MarkAsReadAction()
        result = action.execute(mock_gmail_provider, sample_email)
        
        assert result is False