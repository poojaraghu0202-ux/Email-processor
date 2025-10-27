import pytest
from rules.conditions.factory import ConditionFactory
from rules.conditions.string_conditions import ContainsCondition
from rules.conditions.date_conditions import LessThanDaysCondition


class TestConditionFactory:
    """Test ConditionFactory"""
    
    def test_create_contains_condition(self, condition_factory):
        """Test creating ContainsCondition"""
        condition = condition_factory.create('contains', 'from', 'test@test.com')
        assert isinstance(condition, ContainsCondition)
        assert condition.field == 'from'
        assert condition.value == 'test@test.com'
    
    def test_create_date_condition(self, condition_factory):
        """Test creating date condition"""
        condition = condition_factory.create('less_than_days', 'received_date', 7)
        assert isinstance(condition, LessThanDaysCondition)
        assert condition.field == 'received_date'
        assert condition.value == 7
    
    def test_create_unsupported_predicate(self, condition_factory):
        """Test creating condition with unsupported predicate"""
        with pytest.raises(ValueError, match="Unsupported predicate"):
            condition_factory.create('unsupported_predicate', 'field', 'value')
    
    def test_get_available_predicates(self, condition_factory):
        """Test getting list of available predicates"""
        predicates = condition_factory.get_available_predicates()
        assert 'contains' in predicates
        assert 'equals' in predicates
        assert 'less_than_days' in predicates
        assert len(predicates) >= 8
    
    def test_register_custom_condition(self, condition_factory):
        """Test registering custom condition"""
        from rules.conditions.conditions import Condition
        
        class CustomCondition(Condition):
            def evaluate(self, email):
                return True
        
        condition_factory.register_condition('custom', CustomCondition)
        condition = condition_factory.create('custom', 'field', 'value')
        assert isinstance(condition, CustomCondition)