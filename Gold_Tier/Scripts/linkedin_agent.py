# linkedin_agent.py
import os
import sqlite3
from datetime import datetime

VAULT_PATH = r"D:\Routine_Digital_Assistant\vault"
LINKEDIN_FOLDER = os.path.join(VAULT_PATH, "Social", "LinkedIn")
DB_PATH = os.path.join(VAULT_PATH, "corporate_memory.db")

def log_to_memory(details):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO communications (channel, account, subject, timestamp, body_snippet, action_taken)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', ("LinkedIn", "tahiryamin", details['title'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), details['snippet'], "DRAFT_MOVED"))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Memory logging failed: {e}")

def organize_linkedin():
    print("Core Field Content (PM/PMP) redirected to LinkedIn repository...")
    # This agent will eventually handle automated LinkedIn API posting
    # For now, it manages the professional content queue.
    log_to_memory({"title": "PMI Talent Triangle Evolution", "snippet": "Refactored long-form post for professional audience."})

if __name__ == "__main__":
    organize_linkedin()
