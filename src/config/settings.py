import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"
RULES_FILE = BASE_DIR / "src" / "config" / "rules.json"

# Gmail API settings
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels'
]

# Database settings
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///emails.db')

# Email provider settings
EMAIL_PROVIDER = os.getenv('EMAIL_PROVIDER', 'gmail')
FETCH_LIMIT = int(os.getenv('FETCH_LIMIT', 10))