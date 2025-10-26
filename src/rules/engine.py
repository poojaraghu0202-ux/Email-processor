from typing import List, Dict, Any
from enum import Enum
from utils.logger import setup_logger

logger = setup_logger(__name__)

class RulePredicate(Enum):
    """Rule predicate types"""
    ALL = "all"
    ANY = "any"


class Rule:
    """Represents a single rule with conditions and actions"""
    
    def __init__(self, name: str, predicate: str, conditions: List[Any], 
                 actions: List[Any], description: str = ""):
        self.name = name
        self.description = description
        self.predicate = RulePredicate(predicate.lower())
        self.conditions = conditions
        self.actions = actions
    
    def matches(self, email: Dict[str, Any]) -> bool:
        """Check if email matches rule conditions"""
        if not self.conditions:
            return False
        
        results = [condition.evaluate(email) for condition in self.conditions]
        
        if self.predicate == RulePredicate.ALL:
            return all(results)
        else:  # ANY
            return any(results)
    
    def apply(self, email_provider: Any, email: Dict) -> List[bool]:
        """Apply all actions to the email"""
        results = []
        for action in self.actions:
            try:
                result = action.execute(email_provider, email)
                results.append(result)
            except Exception as e:
                logger.error(f"Error executing action {action}: {str(e)}")
                results.append(False)
        return results
    
    def __repr__(self):
        return f"<Rule(name={self.name}, predicate={self.predicate.value}, conditions={len(self.conditions)}, actions={len(self.actions)})>"


class RulesEngine:
    """Main engine for processing rules"""
    
    def __init__(self, rules: List[Rule]):
        self.rules = rules
        logger.info(f"Initialized RulesEngine with {len(rules)} rules")
    
    def process_email(self, email_provider: Any, email: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single email against all rules"""
        results = {
            'email_id': email['id'],
            'email_subject': email.get('subject', '')[:50],
            'rules_matched': [],
            'actions_executed': [],
            'actions_failed': []
        }
        
        for rule in self.rules:
            try:
                if rule.matches(email):
                    logger.info(f"  ✓ Rule matched: '{rule.name}'")
                    results['rules_matched'].append(rule.name)
                    
                    action_results = rule.apply(email_provider, email)
                    
                    for action, success in zip(rule.actions, action_results):
                        action_name = type(action).__name__
                        if success:
                            results['actions_executed'].append(action_name)
                        else:
                            results['actions_failed'].append(action_name)
            except Exception as e:
                logger.error(f"Error processing rule '{rule.name}': {str(e)}")
        
        return results
    
    def process_emails(self, email_provider: Any, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple emails"""
        logger.info(f"Processing {len(emails)} emails against {len(self.rules)} rules...")
        results = []
        
        for i, email in enumerate(emails, 1):
            logger.info(f"\n[{i}/{len(emails)}] Processing: {email.get('subject', 'No Subject')[:60]}")
            result = self.process_email(email_provider, email)
            results.append(result)
        
        return results