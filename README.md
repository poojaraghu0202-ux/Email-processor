📧 Email Rule Processor

Email Rule Processor is a standalone Python application that integrates with the Gmail API to fetch, store, and process emails automatically based on configurable rules.
It allows users to define flexible rule conditions (like sender, subject, or age) and execute actions such as marking emails as read/unread or moving them to specific labels.

## ✨ Features

- 🔐 **Gmail OAuth 2.0 Authentication** — Secure authentication via Google's official Python client
- 📥 **Email Fetching** — Fetch emails from Gmail and store them in a relational database
- ⚙️ **Rule-Based Processing** — Apply custom rules defined in JSON format
- 🧩 **Flexible Conditions** — Supports string-based (e.g., "contains", "equals") and date-based predicates (e.g., "older than N days")
- 📨 **Multiple Actions** — Mark emails as read/unread, move them to labels, and more
- 🏗️ **Extensible Architecture** — Easily add new providers, condition types, and actions
- 🧪 **Comprehensive Tests**

## 🛠️ Tech Stack

- **Python 3**
- **SQLAlchemy** — ORM for database operations
- **Gmail API** (via google-api-python-client)
- **pytest** — for testing

## 📁 Project Structure
```
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
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Gmail account
- Google Cloud Project with Gmail API enabled

### 1. Clone Repository

```bash
git clone 
cd email-rule-processor
```

### 2. Install Dependencies

```bash
# Install main dependencies
pip install -r requirements.txt
```

### 3. Google Cloud Setup

#### Step 1: Go to Google Cloud Console
Visit: https://console.cloud.google.com

#### Step 2: Create/Select Project
Create a new project or select an existing one

#### Step 3: Enable Gmail API
1. Navigate to: **APIs & Services > Library**
2. Search for "Gmail API"
3. Click "Enable"

#### Step 4: Create OAuth 2.0 Credentials
1. Go to: **APIs & Services > Credentials**
2. Click: **"Create Credentials" > "OAuth client ID"**
3. Application type: **"Desktop app"**
4. Name it: "Email Rule Processor"
5. Click "Create"

#### Step 5: Download Credentials
1. Click the download icon next to your OAuth 2.0 Client ID
2. Save the file as `credentials.json` in the project root directory

### 4. Configure Rules

Edit `src/config/rules.json` to define your email processing rules.

Each rule has:
- **name**: Unique rule identifier
- **description**: Human-readable description
- **predicate**: `"all"` (AND logic) or `"any"` (OR logic)
- **conditions**: Array of conditions to match
- **actions**: Array of actions to execute

## 📖 Usage

### Step 1: Fetch Emails

Run this script first to authenticate and fetch emails:
```bash
python3 fetch_emails.py
```

**What happens:**
1. Opens browser for Gmail OAuth authentication (first time only)
2. You grant necessary permissions
3. Fetches emails as configured in the fetch limit given in setting.py
4. Stores emails in database
5. Creates `token.json` for future authentication

### Step 2: Process Emails

Run the rule processor:
```bash
python3 process_emails.py
```

**What happens:**
1. Loads rules from `src/config/rules.json`
2. Authenticates with Gmail API
3. Retrieves emails from database
4. Evaluates each email against rules
5. Executes actions for matching emails
6. Logs results to database



## 🏗️ Architecture

### Design Patterns

The application follows several key design patterns for maintainability and extensibility:

#### 1. **Strategy Pattern** — Email Providers
- Abstracts email provider implementations (Gmail, Zoho, Outlook)
- Implemented in `src/providers/`

#### 2. **Factory Pattern** — Component Creation
- Creates conditions, actions, and providers dynamically
- Centralizes object instantiation logic
- Factory implementations:
  - `src/providers/factory.py` — Provider factory
  - `src/rules/conditions/factory.py` — Condition factory
  - `src/rules/actions/factory.py` — Action factory

#### 3. **Repository Pattern** — Data Access Layer
- Abstracts database operations from business logic
- Implemented in `src/database/email_datastore.py`

#### 4. **Command Pattern** — Executable Actions
- Encapsulates action as an object with a common interface
- Implemented in `src/rules/actions/`





   
 
  
  
  
