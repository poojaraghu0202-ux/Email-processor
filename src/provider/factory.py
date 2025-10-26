from .email_provider import EmailProvider
from .gmail_provider import GmailProvider


class EmailProviderFactory:
    """Factory for creating email provider instances"""
    
    _providers = {
        'gmail': GmailProvider,
        'zoho': None,  # Future implementation
        'outlook': None,  # Future implementation
    }
    
    @classmethod
    def create(cls, provider_type: str) -> EmailProvider:
        provider_class = cls._providers.get(provider_type.lower())
        if not provider_class:
            raise ValueError(f"Unsupported provider: {provider_type}")
        return provider_class()
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """Register a new email provider"""
        cls._providers[name.lower()] = provider_class