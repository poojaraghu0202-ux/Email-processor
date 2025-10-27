import pytest
from rules.parser import RuleParser
from rules.engine import Rule


class TestRuleParser:
    """Test RuleParser"""
    
    def test_parse_rules_from_file(self, sample_rules_json):
        """Test parsing rules from JSON file"""
        parser = RuleParser()
        rules = parser.parse_file(sample_rules_json)
        
        assert len(rules) == 2
        assert rules[0].name == 'Test Rule 1'
        assert rules[1].name == 'Test Rule 2'
    
    def test_parse_rule_conditions(self, sample_rules_json):
        """Test parsing rule conditions"""
        parser = RuleParser()
        rules = parser.parse_file(sample_rules_json)
        
        rule = rules[0]
        assert len(rule.conditions) == 2
        assert rule.conditions[0].field == 'from'
        assert rule.conditions[0].value == 'boss'
    
    def test_parse_rule_actions(self, sample_rules_json):
        """Test parsing rule actions"""
        parser = RuleParser()
        rules = parser.parse_file(sample_rules_json)
        
        rule = rules[1]
        assert len(rule.actions) == 2
    
    def test_parse_file_not_found(self):
        """Test parsing non-existent file"""
        parser = RuleParser()
        with pytest.raises(FileNotFoundError):
            parser.parse_file('nonexistent.json')
    
    def test_parse_invalid_json(self, tmp_path):
        """Test parsing invalid JSON"""
        invalid_file = tmp_path / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write("invalid json content")
        
        parser = RuleParser()
        with pytest.raises(Exception):
            parser.parse_file(str(invalid_file))