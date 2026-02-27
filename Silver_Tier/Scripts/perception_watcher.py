import os
import json
import time
from datetime import datetime

# CONFIGURATION
VAULT_PATH = r"D:\Routine_Digital_Assistant\vault"
INBOX_PATH = os.path.join(VAULT_PATH, "Inbox")
ACTION_PATH = os.path.join(VAULT_PATH, "Needs_Action")
DASHBOARD_PATH = os.path.join(VAULT_PATH, "Dashboard.md")

def log_activity(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    
    # Update local audit log (optional for Bronze)
    log_file = os.path.join(VAULT_PATH, "System_Audit.log")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

def process_inbox():
    """
    Bronze Tier Perception:
    Scans Inbox and moves items to Needs_Action while tagging them.
    """
    if not os.path.exists(INBOX_PATH):
        os.makedirs(INBOX_PATH)
        return

    files = [f for f in os.listdir(INBOX_PATH) if os.path.isfile(os.path.join(INBOX_PATH, f))]
    
    if not files:
        return

    log_activity(f"Perception detected {len(files)} new items in Inbox.")

    for filename in files:
        src = os.path.join(INBOX_PATH, filename)
        dst = os.path.join(ACTION_PATH, f"ACTION_{filename}")
        
        # Simple atomic move for task ownership
        try:
            os.rename(src, dst)
            log_activity(f"Categorized: {filename} -> Needs_Action")
        except Exception as e:
            log_activity(f"Error processing {filename}: {str(e)}")

def update_dashboard():
    """
    Silver Tier Reasoning:
    Updates Dashboard.md with full pipeline metrics and AI health.
    """
    PLAN_PATH = os.path.join(VAULT_PATH, "Plans")
    DRAFTS_PATH = os.path.join(VAULT_PATH, "Drafts")
    
    pending_items = len(os.listdir(ACTION_PATH)) if os.path.exists(ACTION_PATH) else 0
    plan_count = len(os.listdir(PLAN_PATH)) if os.path.exists(PLAN_PATH) else 0
    draft_count = len(os.listdir(DRAFTS_PATH)) if os.path.exists(DRAFTS_PATH) else 0
    
    # Check Ollama Health
    import requests
    ollama_status = "🔴 OFFLINE"
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=2)
        if resp.status_code == 200:
            ollama_status = "🟢 ACTIVE (llama3.2)"
    except:
        pass

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Read the existing dashboard
    if os.path.exists(DASHBOARD_PATH):
        with open(DASHBOARD_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        skip_standup = False
        
        # Build task list for triage
        standup_lines = []
        for f in os.listdir(ACTION_PATH):
            if f.startswith("ACTION_"):
                standup_lines.append(f"- [ ] {f.replace('ACTION_', '')}\n")
        if not standup_lines: standup_lines = ["*No pending actions.*\n"]

        for line in lines:
            if "**Last Sync**:" in line:
                new_lines.append(f"**Last Sync**: {timestamp}\n")
                continue
            
            # Metrics Update
            if "| **Triage Queue** |" in line:
                new_lines.append(f"| **Triage Queue** | {pending_items} | {'ACTION REQUIRED' if pending_items > 0 else 'CLEAR'} |\n")
                continue
            if "| **AI Plans** |" in line:
                new_lines.append(f"| **AI Plans** | {plan_count} | {'READY FOR REVIEW' if plan_count > 0 else 'EMPTY'} |\n")
                continue
            if "| **Email Drafts** |" in line:
                new_lines.append(f"| **Email Drafts** | {draft_count} | {'AWAITING SYNC' if draft_count > 0 else 'SYNCED'} |\n")
                continue
            
            # Integrity Section
            if "- **AI Brain Status**:" in line:
                new_lines.append(f"- **AI Brain Status**: {ollama_status}\n")
                continue
            if "- **Silver Tier Sync**:" in line:
                new_lines.append(f"- **Silver Tier Sync**: OK (GDS v1.2)\n")
                continue

            # Stand-up Section
            if "### 📥 Pending Triage" in line:
                new_lines.append(line)
                new_lines.extend(standup_lines)
                skip_standup = True
                continue
            
            if skip_standup:
                if line.startswith("###") or line.startswith("---"):
                    skip_standup = False
                    new_lines.append(line)
                continue

            new_lines.append(line)

        with open(DASHBOARD_PATH, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            
    log_activity(f"Dashboard updated. Triage:{pending_items} Plans:{plan_count} Drafts:{draft_count}")

if __name__ == "__main__":
    log_activity("Routine Digital Assistant (Silver Watcher) Initialized.")
    while True:
        process_inbox()
        update_dashboard()
        time.sleep(30)
