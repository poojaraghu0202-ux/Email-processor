import json
from typing import List, Dict
from pathlib import Path

from .engine import Rule
from rules.conditions.factory import ConditionFactory
from rules.actions.factory import ActionFactory
from utils.logger import setup_logger

logger = setup_logger(__name__)

class RuleParser:
    """Parse rules from JSON configuration"""
    
    def __init__(self):
        self.condition_factory = ConditionFactory()
        self.action_factory = ActionFactory()
    
    def parse_file(self, filepath: str) -> List[Rule]:
        """Parse rules from JSON file"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Rules file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        rules = self.parse_rules(data.get('rules', []))
        logger.info(f"Loaded {len(rules)} rules from {filepath}")
        return rules
    
    def parse_rules(self, rules_data: List[Dict]) -> List[Rule]:
        """Parse list of rule definitions"""
        rules = []
        for rule_data in rules_data:
            try:
                rule = self._parse_rule(rule_data)
                rules.append(rule)
                logger.info(f"  ✓ Loaded rule: {rule.name}")
            except Exception as e:
                logger.error(f"  ✗ Failed to parse rule '{rule_data.get('name', 'Unknown')}': {str(e)}")
        return rules
    
    def _parse_rule(self, rule_data: Dict) -> Rule:
        """Parse single rule definition"""
        # Parse conditions
        conditions = []
        for cond in rule_data.get('conditions', []):
            condition = self.condition_factory.create(
                predicate=cond['predicate'],
                field=cond['field'],
                value=cond['value']
            )
            conditions.append(condition)
        
        # Parse actions
        actions = []
        for action_data in rule_data.get('actions', []):
            action = self.action_factory.create(
                action_type=action_data['type'],
                parameters=action_data.get('parameters')
            )
            actions.append(action)
        
        return Rule(
            name=rule_data['name'],
            description=rule_data.get('description', ''),
            predicate=rule_data['predicate'],
            conditions=conditions,
            actions=actions
        )