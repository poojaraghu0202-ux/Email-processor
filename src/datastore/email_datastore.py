from typing import List, Optional
from enums.email_enums import EmailProviderType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import json

from .email_info import Base as EmailBase, Email
from .rule_execution import Base as RuleBase, RuleExecution
from config.settings import DATABASE_URL
from utils.logger import setup_logger

logger = setup_logger(__name__)

class EmailRepository:
    """Repository for email database operations"""
    
    def __init__(self, database_url: str = DATABASE_URL):
        self.engine = create_engine(database_url, echo=False)
        EmailBase.metadata.create_all(self.engine)
        RuleBase.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        logger.info(f"Database initialized at {database_url}")
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    def save_emails(self, emails: List[dict], provider_type: str = 'gmail') -> int:
        """Save emails to database"""
        session = self.get_session()
        new_count = 0
        
        try:
            for email_data in emails:
                existing = session.query(Email).filter_by(
                    provider_id=email_data['id']
                ).first()
                
                if existing:
                    existing.is_read = email_data['is_read']
                    existing.labels = json.dumps(email_data['labels'])
                    existing.updated_at = datetime.utcnow()
                else:
                    email = Email(
                        provider_id=email_data['id'],
                        provider_type_enum=EmailProviderType.from_string(provider_type),
                        from_address=email_data['from'],
                        to_address=email_data['to'],
                        subject=email_data['subject'],     
                        received_date=email_data['received_date'],
                        is_read=email_data['is_read']
                    
                    )
                    session.add(email)
                    new_count += 1
            
            session.commit()
            logger.info(f"Saved {new_count} new emails, updated {len(emails) - new_count}")
            return new_count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving emails: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_all_emails(self) -> List[Email]:
        """Get all emails from database"""
        session = self.get_session()
        try:
            return session.query(Email).order_by(Email.received_date.desc()).all()
        finally:
            session.close()
    
    def get_emails_for_processing(self, limit: Optional[int] = None) -> List[Email]:
        """Get emails that need rule processing"""
        session = self.get_session()
        try:
            query = session.query(Email).order_by(Email.received_date.desc())
            if limit:
                query = query.limit(limit)
            return query.all()
        finally:
            session.close()
    
    def log_rule_execution(self, email_id: str, rule_name: str, 
                          matched: bool, actions: List[str]):
        """Log a rule execution"""
        session = self.get_session()
        try:
            execution = RuleExecution(
                email_id=email_id,
                rule_name=rule_name,
                matched=matched,
                actions_executed=json.dumps(actions)
            )
            session.add(execution)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error logging rule execution: {str(e)}")
        finally:
            session.close()
    
    def get_rule_executions(self, email_id: str) -> List[RuleExecution]:
        """Get all rule executions for an email"""
        session = self.get_session()
        try:
            return session.query(RuleExecution).filter_by(email_id=email_id).all()
        finally:
            session.close()