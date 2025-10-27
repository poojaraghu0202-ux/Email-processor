📧 Email Rule Processor

Email Rule Processor is a standalone Python application that integrates with the Gmail API to fetch, store, and process emails automatically based on configurable rules.
It allows users to define flexible rule conditions (like sender, subject, or age) and execute actions such as marking emails as read/unread or moving them to specific labels.

✨ Features

🔐 Gmail OAuth 2.0 Authentication — Secure authentication via Google’s official Python client

📥 Email Fetching — Fetch emails from Gmail and store them in a relational database

⚙️ Rule-Based Processing — Apply custom rules defined in JSON format

🧩 Flexible Conditions — Supports string-based (e.g., “contains”, “equals”) and date-based predicates (e.g., “older than N days”)

📨 Multiple Actions — Mark emails as read/unread, move them to labels, and more

🏗️ Extensible Architecture — Easily add new providers, condition types, and actions

🧪 Comprehensive Tests 

🛠️ Tech Stack

Python 3

SQLAlchemy — ORM for database operations

Gmail API (via google-api-python-client)

pytest — for testing


Project structure

email-rule-processor/
├── src/
│   ├── fetch_emails.py             # Script 1: Fetch emails from Gmail
│   ├── process_emails.py           # Script 2: Apply rules to stored emails
│   ├── config/
│   │   ├── settings.py             # Configuration management
│   │   └── rules.json              # Rule definitions
│   ├── providers/
│   │   ├── provider.py             # Abstract email provider interface
│   │   ├── gmail_provider.py       # Gmail API implementation
│   │   └── factory.py              # Provider factory pattern
│   ├── database/
│   │   ├── email_info.py           # SQLAlchemy model for Email info
│   │   ├── rule_execution.py       # SQLAlchemy model for rule execution
│   │   └── email_datastore.py      # Data store layer
│   ├── enums/
│   │   └── email_enums.py          # Enums for actions, labels, and statuses
│   ├── rules/
│   │   ├── engine.py               # Rule evaluation engine
│   │   ├── parser.py               # JSON rule parser
│   │   ├── conditions/
│   │   │   ├── conditions.py       # Abstract condition interface
│   │   │   ├── string_conditions.py # String-based predicates
│   │   │   ├── date_conditions.py   # Date-based predicates
│   │   │   └── factory.py          # Condition factory
│   │   └── actions/
│   │       ├── action.py           # Abstract action interface
│   │       ├── mark_actions.py     # Mark read/unread actions
│   │       ├── move_actions.py     # Move message action
│   │       └── factory.py          # Action factory
│   ├── utils/
│   │   └── logger.py               # Logging configuration
│   └── tests/
│       ├── unit/                   # Unit tests
│       │   └── conftest.py         # Shared test fixtures
├── .gitignore                      # Ignore secrets and temp files
└── README.md


   
 
  
  
  
