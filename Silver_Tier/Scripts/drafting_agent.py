import os
import time
from datetime import datetime

# CONFIGURATION
VAULT_PATH = r"D:\Routine_Digital_Assistant\vault"
ACTION_PATH = os.path.join(VAULT_PATH, "Needs_Action")
DRAFTS_PATH = os.path.join(VAULT_PATH, "Drafts")

def log_activity(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_msg = msg.encode('ascii', 'ignore').decode('ascii')
    print(f"[{timestamp}] [DRAFT] {safe_msg}")
    log_file = os.path.join(VAULT_PATH, "System_Audit.log")
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(f"[{timestamp}] [DRAFT] {msg}\n")

def create_draft(action_file):
    """
    Silver Tier Action:
    Drafts a professional response for items in Needs_Action.
    """
    if not action_file.endswith(('.md', '.txt')):
        return

    file_path = os.path.join(ACTION_PATH, action_file)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return

    # --- SMART FILTERING (Silver Tier Intelligence) ---
    sender = ""
    subject = ""
    if "From:" in content:
        sender = content.split("From:")[1].split("\n")[0].strip()
    if "Subject:" in content:
        subject = content.split("Subject:")[1].split("\n")[0].strip()
    
    log_activity(f"Analyzing: Sender='{sender}', Subject='{subject}'")

    # Rule 1: No-Reply & Automated Filter
    automated_senders = ["no-reply", "noreply", "newsletter", "alert", "notification", "digest", "update"]
    if any(term in sender.lower() for term in automated_senders):
        log_activity(f"Smart Filter: Skipping Automated Sender ({sender})")
        return

    # Rule 2: Newsletter & Marketing Content Detection
    broadcast_terms = [
        "issue #", "job alert", "daily reach", "weekly digest", "top picks", 
        "posted jobs", "marketing", "promotion", "exciting news", "just posted"
    ]
    broadcast_body_patterns = ["hello everyone", "hello all", "hi everyone", "view in browser", "click here to"]
    tracking_links = ["click.convertkit", "email.mg", "newsletter", "/track/"]
    
    body_content = content.split('---')[-1].lower() if '---' in content else content.lower()
    
    if any(term in subject.lower() for term in broadcast_terms) or \
       any(pattern in body_content[:500] for pattern in broadcast_body_patterns) or \
       any(link in body_content for link in tracking_links) or \
       "unsubscribe" in body_content:
        log_activity(f"Smart Filter: Skipping Broadcast/Newsletter ({subject})")
        return

    # Rule 3: Security/System Alert Filter
    system_terms = ["security alert", "welcome to", "sign-in on", "verification code", "confirm your", "access to your account", "published a project"]
    if any(term in subject.lower() for term in system_terms):
        log_activity(f"Smart Filter: Skipping System/Security item ({subject})")
        return

    # Rule 4: Self-Communication Filter
    ACCOUNTS = ["tahiryamin52@gmail.com", "tahiryamin2050@gmail.com", "tahiryamin2030@gmail.com"]
    for email in ACCOUNTS:
        if email.lower() in sender.lower():
            log_activity(f"Smart Filter: Skipping self-email from {sender}")
            return
            
    # Rule 5: Personal Address Detection (Body Only)
    inquiry_markers = ["?", "could you", "request", "please", "can you", "regards"]
    is_personal = "tahir" in body_content or "yamin" in body_content
    has_inquiry = any(marker in body_content for marker in inquiry_markers)
    
    if not (is_personal or has_inquiry):
        log_activity(f"Smart Filter: Skipping Low-Priority/Non-Direct content ({subject})")
        return

    # --------------------------------------------------

    draft_name = f"DRAFT_{action_file.replace('ACTION_', '')}"
    draft_path = os.path.join(DRAFTS_PATH, draft_name)

    # --- OLLAMA AI DRAFTING (Silver Tier Intelligence) ---
    import json
    import requests

    def get_ai_draft(sender, subject, body):
        prompt = f"""
        Act as a Senior Planning Engineer's Executive Assistant. 
        Generate a professional email draft responding to this:
        FROM: {sender}
        SUBJECT: {subject}
        BODY: {body}
        
        Style: Professional, Concise, Executive.
        Sign-off: Tahir Yamin, PMP | Senior Planning Engineer.
        Rule: Mention that this is an automated draft flagged for senior review.
        """
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2:3b-small",
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json().get("response", "Error generating draft.")
        except Exception as e:
            return f"Error connecting to Ollama: {e}"

    log_activity(f"Requesting AI Brain for: {subject}")
    ai_response = get_ai_draft(sender, subject, content)

    # Detect Account Context from action_file
    account_context = "Primary"
    if "tahiryamin2050" in action_file: account_context = "tahiryamin2050"
    elif "tahiryamin2030" in action_file: account_context = "tahiryamin2030"
    
    # Extract clean recipient email if possible
    clean_recipient = sender
    if "<" in sender and ">" in sender:
        clean_recipient = sender.split("<")[1].split(">")[0]

    # Format for sync_to_gmail_drafts.py
    final_draft = f"""# 📝 EXECUTIVE DRAFT: {subject}
**Target Recipient**: {clean_recipient}
**Account Context**: {account_context}
**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---
{ai_response}
"""

    with open(draft_path, 'w', encoding='utf-8') as f:
        f.write(final_draft)
    
    log_activity(f"AI-Powered draft prepared for sync: {draft_name}")

def update_drafts():
    if not os.path.exists(ACTION_PATH): return
    if not os.path.exists(DRAFTS_PATH): os.makedirs(DRAFTS_PATH)

    actions = [f for f in os.listdir(ACTION_PATH) if f.startswith("ACTION_")]
    existing_drafts = [f.replace("DRAFT_", "ACTION_") for f in os.listdir(DRAFTS_PATH)]

    for action in actions:
        if action not in existing_drafts:
            log_activity(f"New action item detected: {action}. Generating outreach draft...")
            create_draft(action)

if __name__ == "__main__":
    log_activity("Drafting Agent (Silver) Initialized.")
    while True:
        update_drafts()
        time.sleep(20)
