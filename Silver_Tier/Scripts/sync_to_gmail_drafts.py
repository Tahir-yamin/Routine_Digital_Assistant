import os
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# CONFIGURATION
VAULT_PATH = r"D:\Routine_Digital_Assistant\vault"
DRAFTS_FOLDER = os.path.join(VAULT_PATH, "Drafts")
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
ACCOUNTS = ["tahiryamin52@gmail.com", "tahiryamin2050@gmail.com", "tahiryamin2030@gmail.com"]

def get_service(email):
    safe_email = email.split('@')[0]
    token_path = os.path.join(r"D:\Routine_Digital_Assistant", f"token_{safe_email}.json")
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        return build('gmail', 'v1', credentials=creds)
    return None

def create_gmail_draft(service, recipient, subject, body):
    message = MIMEText(body)
    message['to'] = recipient
    message['subject'] = subject
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    try:
        draft = service.users().drafts().create(userId='me', body={'message': {'raw': raw}}).execute()
        return draft['id']
    except Exception as e:
        print(f"Error creating draft: {e}")
        return None

def sync():
    if not os.path.exists(DRAFTS_FOLDER):
        print("No drafts folder found.")
        return

    services = {email: get_service(email) for email in ACCOUNTS}
    
    draft_files = [f for f in os.listdir(DRAFTS_FOLDER) if f.startswith("DRAFT_")]
    print(f"Syncing {len(draft_files)} drafts to Gmail accounts...")

    for filename in draft_files:
        path = os.path.join(DRAFTS_FOLDER, filename)
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Simple parsing
        subject = "No Subject"
        recipient = ""
        account_name = ""
        body_start = 0
        
        for i, line in enumerate(lines):
            if line.startswith("# 📝 EXECUTIVE DRAFT:"):
                subject = line.replace("# 📝 EXECUTIVE DRAFT:", "").strip()
            elif line.startswith("**Target Recipient**:"):
                recipient = line.replace("**Target Recipient**:", "").strip()
            elif line.startswith("**Account Context**:"):
                account_name = line.replace("**Account Context**:", "").strip()
            elif "---" in line and i > 2:
                body_start = i + 1
                break
        
        body = "".join(lines[body_start:]).strip()
        
        # Match account
        target_email = None
        if account_name.lower() == "primary":
            target_email = "tahiryamin52@gmail.com"
        else:
            for email in ACCOUNTS:
                if account_name in email:
                    target_email = email
                    break
        
        if target_email and services[target_email]:
            safe_subject = subject.encode('ascii', 'ignore').decode('ascii')
            print(f"Uploading draft to {target_email}: {safe_subject}")
            draft_id = create_gmail_draft(services[target_email], recipient, subject, body)
            if draft_id:
                print(f"Successfully uploaded! Draft ID: {draft_id}")
                # Move to processing/done to avoid duplication
                done_path = os.path.join(VAULT_PATH, "Logs", "Synced_Drafts")
                if not os.path.exists(done_path): os.makedirs(done_path)
                os.rename(path, os.path.join(done_path, filename))
            else:
                print(f"Failed to upload {filename}")
        else:
            print(f"Could not find matching service for '{account_name}'")

if __name__ == '__main__':
    sync()
