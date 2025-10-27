import pytest
from src.rules.conditions.string_conditions import (
    ContainsCondition,
    DoesNotContainCondition,
    EqualsCondition,
    DoesNotEqualCondition
)


class TestStringConditions:
    """Test string-based conditions"""
    
    def test_contains_condition_matches(self, sample_email):
        """Test ContainsCondition when value is present"""
        condition = ContainsCondition('from', 'boss@company.com')
        assert condition.evaluate(sample_email) is True
    
    def test_contains_condition_case_insensitive(self, sample_email):
        """Test ContainsCondition is case-insensitive"""
        condition = ContainsCondition('from', 'BOSS')
        assert condition.evaluate(sample_email) is True
    
    def test_contains_condition_not_matches(self, sample_email):
        """Test ContainsCondition when value is absent"""
        condition = ContainsCondition('from', 'unknown@example.com')
        assert condition.evaluate(sample_email) is False
    
    def test_contains_condition_in_subject(self, sample_email):
        """Test ContainsCondition in subject field"""
        condition = ContainsCondition('subject', 'urgent')
        assert condition.evaluate(sample_email) is True
    
    def test_does_not_contain_condition_matches(self, sample_email):
        """Test DoesNotContainCondition when value is absent"""
        condition = DoesNotContainCondition('from', 'spam')
        assert condition.evaluate(sample_email) is True
    
    def test_does_not_contain_condition_not_matches(self, sample_email):
        """Test DoesNotContainCondition when value is present"""
        condition = DoesNotContainCondition('from', 'boss')
        assert condition.evaluate(sample_email) is False
    
    def test_equals_condition_matches(self, sample_email):
        """Test EqualsCondition exact match"""
        condition = EqualsCondition('from', 'boss@company.com')
        assert condition.evaluate(sample_email) is True
    
    def test_equals_condition_case_insensitive(self, sample_email):
        """Test EqualsCondition is case-insensitive"""
        condition = EqualsCondition('from', 'BOSS@COMPANY.COM')
        assert condition.evaluate(sample_email) is True
    
    def test_equals_condition_not_matches(self, sample_email):
        """Test EqualsCondition when not equal"""
        condition = EqualsCondition('from', 'other@company.com')
        assert condition.evaluate(sample_email) is False
    
    def test_does_not_equal_condition_matches(self, sample_email):
        """Test DoesNotEqualCondition when different"""
        condition = DoesNotEqualCondition('from', 'other@company.com')
        assert condition.evaluate(sample_email) is True
    
    def test_does_not_equal_condition_not_matches(self, sample_email):
        """Test DoesNotEqualCondition when same"""
        condition = DoesNotEqualCondition('from', 'boss@company.com')
        assert condition.evaluate(sample_email) is False
    
    def test_condition_with_missing_field(self):
        """Test condition when field doesn't exist"""
        email = {'from': 'test@test.com'}
        condition = ContainsCondition('subject', 'test')
        assert condition.evaluate(email) is False