from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json

Base = declarative_base()

class RuleExecution(Base):
    """Track rule executions"""
    __tablename__ = 'rule_executions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(String(255), nullable=False, index=True)
    rule_name = Column(String(255), nullable=False)
    matched = Column(Boolean, nullable=False)
    actions_executed = Column(Text)
    executed_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<RuleExecution(rule={self.rule_name}, email={self.email_id}, matched={self.matched})>"