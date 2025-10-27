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