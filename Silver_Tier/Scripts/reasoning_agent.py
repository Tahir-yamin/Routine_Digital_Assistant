import os
import time
from datetime import datetime

# CONFIGURATION
VAULT_PATH = r"D:\Routine_Digital_Assistant\vault"
ACTION_PATH = os.path.join(VAULT_PATH, "Needs_Action")
PLANS_PATH = os.path.join(VAULT_PATH, "Plans")
DASHBOARD_PATH = os.path.join(VAULT_PATH, "Dashboard.md")

def log_activity(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [THINK] {msg}")
    log_file = os.path.join(VAULT_PATH, "System_Audit.log")
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(f"[{timestamp}] [THINK] {msg}\n")

def generate_plan(action_file):
    """
    Silver Tier Reasoning:
    Analyzes a task and creates a structured Plan.md with checkboxes.
    """
    if not action_file.endswith(('.md', '.txt')):
        log_activity(f"Skipping non-text file for intelligence-based planning: {action_file}")
        return

    file_path = os.path.join(ACTION_PATH, action_file)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        log_activity(f"Failed to read {action_file}: {str(e)}")
        return

    plan_name = f"PLAN_{action_file.replace('ACTION_', '')}"
    plan_path = os.path.join(PLANS_PATH, plan_name)

    # Simplified AI logic for "Drafting"
    # In a real scenario, this would call an LLM API. 
    # Here we simulate the specialized expertise of a Digital Assistant.
    
    # --- OLLAMA AI REASONING (Silver Tier Intelligence) ---
    import requests

    def get_ai_plan(title, context):
        prompt = f"""
        Act as a Senior Planning Engineer's Strategic Assistant.
        Generate a detailed implementation plan for this task:
        TASK: {title}
        CONTEXT: {context}
        
        Format as Markdown:
        ## 📋 SUMMARY
        [Brief overview]
        
        ## 🛠️ PROPOSED ACTIONS
        - [ ] [Specific action 1]
        - [ ] [Specific action 2]
        
        ## 🛡️ SAFETY GUARDRAILS
        [Potential risks/guards]
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
            return response.json().get("response", "Error generating plan.")
        except Exception as e:
            return f"Error connecting to Ollama: {e}"

    log_activity(f"Consulting AI Brain for strategy on: {action_file}")
    plan_content = f"# Executive Plan: {action_file.replace('ACTION_', '').replace('.md', '')}\n"
    plan_content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    plan_content += f"**Status**: DRAFT (Awaiting Approval)\n"
    plan_content += f"**Reference**: {action_file}\n\n"
    plan_content += get_ai_plan(action_file, content)
    plan_content += "\n\n---\n*Created by Routine Digital Assistant | Silver Tier Operations (Ollama Powered)*"
    # ----------------------------------------------------

    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(plan_content)
    
    # Move original action to specialized processing folder or archive
    # (Optional: In Bronze we leave it in Needs_Action, in Silver we move it)
    log_activity(f"Created Strategic Plan: {plan_name}")

def update_status():
    """
    Scan ACTION folder and generate plans for anything that doesn't have one.
    """
    if not os.path.exists(ACTION_PATH): return
    if not os.path.exists(PLANS_PATH): os.makedirs(PLANS_PATH)

    actions = [f for f in os.listdir(ACTION_PATH) if f.startswith("ACTION_")]
    existing_plans = [f.replace("PLAN_", "ACTION_") for f in os.listdir(PLANS_PATH)]

    for action in actions:
        if action not in existing_plans:
            log_activity(f"New action detected: {action}. Commencing reasoning...")
            generate_plan(action)

if __name__ == "__main__":
    log_activity("Silver Tier Reasoning Loop Initialized.")
    while True:
        update_status()
        time.sleep(15)
