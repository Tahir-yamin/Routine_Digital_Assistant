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
    Focus: AI Sovereignty, Open Source, and Nanabanana Tech. (NOT PM field)
    """
    # 1. Pattern Interrupt Hook
    hook = f"💀 'Local-First' is no longer a niche preference. It's a survival strategy.\n\nI just built a relational memory brain (SQLite) for my AI Employee that runs 100% on my local D: drive. \n\nNo cloud. No 429 quota errors. Just Sovereign Intelligence. 🧵👇"
    
    # 2. Value Points
    points = [
        "1/ The Problem: Most agents are thin wrappers around APIs. When the server goes down, your 'employee' dies. Local-first means your business logic is permanent.",
        "2/ Tech Stack: I'm using a Watchdog perception layer + Ollama (llama3.2) + SQLite Corporate Memory. It triages my Gmail and drafts my X posts while I sleep.",
        "3/ The 'Corporate Memory' database indexes every task I complete, creating a relational graph of project successes and bottlenecks.",
        "4/ This isn't just automation. It's an architecture for the future of Sovereign Engineering."
    ]
    
    # 3. Engagement CTA
    cta = "Are you building on rented land (Cloud) or are you building a Sovereign Fortress?\n\nDrop a 'BRAIN' below if you want the SQLite schema I'm using. 🧠🏗️\n\n#AI #SovereignAI #OpenSource #Nanabanana #LocalFirst"

    full_thread = f"# 📝 X POST DRAFT: Sovereign Memory Brain\n**Account Context**: tahir_yamin_ (X/Twitter)\n**Status**: PENDING APPROVAL\n\n---\n\n"
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
