@echo off
TITLE Routine Digital Assistant - GOLD TIER (Sovereign Autonomy)
cd /d "D:\Routine_Digital_Assistant"

echo [SYSTEM] Starting Sovereign Swarm...

:: 1. Perception Watcher (Inbox -> Needs_Action)
start "Perception Watcher" /min python Silver_Tier/Scripts/perception_watcher.py

:: 2. Gmail Multi-Watcher (GMAIL -> Inbox)
start "Gmail Sync" /min python Silver_Tier/Scripts/gmail_watcher.py

:: 3. Reasoning Agent (Needs_Action -> Plans)
start "Reasoning Agent" /min python Silver_Tier/Scripts/reasoning_agent.py

:: 4. Ralph Wiggum Loop (Plans -> DONE / Execution)
start "Autonomous Loop" /min python Gold_Tier/Scripts/autonomous_loop.py

:: 5. Drafting Agent
start "Drafting Agent" /min python Silver_Tier/Scripts/drafting_agent.py

echo [SUCCESS] Routine Digital Assistant is now running in FULL AUTONOMOUS MODE.
echo [INFO] Monitor Dashboard.md in Obsidian for live updates.
pause
