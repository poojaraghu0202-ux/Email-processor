from typing import Any, Dict
from .action import Action
from utils.logger import setup_logger

logger = setup_logger(__name__)

class MarkAsReadAction(Action):
    """Mark email as read"""
    
    def execute(self, email_provider: Any, email: Dict) -> bool:
        try:
            result = email_provider.mark_as_read(email['id'])
            if result:
                logger.info(f"✓ Marked as read: {email['subject'][:50]}")
            return result
        except Exception as e:
            logger.error(f"Failed to mark as read: {str(e)}")
            return False


class MarkAsUnreadAction(Action):
    """Mark email as unread"""
    
    def execute(self, email_provider: Any, email: Dict) -> bool:
        try:
            result = email_provider.mark_as_unread(email['id'])
            if result:
                logger.info(f"✓ Marked as unread: {email['subject'][:50]}")
            return result
        except Exception as e:
            logger.error(f"Failed to mark as unread: {str(e)}")
            return False