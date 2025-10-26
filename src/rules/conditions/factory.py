from typing import Any, Dict, Type
from .conditions import Condition
from .string_conditions import (
    ContainsCondition,
    DoesNotContainCondition,
    EqualsCondition,
    DoesNotEqualCondition
)
from .date_conditions import (
    LessThanDaysCondition,
    GreaterThanDaysCondition,
    LessThanMonthsCondition,
    GreaterThanMonthsCondition
)

class ConditionFactory:
    """Factory for creating condition instances"""
    
    _conditions: Dict[str, Type[Condition]] = {
        'contains': ContainsCondition,
        'does_not_contain': DoesNotContainCondition,
        'equals': EqualsCondition,
        'does_not_equal': DoesNotEqualCondition,
        'less_than_days': LessThanDaysCondition,
        'greater_than_days': GreaterThanDaysCondition,
        'less_than_months': LessThanMonthsCondition,
        'greater_than_months': GreaterThanMonthsCondition,
    }
    
    @classmethod
    def create(cls, predicate: str, field: str, value: Any) -> Condition:
        """Create a condition instance"""
        condition_class = cls._conditions.get(predicate.lower())
        if not condition_class:
            raise ValueError(f"Unsupported predicate: {predicate}")
        return condition_class(field, value)
    
    @classmethod
    def register_condition(cls, name: str, condition_class: Type[Condition]):
        """Register a new condition type"""
        cls._conditions[name.lower()] = condition_class
    
    @classmethod
    def get_available_predicates(cls) -> list:
        """Get list of available predicates"""
        return list(cls._conditions.keys())
