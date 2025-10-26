"""
Script to process emails from database using rules

Usage:
    python -m src.process_emails
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from provider.factory import EmailProviderFactory
from datastore.email_datastore import EmailRepository
from rules.parser import RuleParser
from rules.engine import RulesEngine
from config.settings import EMAIL_PROVIDER, RULES_FILE
from utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    """Main function to process emails with rules"""
    try:
        logger.info("=" * 70)
        logger.info("EMAIL RULE PROCESSOR - Starting Process")
        logger.info("=" * 70)
        
        # Load rules
        logger.info(f"Loading rules from {RULES_FILE}...")
        parser = RuleParser()
        rules = parser.parse_file(str(RULES_FILE))
        
        if not rules:
            logger.error("No rules found.")
            return
        
        # Get emails from database
        logger.info("Loading emails from database...")
        repo = EmailRepository()
        emails = repo.get_emails_for_processing()
        
        if not emails:
            logger.info("No emails found in database.")
            logger.info("Run 'python -m src.fetch_emails' first to fetch emails.")
            return
        
        logger.info(f"Found {len(emails)} emails to process")
        
        # Authenticate with provider
        logger.info(f"Authenticating with {EMAIL_PROVIDER}...")
        provider = EmailProviderFactory.create(EMAIL_PROVIDER)
        provider.authenticate()
        
        # Process emails
        logger.info("\nProcessing emails with rules...")
        logger.info("-" * 70)
        
        email_dicts = [email.to_dict() for email in emails]

          # Create rules engine
        engine = RulesEngine(rules)
        results = engine.process_emails(provider, email_dicts)
        
        # Log results to database
        logger.info("\nLogging results to database...")
        for email, result in zip(emails, results):
            for rule_name in result['rules_matched']:
                repo.log_rule_execution(
                    email_id=email.provider_id,
                    rule_name=rule_name,
                    matched=True,
                    actions=result['actions_executed']
                )
        
        # Summary
        logger.info("=" * 70)
        logger.info("✓ PROCESSING COMPLETE")
        logger.info(f"  Total emails processed: {len(results)}")
        
        matched_count = sum(1 for r in results if r['rules_matched'])
        logger.info(f"  Emails matching rules: {matched_count}")
        
        total_actions = sum(len(r['actions_executed']) for r in results)
        logger.info(f"  Total actions executed: {total_actions}")
        
        failed_actions = sum(len(r['actions_failed']) for r in results)
        if failed_actions > 0:
            logger.info(f"  Failed actions: {failed_actions}")
        
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"✗ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()