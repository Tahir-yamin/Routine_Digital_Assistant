import os
import time
import json
import base64
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# CONFIGURATION
VAULT_PATH = r"D:\Routine_Digital_Assistant\vault"
INBOX_PATH = os.path.join(VAULT_PATH, "Inbox")
CREDENTIALS_PATH = r"D:\Routine_Digital_Assistant\credentials.json"
ACCOUNTS = ["tahiryamin52@gmail.com", "tahiryamin2050@gmail.com", "tahiryamin2030@gmail.com"]

# Scopes for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def log_activity(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [GMAIL] {msg}")
    log_file = os.path.join(VAULT_PATH, "System_Audit.log")
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(f"[{timestamp}] [GMAIL] {msg}\n")

class GmailWatcher:
    def __init__(self):
        self.last_check_file_prefix = os.path.join(VAULT_PATH, ".gmail_last_check_")
        self.services = {}
        self.initialize_services()

    def get_token_path(self, email):
        safe_email = email.split('@')[0]
        return os.path.join(os.path.dirname(CREDENTIALS_PATH), f"token_{safe_email}.json")

    def initialize_services(self):
        for email in ACCOUNTS:
            service = self.authenticate(email)
            if service:
                self.services[email] = service
                log_activity(f"Initialized service for {email}")
            else:
                log_activity(f"FAILED to initialize service for {email}")

    def authenticate(self, email):
        """Authenticate with Gmail API for a specific email"""
        token_path = self.get_token_path(email)
        creds = None
        
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    log_activity(f"Failed to refresh token for {email}: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(CREDENTIALS_PATH):
                    log_activity("CRITICAL: credentials.json not found.")
                    return None
                    
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                
                # Get the auth URL
                auth_url, _ = flow.authorization_url(prompt='consent', login_hint=email)
                log_activity(f"HANDSHAKE REQUIRED for {email}: {auth_url}")
                
                print("\n" + "!"*60)
                print(f"GMAIL HANDSHAKE REQUIRED: {email}")
                print(f"URL: {auth_url}")
                print("!"*60 + "\n")
                
                creds = flow.run_local_server(port=0, open_browser=True)

            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def get_last_check_time(self, email):
        safe_email = email.split('@')[0]
        check_file = f"{self.last_check_file_prefix}{safe_email}"
        try:
            with open(check_file, 'r') as f:
                return float(f.read().strip())
        except FileNotFoundError:
            return time.time() - 3600

    def save_last_check_time(self, email, timestamp):
        safe_email = email.split('@')[0]
        check_file = f"{self.last_check_file_prefix}{safe_email}"
        with open(check_file, 'w') as f:
            f.write(str(timestamp))

    def fetch_new_emails(self, email, service):
        last_check = self.get_last_check_time(email)
        query = f'after:{int(last_check)}'
        try:
            results = service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])
            
            emails = []
            for msg in messages:
                msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
                headers = msg_data['payload'].get('headers', [])
                
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown Sender')
                
                body = ""
                payload = msg_data['payload']
                parts = payload.get('parts', [])
                if not parts and 'body' in payload:
                    parts = [payload]
                
                for part in parts:
                    if part.get('mimeType') == 'text/plain':
                        data = part['body'].get('data', '')
                        if data:
                            body = base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
                        break
                
                emails.append({
                    'id': msg['id'],
                    'subject': subject,
                    'sender': sender,
                    'body': body[:1000],
                    'account': email
                })
            return emails
        except Exception as e:
            log_activity(f"Error fetching for {email}: {e}")
            return []

    def run_cycle(self):
        for email, service in self.services.items():
            emails = self.fetch_new_emails(email, service)
            for mail in emails:
                filename = f"EMAIL_{email.split('@')[0]}_{mail['id']}.md"
                filepath = os.path.join(INBOX_PATH, filename)
                
                if os.path.exists(filepath): continue

                content = f"""# INCOMING GMAIL PERCEPTION ({email})
---
From: {mail['sender']}
Subject: {mail['subject']}
ID: {mail['id']}
---
{mail['body']}

---
*Perceived via Sovereign Gmail Watcher*
"""
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                log_activity(f"[{email}] Perceived email: {mail['subject']}")
            
            self.save_last_check_time(email, time.time())

if __name__ == "__main__":
    log_activity("Sovereign Multi-Account Gmail Watcher Initialized.")
    watcher = GmailWatcher()
    while True:
        watcher.run_cycle()
        time.sleep(300)
