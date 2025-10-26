from typing import Any, Dict
from .action import Action
from utils.logger import setup_logger

logger = setup_logger(__name__)

class MoveMessageAction(Action):
    """Move email to specified folder/label"""

    def execute(self, email_provider: Any, email: Dict) -> bool:
        try:
            destination = self.parameters.get('destination')
            if not destination:
                logger.error("Destination folder/label not specified for MoveMessageAction")
                return False

            # Skip if already in the destination
            current_labels = set(email.get('labels', []))
            dest_label_id = email_provider._get_label_id(destination)
            if dest_label_id in current_labels:
                logger.info(f"Email '{email['subject'][:50]}' is already in '{destination}', skipping move.")
                return True

            # Move email
            result = email_provider.move_email(email['id'], destination)
            if result:
                logger.info(f"✓ Moved to {destination}: {email['subject'][:50]}")
            return result

        except Exception as e:
            logger.error(f"Failed to move email: {str(e)}")
            return False
