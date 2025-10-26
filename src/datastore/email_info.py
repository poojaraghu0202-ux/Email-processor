from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enums.email_enums import EmailProviderType
import json

Base = declarative_base()

class Email(Base):
    """Email model"""
    __tablename__ = 'email_info'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_id = Column(String(255), unique=True, nullable=False, index=True)
    provider_type = Column(Integer, nullable=False, default=EmailProviderType.GMAIL.value)
    from_address = Column(String(500), nullable=False, index=True)
    to_address = Column(Text)
    subject = Column(Text, index=True)
    received_date = Column(DateTime, nullable=False, index=True)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for rule processing"""
        return {
            'id': self.provider_id,
            'from': self.from_address,
            'to': self.to_address,
            'subject': self.subject or '',
            'received_date': self.received_date,
            'is_read': self.is_read
        }
    @property
    def provider_type_enum(self) -> EmailProviderType:
        """Get provider type as enum"""
        return EmailProviderType(self.provider_type)
    
    @provider_type_enum.setter
    def provider_type_enum(self, value: EmailProviderType):
        """Set provider type from enum"""
        self.provider_type = value.value
    
    
    def __repr__(self):
        return f"<Email(id={self.id}, from={self.from_address}, subject={self.subject[:30]})>"