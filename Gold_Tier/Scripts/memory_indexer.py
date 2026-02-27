# memory_indexer.py
import os
import sqlite3
import re
from datetime import datetime

VAULT_PATH = r"D:\Routine_Digital_Assistant\vault"
DB_PATH = os.path.join(VAULT_PATH, "corporate_memory.db")
DONE_PATH = os.path.join(VAULT_PATH, "Done")

def log_event(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [MEMORY] {msg}")

def index_completed_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if not os.path.exists(DONE_PATH): return

    files = [f for f in os.listdir(DONE_PATH) if f.endswith(".md")]
    
    for filename in files:
        file_path = os.path.join(DONE_PATH, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract basic metadata
            title = filename.replace(".md", "").replace("PLAN_", "").replace("ACTION_", "")
            status = "DONE"
            
            # Simple metadata extraction logic
            created_at = None
            date_match = re.search(r"\d{4}-\d{2}-\d{2}", content)
            if date_match:
                created_at = date_match.group(0)
            
            # Insert into DB (ignore if exists)
            cursor.execute('''
            INSERT OR IGNORE INTO tasks (file_name, title, status, created_at, plan_content)
            VALUES (?, ?, ?, ?, ?)
            ''', (filename, title, status, created_at, content))
            
            log_event(f"Indexed task: {filename}")
            
        except Exception as e:
            log_event(f"Error indexing {filename}: {e}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    log_event("Starting Memory Indexing...")
    index_completed_tasks()
    log_event("Indexing complete.")
