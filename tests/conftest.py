import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from datastore.email_info import Base as EmailBase, Email
from datastore.rule_execution import Base as RuleBase, RuleExecution
from datastore.email_datastore import EmailRepository
from rules.conditions.factory import ConditionFactory
from rules.actions.factory import ActionFactory
from rules.engine import Rule, RulesEngine
from rules.parser import RuleParser


@pytest.fixture
def test_db():
    """Create in-memory test database"""
    engine = create_engine('sqlite:///:memory:')
    EmailBase.metadata.create_all(engine)
    RuleBase.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def email_repository():
    """Create test email repository"""
    return EmailRepository('sqlite:///:memory:')


@pytest.fixture
def sample_email():
    """Sample email data for testing"""
    return {
        'id': 'test_email_123',
        'thread_id': 'thread_456',
        'from': 'boss@company.com',
        'to': 'employee@company.com',
        'subject': 'Urgent: Project Update',
        'labels': ['INBOX', 'IMPORTANT'],

        'received_date': datetime(2024, 1, 1, 10, 0, 0),
        'is_read': False
    }


@pytest.fixture
def old_email():
    """Old email for date testing"""
    return {
        'id': 'old_email_456',
        'thread_id': 'thread_789',
        'from': 'newsletter@example.com',
        'to': 'user@company.com',
        'subject': 'Weekly Newsletter',
        'labels': ['INBOX', 'NEWSLETTER'],
        'received_date': datetime.now() - timedelta(days=365),
        'is_read': False,
    }


@pytest.fixture
def mock_gmail_provider(mocker):
    """Mock Gmail provider"""
    mock_provider = mocker.MagicMock()
    mock_provider.mark_as_read.return_value = True
    mock_provider.mark_as_unread.return_value = True
    mock_provider.move_email.return_value = True
    return mock_provider


@pytest.fixture
def condition_factory():
    """Condition factory instance"""
    return ConditionFactory()


@pytest.fixture
def action_factory():
    """Action factory instance"""
    return ActionFactory()


@pytest.fixture
def sample_rules_json(tmp_path):
    """Create temporary rules JSON file"""
    rules_data = {
        "rules": [
            {
                "name": "Test Rule 1",
                "description": "Mark urgent emails as read",
                "predicate": "all",
                "conditions": [
                    {"field": "from", "predicate": "contains", "value": "boss"},
                    {"field": "subject", "predicate": "contains", "value": "urgent"}
                ],
                "actions": [
                    {"type": "mark_as_read"}
                ]
            },
            {
                "name": "Test Rule 2",
                "description": "Archive newsletters",
                "predicate": "any",
                "conditions": [
                    {"field": "subject", "predicate": "contains", "value": "newsletter"},
                    {"field": "from", "predicate": "contains", "value": "noreply"}
                ],
                "actions": [
                    {"type": "mark_as_read"},
                    {"type": "move_message", "parameters": {"destination": "Archive"}}
                ]
            }
        ]
    }
    
    rules_file = tmp_path / "test_rules.json"
    with open(rules_file, 'w') as f:
        json.dump(rules_data, f)
    
    return str(rules_file)