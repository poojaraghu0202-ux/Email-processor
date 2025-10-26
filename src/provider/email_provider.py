from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class EmailProvider(ABC):
    """Abstract base class for all email providers"""
    
    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the email service"""
        pass
    
    @abstractmethod
    def fetch_emails(self, folder: str = "INBOX", limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch emails from specified folder"""
        pass
    
    @abstractmethod
    def mark_as_read(self, email_id: str) -> bool:
        """Mark email as read"""
        pass
    
    @abstractmethod
    def mark_as_unread(self, email_id: str) -> bool:
        """Mark email as unread"""
        pass
    
    @abstractmethod
    def move_email(self, email_id: str, destination: str) -> bool:
        """Move email to destination folder"""
        pass
    