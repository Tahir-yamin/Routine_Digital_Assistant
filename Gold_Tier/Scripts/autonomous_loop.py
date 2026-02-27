# autonomous_loop.py
import os
import time
import re
from datetime import datetime

VAULT_PATH = r"D:\Routine_Digital_Assistant\vault"
PLANS_PATH = os.path.join(VAULT_PATH, "Plans")
DONE_PATH = os.path.join(VAULT_PATH, "Done")
AUDIT_LOG = os.path.join(VAULT_PATH, "System_Audit.log")

def log_event(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [GOLD_LOOP] {msg}")
    with open(AUDIT_LOG, "a", encoding='utf-8') as f:
        f.write(f"[{ts}] [GOLD_LOOP] {msg}\n")

def execute_step(step_text):
    """
    Simulates the actual work for a plan step.
    In a full implementation, this calls specific tool/skills.
    """
    log_event(f"Executing step: {step_text}")
    # Simulating work...
    time.sleep(2) 
    return True

def run_ralph_wiggum_cycle():
    """
    The Ralph Wiggum Loop: Persistent Autonomous Execution.
    """
    if not os.path.exists(PLANS_PATH): return

    plan_files = [f for f in os.listdir(PLANS_PATH) if f.endswith(".md")]
    
    for plan_file in plan_files:
        plan_path = os.path.join(PLANS_PATH, plan_file)
        with open(plan_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        updated_lines = []
        changes_made = False
        all_done = True

        for line in lines:
            # Look for an unchecked checkbox [ ]
            if "- [ ]" in line:
                # We found a pending step!
                # Extract the text after the [ ]
                step_match = re.search(r"- \[ \]\s*(.*)", line)
                if step_match:
                    step_desc = step_match.group(1)
                    
                    # Execute the step
                    success = execute_step(step_desc)
                    if success:
                        line = line.replace("- [ ]", "- [x]")
                        changes_made = True
                        log_event(f"Step completed: {step_desc}")
                    else:
                        all_done = False
                else:
                    all_done = False
            
            updated_lines.append(line)

        if changes_made:
            with open(plan_path, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
            
            # If all steps are now [x], move to Done and Index in Memory
            if all_done:
                log_event(f"Strategic Plan Fully Executed: {plan_file}. Moving to Archive.")
                archive_path = os.path.join(DONE_PATH, plan_file)
                os.rename(plan_path, archive_path)
                
                # --- GOLD TIER CORPORATE MEMORY INDEXING ---
                try:
                    import sqlite3
                    DB_PATH = os.path.join(VAULT_PATH, "corporate_memory.db")
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    with open(archive_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    cursor.execute('''
                    INSERT OR IGNORE INTO tasks (file_name, title, status, created_at, plan_content)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (plan_file, plan_file.replace("PLAN_", "").replace(".md", ""), "DONE", datetime.now().strftime("%Y-%m-%d"), content))
                    conn.commit()
                    conn.close()
                    log_event(f"Relational Memory Updated for: {plan_file}")
                except Exception as e:
                    log_event(f"Memory update failed: {e}")
                # -------------------------------------------

if __name__ == "__main__":
    log_event("Ralph Wiggum Loop (Gold Tier) Active.")
    while True:
        run_ralph_wiggum_cycle()
        time.sleep(60) # Full sync every minute
