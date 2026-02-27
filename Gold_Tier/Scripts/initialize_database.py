# initialize_database.py
import sqlite3
import os

DB_PATH = r"D:\Routine_Digital_Assistant\vault\corporate_memory.db"

def initialize_db():
    print(f"Initializing Corporate Memory Database at: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Tasks Table (History of everything processed)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT UNIQUE,
        title TEXT,
        category TEXT,
        status TEXT,
        created_at DATETIME,
        completed_at DATETIME,
        plan_content TEXT
    )
    ''')
    
    # 2. Audit Logs Table (Relational logging for indexing)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS system_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME,
        subsystem TEXT,
        event_type TEXT,
        message TEXT,
        details TEXT
    )
    ''')
    
    # 3. Communications Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS communications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel TEXT,
        account TEXT,
        sender TEXT,
        subject TEXT,
        timestamp DATETIME,
        body_snippet TEXT,
        action_taken TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_db()
