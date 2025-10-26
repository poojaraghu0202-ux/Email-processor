from typing import Any, Dict
from datetime import datetime, timedelta
from .conditions import Condition
from utils.logger import setup_logger

logger = setup_logger(__name__)

class LessThanDaysCondition(Condition):
    """Check if email received less than N days ago"""
    
    def evaluate(self, email: Dict[str, Any]) -> bool:
        try:
            email_date = email.get('received_date')
            if isinstance(email_date, str):
                email_date = datetime.fromisoformat(email_date)
            
            days_ago = datetime.now(email_date.tzinfo) - timedelta(days=int(self.value))
            result = email_date > days_ago
            return result
        except Exception as e:
            logger.error(f"Error evaluating LessThanDaysCondition: {str(e)}")
            return False


class GreaterThanDaysCondition(Condition):
    """Check if email received more than N days ago"""
    
    def evaluate(self, email: Dict[str, Any]) -> bool:
        try:
            email_date = email.get('received_date')
            if isinstance(email_date, str):
                email_date = datetime.fromisoformat(email_date)
            
            days_ago = datetime.now(email_date.tzinfo) - timedelta(days=int(self.value))
            result = email_date < days_ago
            return result
        except Exception as e:
            logger.error(f"Error evaluating GreaterThanDaysCondition: {str(e)}")
            return False


class LessThanMonthsCondition(Condition):
    """Check if email received less than N months ago"""
    
    def evaluate(self, email: Dict[str, Any]) -> bool:
        try:
            email_date = email.get('received_date')
            if isinstance(email_date, str):
                email_date = datetime.fromisoformat(email_date)
            
            months_ago = datetime.now(email_date.tzinfo) - timedelta(days=int(self.value) * 30)
            result = email_date > months_ago
            return result
        except Exception as e:
            logger.error(f"Error evaluating LessThanMonthsCondition: {str(e)}")
            return False


class GreaterThanMonthsCondition(Condition):
    """Check if email received more than N months ago"""
    
    def evaluate(self, email: Dict[str, Any]) -> bool:
        try:
            email_date = email.get('received_date')
            if isinstance(email_date, str):
                email_date = datetime.fromisoformat(email_date)
            
            months_ago = datetime.now(email_date.tzinfo) - timedelta(days=int(self.value) * 30)
            result = email_date < months_ago
            return result
        except Exception as e:
            logger.error(f"Error evaluating GreaterThanMonthsCondition: {str(e)}")
            return False