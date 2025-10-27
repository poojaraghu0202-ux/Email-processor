import pytest
from datetime import datetime


class TestEmailRepository:
    """Test EmailRepository integration"""
    
    def test_save_emails(self, email_repository, sample_email):
        """Test saving emails to database"""
        new_count = email_repository.save_emails([sample_email])
        assert new_count == 1
    
    def test_save_duplicate_emails(self, email_repository, sample_email):
        """Test saving duplicate emails (should update)"""
        email_repository.save_emails([sample_email])
        new_count = email_repository.save_emails([sample_email])
        assert new_count == 0  # No new emails
    
    def test_get_all_emails(self, email_repository, sample_email, old_email):
        """Test retrieving all emails"""
        email_repository.save_emails([sample_email, old_email])
        emails = email_repository.get_all_emails()
        assert len(emails) == 2
    
    def test_get_emails_for_processing(self, email_repository, sample_email):
        """Test getting emails for processing"""
        email_repository.save_emails([sample_email])
        emails = email_repository.get_emails_for_processing()
        assert len(emails) >= 1
    
    def test_log_rule_execution(self, email_repository, sample_email):
        """Test logging rule execution"""
        email_repository.save_emails([sample_email])
        email_repository.log_rule_execution(
            email_id=sample_email['id'],
            rule_name='Test Rule',
            matched=True,
            actions=['mark_as_read']
        )
        
        executions = email_repository.get_rule_executions(sample_email['id'])
        assert len(executions) == 1
        assert executions[0].rule_name == 'Test Rule'
        assert executions[0].matched is True
    
    def test_email_to_dict(self, email_repository, sample_email):
        """Test email model to_dict method"""
        email_repository.save_emails([sample_email])
        emails = email_repository.get_all_emails()
        email_dict = emails[0].to_dict()
        
        assert email_dict['id'] == sample_email['id']
        assert email_dict['from'] == sample_email['from']
        assert email_dict['subject'] == sample_email['subject']