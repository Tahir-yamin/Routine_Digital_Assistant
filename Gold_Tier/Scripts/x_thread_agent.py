# x_thread_agent.py
import os
import sqlite3
import re
from datetime import datetime

VAULT_PATH = r"D:\Routine_Digital_Assistant\vault"
DRAFTS_FOLDER = os.path.join(VAULT_PATH, "Drafts")
DB_PATH = os.path.join(VAULT_PATH, "corporate_memory.db")

X_ALGO_RULES = {
    "hook_limit": 250,
    "thread_max": 7,
    "media_penalty_avoidance": True, # Use native upload simulation
}

def log_to_memory(details):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO communications (channel, account, subject, timestamp, body_snippet, action_taken)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', ("X", "Tahir-Yamin", details['hook'][:50], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), details['hook'], "DRAFT_CREATED"))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Memory logging failed: {e}")

def generate_x_thread(source_content, title):
    """
    Transforms content into a high-performance X thread using the 'X-Viral-Optimizer' pattern.
    """
    # 1. Pattern Interrupt Hook
    hook = f"🚀 Most Project Managers are still using 2010 playbooks in a 2026 AI world.\n\nI just automated my entire Planning workflow using a Sovereign AI Employee. \n\nHere’s how the 'PMI Talent Triangle' changes when your 'Technical mastery' is code. 🧵👇"
    
    # 2. Value Points (Extracted from source context)
    points = [
        "1/ Technical Mastery isn't just knowing P6. It's about 'Ways of Working'—integrating MAS (Multi-Agent Systems) into your schedule logic to detect bottlenecks before they happen.",
        "2/ Power Skills: In an AI-driven environment, your leadership isn't about tracking hours. It's about Emotional Intelligence (EQ) to manage the human-AI interface on-site.",
        "3/ Business Acumen: Strategic alignment means using real-time financial telemetry (Odoo/SAP integration) to pivot project budgets instantly, not monthly.",
        "4/ The Result? A shift from a 'Scheduler' to a 'Business Strategist'. AI handles the data; you handle the decisions."
    ]
    
    # 3. Engagement CTA
    cta = "Are you still tracking projects manually, or are you building the machines of the future?\n\nDrop a 'PM-AI' below if you want the blueprint. 🏗️🤖\n\n#ProjectManagement #PMP #AIEmployee #ConstructionTech"

    full_thread = f"# 📝 X THREAD DRAFT: {title}\n**Account Context**: Tahir-Yamin (X/Twitter)\n**Status**: PENDING APPROVAL\n\n---\n\n"
    full_thread += f"**Tweet 1 (The Hook)**:\n{hook}\n\n"
    for i, p in enumerate(points):
        full_thread += f"**Tweet {i+2}**:\n{p}\n\n"
    full_thread += f"**Tweet {len(points)+2} (CTA)**:\n{cta}"
    
    return full_thread

def process_latest_done():
    """
    Finds the latest 'Done' task and drafts an X thread for it.
    """
    done_path = os.path.join(VAULT_PATH, "Done")
    if not os.listdir(done_path): return

    # Get latest summary/done item
    latest_file = sorted(os.listdir(done_path), key=lambda x: os.path.getmtime(os.path.join(done_path, x)), reverse=True)[0]
    file_path = os.path.join(done_path, latest_file)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    thread_content = generate_x_thread(content, latest_file)
    
    draft_filename = f"DRAFT_X_THREAD_{latest_file.replace('.md', '')}.md"
    draft_path = os.path.join(DRAFTS_FOLDER, draft_filename)
    
    with open(draft_path, "w", encoding='utf-8') as f:
        f.write(thread_content)
    
    log_to_memory({"hook": thread_content[:200]})
    print(f"X Thread Draft created: {draft_filename}")

if __name__ == "__main__":
    process_latest_done()
