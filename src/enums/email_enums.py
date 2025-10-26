from enum import IntEnum

class EmailProviderType(IntEnum):
    """Email provider types"""
    GMAIL = 1
    ZOHO = 2
    CUSTOM = 99
    
    @classmethod
    def from_string(cls, provider: str):
        """Convert string to enum"""
        mapping = {
            'gmail': cls.GMAIL,
            'zoho': cls.ZOHO
        }
        return mapping.get(provider.lower(), cls.CUSTOM)
    
    def to_string(self) -> str:
        """Convert enum to string"""
        mapping = {
            self.GMAIL: 'gmail',
            self.ZOHO: 'zoho',
            self.CUSTOM: 'custom'
        }
        return mapping.get(self, 'unknown')
    
    @classmethod
    def get_all_providers(cls):
        """Get list of all providers"""
        return [member for member in cls]
    
class EmailLabelType(IntEnum) :
    """Email label types"""
    INBOX = 1
    IMPORTANT = 2
    STARRED = 3
    SPAM = 4
    TRASH = 5
    CUSTOM = 99
    
    @classmethod
    def from_string(cls, label: str):
        """Convert string to enum"""
        mapping = {
            'inbox': cls.INBOX,
            'important': cls.IMPORTANT,
            'starred': cls.STARRED,
            'spam': cls.SPAM,
            'trash': cls.TRASH,
        }
        return mapping.get(label.lower(), cls.CUSTOM)
    
    def to_string(self) -> str:
        """Convert enum to string"""
        mapping = {
            self.INBOX: 'inbox',
            self.IMPORTANT: 'important',
            self.STARRED: 'starred',
            self.SPAM: 'spam',
            self.TRASH: 'trash',
            self.CUSTOM: 'custom',
        }
        return mapping.get(self, 'unknown')