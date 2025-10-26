from typing import Any, Dict
from .conditions import Condition

class ContainsCondition(Condition):
    """Check if field contains value (case-insensitive)"""
    
    def evaluate(self, email: Dict[str, Any]) -> bool:
        field_value = str(email.get(self.field, '')).lower()
        search_value = str(self.value).lower()
        return search_value in field_value


class DoesNotContainCondition(Condition):
    """Check if field does not contain value (case-insensitive)"""
    
    def evaluate(self, email: Dict[str, Any]) -> bool:
        field_value = str(email.get(self.field, '')).lower()
        search_value = str(self.value).lower()
        return search_value not in field_value


class EqualsCondition(Condition):
    """Check if field equals value (case-insensitive)"""
    
    def evaluate(self, email: Dict[str, Any]) -> bool:
        field_value = str(email.get(self.field, '')).lower().strip()
        search_value = str(self.value).lower().strip()
        return field_value == search_value


class DoesNotEqualCondition(Condition):
    """Check if field does not equal value (case-insensitive)"""
    
    def evaluate(self, email: Dict[str, Any]) -> bool:
        field_value = str(email.get(self.field, '')).lower().strip()
        search_value = str(self.value).lower().strip()
        return field_value != search_value