import os
import sys
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
ACCOUNTS = ['tahiryamin52@gmail.com', 'tahiryamin2050@gmail.com', 'tahiryamin2030@gmail.com']

def get_service(email):
    safe_email = email.split('@')[0]
    token_path = os.path.join(r'D:\Routine_Digital_Assistant', f'token_{safe_email}.json')
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        return build('gmail', 'v1', credentials=creds)
    return None

def check_inboxes():
    for email in ACCOUNTS:
        service = get_service(email)
        if service:
            try:
                results = service.users().messages().list(userId='me', maxResults=3).execute()
                messages = results.get('messages', [])
                print(f"\n--- {email} ---")
                for msg in messages:
                    msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
                    snippet = msg_data.get('snippet', '')
                    internal_date = int(msg_data.get('internalDate', 0)) / 1000
                    from datetime import datetime
                    dt = datetime.fromtimestamp(internal_date).strftime('%Y-%m-%d %H:%M:%S')
                    headers = msg_data['payload'].get('headers', [])
                    subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
                    try:
                        safe_subject = subject.encode('ascii', 'ignore').decode('ascii')
                        safe_snippet = snippet[:50].encode('ascii', 'ignore').decode('ascii')
                        print(f"[{dt}] Subject: {safe_subject} | Snippet: {safe_snippet}...")
                    except Exception as e:
                        print(f"[{dt}] (Print error): {e}")
            except Exception as e:
                print(f"Error for {email}: {e}")

if __name__ == '__main__':
    check_inboxes()
