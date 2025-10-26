import os
import base64
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from email.utils import parsedate_to_datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .email_provider import EmailProvider
from config.settings import SCOPES, CREDENTIALS_FILE, TOKEN_FILE
from utils.logger import setup_logger

logger = setup_logger(__name__)


class GmailProvider(EmailProvider):
    """Gmail API implementation"""

    def __init__(self):
        self.service = None
        self.user_id = "me"
        self.creds = None

    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth 2.0
        Creates token.json on first run for subsequent authentications
        """
        try:
            if os.path.exists(TOKEN_FILE):
                self.creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    logger.info("Refreshing expired credentials...")
                    self.creds.refresh(Request())
                else:
                    if not os.path.exists(CREDENTIALS_FILE):
                        raise FileNotFoundError(
                            f"Credentials file not found at {CREDENTIALS_FILE}. "
                            "Please download it from Google Cloud Console."
                        )
                    logger.info("Starting OAuth 2.0 flow...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(CREDENTIALS_FILE), SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)

                with open(TOKEN_FILE, 'w') as token:
                    token.write(self.creds.to_json())
                logger.info(f"Credentials saved to {TOKEN_FILE}")

            self.service = build('gmail', 'v1', credentials=self.creds)
            logger.info("Successfully authenticated with Gmail API")
            return True

        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise

    def fetch_emails(self,folder: Optional[str] = "None", limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch emails from Gmail
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        try:
            logger.info(f"Fetching up to {limit} emails from {folder}...")
            results = self.service.users().messages().list(
                userId=self.user_id,
                labelIds=[folder] if folder and folder != "None" else None,
                maxResults=limit
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                logger.info("No messages found.")
                return []

            logger.info(f"Found {len(messages)} messages. Fetching details...")

            emails = []
            for i, msg in enumerate(messages, 1):
                try:
                    email_data = self.service.users().messages().get(
                        userId=self.user_id,
                        id=msg['id'],
                        format='full'
                    ).execute()

                    parsed_email = self._parse_email(email_data)
                    emails.append(parsed_email)

                    if i % 10 == 0:
                        logger.info(f"Processed {i}/{len(messages)} emails...")

                except HttpError as e:
                    logger.error(f"Error fetching email {msg['id']}: {str(e)}")
                    continue

            logger.info(f"Successfully fetched {len(emails)} emails")
            return emails

        except HttpError as e:
            logger.error(f"Gmail API error: {str(e)}")
            raise

    def _parse_email(self, raw_email: Dict) -> Dict[str, Any]:
        headers = {}
        for header in raw_email['payload'].get('headers', []):
            headers[header['name']] = header['value']

        date_str = headers.get('Date', '')
        try:
            received_date = parsedate_to_datetime(date_str)
        except Exception:
            received_date = datetime.now()

        body = self._extract_body(raw_email['payload'])
        is_read = 'UNREAD' not in raw_email.get('labelIds', [])
        labels = raw_email.get('labelIds', [])

        return {
            'id': raw_email['id'],
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', ''),
            'date': date_str,
            'received_date': received_date,
            'is_read': is_read,
            'labels': labels
        }

    def _extract_body(self, payload: Dict) -> str:
        body = ""

        if 'body' in payload and 'data' in payload['body']:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        elif 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                    body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                elif part['mimeType'] == 'text/html' and not body and 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                elif 'parts' in part:
                    body += self._extract_body(part)

        return body.strip()

    def mark_as_read(self, email_id: str) -> bool:
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        try:
            self.service.users().messages().modify(
                userId=self.user_id,
                id=email_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            logger.info(f"Marked email {email_id} as read")
            return True
        except HttpError as e:
            logger.error(f"Error marking email as read: {str(e)}")
            return False

    def mark_as_unread(self, email_id: str) -> bool:
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        try:
            self.service.users().messages().modify(
                userId=self.user_id,
                id=email_id,
                body={'addLabelIds': ['UNREAD']}
            ).execute()
            logger.info(f"Marked email {email_id} as unread")
            return True
        except HttpError as e:
            logger.error(f"Error marking email as unread: {str(e)}")
            return False

    def move_email(self, email_id: str, destination: str) -> bool:
        """
        Move email to destination label safely
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        SYSTEM_LABELS = {"INBOX", "SENT", "DRAFT", "SPAM", "TRASH", "UNREAD", "STARRED", "IMPORTANT"}

        try:
            label_id = self._get_label_id(destination)
            if not label_id:
                logger.error(f"Label '{destination}' not found")
                return False

            message = self.service.users().messages().get(
                userId=self.user_id,
                id=email_id,
                format="metadata"
            ).execute()
            current_labels = set(message.get('labelIds', []))

            add_labels = {label_id} - current_labels
            remove_labels = {lbl for lbl in current_labels if lbl not in add_labels and lbl not in SYSTEM_LABELS}

            if not add_labels and not remove_labels:
                logger.info(f"No label changes needed for email {email_id}")
                return True

            self.service.users().messages().modify(
                userId=self.user_id,
                id=email_id,
                body={
                    'addLabelIds': list(add_labels),
                    'removeLabelIds': list(remove_labels)
                }
            ).execute()

            logger.info(f"Moved email {email_id} to {destination}")
            return True

        except HttpError as e:
            logger.error(f"Error moving email: {str(e)}")
            return False

    def _get_label_id(self, label_name: str) -> Optional[str]:
        if label_name in ['INBOX', 'SENT', 'DRAFT', 'SPAM', 'TRASH', 'UNREAD', 'STARRED', 'IMPORTANT']:
            return label_name

        try:
            labels = self.get_labels()
            for label in labels:
                if label['name'].lower() == label_name.lower():
                    return label['id']
            return None
        except Exception:
            return None

    def get_labels(self) -> List[Dict[str, str]]:
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        try:
            results = self.service.users().labels().list(userId=self.user_id).execute()
            labels = results.get('labels', [])
            return [{'id': label['id'], 'name': label['name']} for label in labels]
        except HttpError as e:
            logger.error(f"Error fetching labels: {str(e)}")
            return []

    def create_label(self, label_name: str) -> Optional[str]:
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        try:
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }

            created_label = self.service.users().labels().create(
                userId=self.user_id,
                body=label_object
            ).execute()

            logger.info(f"Created label: {label_name}")
            return created_label['id']
        except HttpError as e:
            logger.error(f"Error creating label: {str(e)}")
            return None
