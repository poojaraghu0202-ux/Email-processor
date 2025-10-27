import pytest
from rules.engine import Rule, RulesEngine, RulePredicate
from rules.conditions.string_conditions import ContainsCondition
from rules.actions.mark_actions import MarkAsReadAction
from unittest.mock import MagicMock


class TestRuleEngine:
    
    def test_rule_creation(self):
        """Test creating a rule"""
        conditions = [ContainsCondition('from', 'boss')]
        actions = [MarkAsReadAction()]
        rule = Rule('Test Rule', 'all', conditions, actions, 'Test description')
        
        assert rule.name == 'Test Rule'
        assert rule.description == 'Test description'
        assert rule.predicate == RulePredicate.ALL
        assert len(rule.conditions) == 1
        assert len(rule.actions) == 1
    
    def test_rule_matches_all_predicate(self, sample_email):
        """Test rule matching with ALL predicate"""
        conditions = [
            ContainsCondition('from', 'boss'),
            ContainsCondition('subject', 'urgent')
        ]
        actions = [MarkAsReadAction()]
        rule = Rule('Test Rule', 'all', conditions, actions)
        
        assert rule.matches(sample_email) is True
    
    def test_rule_not_matches_all_predicate(self, sample_email):
        """Test rule not matching with ALL predicate"""
        conditions = [
            ContainsCondition('from', 'boss'),
            ContainsCondition('subject', 'not_present')
        ]
        actions = [MarkAsReadAction()]
        rule = Rule('Test Rule', 'all', conditions, actions)
        
        assert rule.matches(sample_email) is False
    
    def test_rule_matches_any_predicate(self, sample_email):
        """Test rule matching with ANY predicate"""
        conditions = [
            ContainsCondition('from', 'unknown'),
            ContainsCondition('subject', 'urgent')
        ]
        actions = [MarkAsReadAction()]
        rule = Rule('Test Rule', 'any', conditions, actions)
        
        assert rule.matches(sample_email) is True
    
    def test_rule_not_matches_any_predicate(self, sample_email):
        """Test rule not matching with ANY predicate"""
        conditions = [
            ContainsCondition('from', 'unknown'),
            ContainsCondition('subject', 'not_present')
        ]
        actions = [MarkAsReadAction()]
        rule = Rule('Test Rule', 'any', conditions, actions)
        
        assert rule.matches(sample_email) is False
    
    def test_rule_apply_actions(self, mock_gmail_provider, sample_email):
        """Test applying rule actions"""
        conditions = [ContainsCondition('from', 'boss')]
        actions = [MarkAsReadAction()]
        rule = Rule('Test Rule', 'all', conditions, actions)
        
        results = rule.apply(mock_gmail_provider, sample_email)
        
        assert len(results) == 1
        assert results[0] is True

    def test_engine_initialization(self):
        """Test creating rules engine"""
        conditions = [ContainsCondition('from', 'boss')]
        actions = [MarkAsReadAction()]
        rule = Rule('Test Rule', 'all', conditions, actions)
        
        engine = RulesEngine([rule])
        assert len(engine.rules) == 1
    
    def test_process_single_email(self, mock_gmail_provider, sample_email):
        """Test processing single email"""
        conditions = [ContainsCondition('from', 'boss')]
        actions = [MarkAsReadAction()]
        rule = Rule('Test Rule', 'all', conditions, actions)
        engine = RulesEngine([rule])
        
        result = engine.process_email(mock_gmail_provider, sample_email)
        
        assert result['email_id'] == 'test_email_123'
        assert 'Test Rule' in result['rules_matched']
        assert len(result['actions_executed']) > 0
    
    def test_process_multiple_emails(self, mock_gmail_provider, sample_email, old_email):
        """Test processing multiple emails"""
        conditions = [ContainsCondition('subject', 'urgent')]
        actions = [MarkAsReadAction()]
        rule = Rule('Test Rule', 'all', conditions, actions)
        engine = RulesEngine([rule])
        
        results = engine.process_emails(mock_gmail_provider, [sample_email, old_email])
        
        assert len(results) == 2
        assert results[0]['rules_matched'] == ['Test Rule']  # sample_email matches
        assert results[1]['rules_matched'] == []  # old_email doesn't match
    
    def test_process_email_no_match(self, mock_gmail_provider, sample_email):
        """Test processing email that doesn't match any rule"""
        conditions = [ContainsCondition('from', 'nonexistent')]
        actions = [MarkAsReadAction()]
        rule = Rule('Test Rule', 'all', conditions, actions)
        engine = RulesEngine([rule])
        
        result = engine.process_email(mock_gmail_provider, sample_email)
        
        assert len(result['rules_matched']) == 0
        assert len(result['actions_executed']) == 0

    def test_circular_rule_conditions(self):
        """Test that rule evaluation doesn't cause infinite loops"""
        from rules.conditions.string_conditions import ContainsCondition
        from rules.actions.mark_actions import MarkAsReadAction
        from rules.engine import Rule, RulesEngine
        
        email = {
            'id': 'test_123',
            'from': 'test@test.com',
            'subject': 'Test'
        }
        
        # Create rule that always matches
        rule = Rule('Always Match', 'any',
                   [ContainsCondition('from', 'test')],
                   [MarkAsReadAction()])
        
        engine = RulesEngine([rule])
        mock_provider = MagicMock()
        mock_provider.mark_as_read.return_value = True
        
        # Should complete without infinite loop
        result = engine.process_email(mock_provider, email)
        assert result is not None