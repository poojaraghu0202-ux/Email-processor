import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
from rules.conditions.date_conditions import (
    LessThanDaysCondition,
    GreaterThanDaysCondition,
    LessThanMonthsCondition,
    GreaterThanMonthsCondition
)


class TestDateConditions:
    """Test date-based conditions"""
    
    @freeze_time("2024-01-15")
    def test_less_than_days_recent_email(self):
        """Test LessThanDaysCondition with recent email"""
        email = {
            'received_date': datetime(2024, 1, 10)  # 5 days ago
        }
        condition = LessThanDaysCondition('received_date', 7)
        assert condition.evaluate(email) is True
    
    @freeze_time("2024-01-15")
    def test_less_than_days_old_email(self):
        """Test LessThanDaysCondition with old email"""
        email = {
            'received_date': datetime(2024, 1, 1)  # 14 days ago
        }
        condition = LessThanDaysCondition('received_date', 7)
        assert condition.evaluate(email) is False
    
    @freeze_time("2024-01-15")
    def test_greater_than_days_old_email(self):
        """Test GreaterThanDaysCondition with old email"""
        email = {
            'received_date': datetime(2023, 12, 1)  # 45 days ago
        }
        condition = GreaterThanDaysCondition('received_date', 30)
        assert condition.evaluate(email) is True
    
    @freeze_time("2024-01-15")
    def test_greater_than_days_recent_email(self):
        """Test GreaterThanDaysCondition with recent email"""
        email = {
            'received_date': datetime(2024, 1, 10)  # 5 days ago
        }
        condition = GreaterThanDaysCondition('received_date', 30)
        assert condition.evaluate(email) is False
    
    @freeze_time("2024-06-15")
    def test_less_than_months_recent_email(self):
        """Test LessThanMonthsCondition with recent email"""
        email = {
            'received_date': datetime(2024, 5, 1)  # ~1.5 months ago
        }
        condition = LessThanMonthsCondition('received_date', 2)
        assert condition.evaluate(email) is True
    
    @freeze_time("2024-06-15")
    def test_greater_than_months_old_email(self):
        """Test GreaterThanMonthsCondition with old email"""
        email = {
            'received_date': datetime(2023, 12, 1)  # ~6 months ago
        }
        condition = GreaterThanMonthsCondition('received_date', 3)
        assert condition.evaluate(email) is True
    
    def test_date_condition_with_string_date(self):
        """Test date condition with ISO string date"""
        email = {
            'received_date': '2024-01-10T10:00:00'
        }
        condition = LessThanDaysCondition('received_date', 30)
        # Should handle string dates gracefully
        result = condition.evaluate(email)
        assert isinstance(result, bool)

