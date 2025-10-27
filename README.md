Email Rule Processor 

A standalone Python application that integrates with Gmail API to fetch emails and process them based on
configurable rules

Features

  Gmail OAuth 2.0 Authentication - Secure authentication using Google's official Python client 
  Email Fetching - Fetch emails from Gmail and store in relational database
  Rule-Based Processing - Define rules in JSON with conditions and actions
  Flexible Conditions - String predicates (contains, equals) and date predicates (less than/greater than
days/months)
 Multiple Actions - Mark as read/unread, move to labels
Extensible Architecture - Easy to add new providers, conditions, and actions
 Comprehensive Tests

Tech Stack
      Python3
      SQLAlchemy - ORM for database operations


Project structure

email-rule-processor/
├── src/
│ ├── fetch_emails.py                  # Script 1: Fetch emails from Gmail
| |
│ ├── process_emails.py                # Script 2: Process emails with rules
| |
│ ├── config/
│ │ ├── settings.py                    # Configuration management
│ │ └── rules.json                     # Rule definitions
|
│ ├── providers/
│ │ ├── provider.py                    # Abstract email provider interface
│ │ ├── gmail_provider.py              # Gmail API implementation
│ │ └── factory.py                     # Provider factory pattern
| |
│ ├── database/
│ │ ├── email_info.py                  # SQLAlchemy model for Email info 
| | |__ rule_execution.py               # SQLAlchemy model for rule execution
│ │ └── email_datastore.py             # Data store layer
| |
| |___ enums/
| |  |__email_enums.py
| |  
| |
│ ├── rules/
│ │ ├── engine.py                      # Rule evaluation engine
│ │ ├── parser.py                     # JSON rule parser
| | |
│ │ ├── conditions/
│ │ │ ├── conditions.py               # Abstract condition interface
│ │ │ ├── string_conditions.py        # String predicates
│ │ │ ├── date_conditions.py          # Date predicates
│ │ │ └── factory.py                 # Condition factory
| | |
│ │ └── actions/
│ │ ├── action.py                    # Abstract action interface
│ │ ├── mark_actions.py              # Mark read/unread actions
│ │ ├── move_actions.py              # Move message action
│ │ └── factory.py                   # Action factory
| |
│ └── utils/
│ ├── logger.py                      # Logging configuration
│
├── tests/
│ ├── unit/ # Unit tests
│ 
│ └── conftest.py # Test fixtures

   
 
  
  
  
