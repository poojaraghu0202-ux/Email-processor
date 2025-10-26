import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from provider.factory import EmailProviderFactory
from datastore.email_datastore import EmailRepository
from config.settings import EMAIL_PROVIDER, FETCH_LIMIT
from utils.logger import setup_logger


logger = setup_logger(__name__)
logger = setup_logger(__name__)

def main():
    """Main function to fetch and store emails"""
    try:
        logger.info("=" * 70)
        logger.info("EMAIL FETCHER - Starting Process")
        logger.info("=" * 70)
        
        # Create email provider
        logger.info(f"Creating {EMAIL_PROVIDER} provider...")
        provider = EmailProviderFactory.create(EMAIL_PROVIDER)
        
        # Authenticate
        logger.info("Authenticating with Gmail API...")
        provider.authenticate()
        
        # Fetch emails
        logger.info(f"Fetching up to {FETCH_LIMIT} emails from INBOX...")
        emails = provider.fetch_emails(folder="None", limit=FETCH_LIMIT)
        
        if not emails:
            logger.info("No emails found.")
            return
        
        # Save to database
        logger.info("Saving emails to database...")
        repo = EmailRepository()
        new_count = repo.save_emails(emails, provider_type=EMAIL_PROVIDER)
        
        logger.info("=" * 70)
        logger.info("✓ SUCCESS")
        logger.info(f"  Total emails fetched: {len(emails)}")
        logger.info(f"  New emails saved: {new_count}")
        logger.info(f"  Updated emails: {len(emails) - new_count}")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"✗ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()