@echo off
TITLE Routine Digital Assistant - SILVER TIER ORCHESTRATOR
cd /d "D:\Routine_Digital_Assistant"

echo [SYSTEM] Launching Autonomous Sub-Agents...

:: Start Perception Watcher
start "RDA Perception" /min C:\Python313\python.exe Silver_Tier\Scripts\perception_watcher.py

:: Start Reasoning Agent (Digital Intelligence)
start "RDA Reasoning" /min C:\Python313\python.exe Silver_Tier\Scripts\reasoning_agent.py

:: Start Drafting Agent (Outreach/Drafting)
start "RDA Drafting" /min C:\Python313\python.exe Silver_Tier\Scripts\drafting_agent.py

:: Start Gmail Watcher (External Perception)
start "RDA Gmail" /min C:\Python313\python.exe Silver_Tier\Scripts\gmail_watcher.py

echo.
echo ==============================================
echo    ROUTINE DIGITAL ASSISTANT IS ACTIVE
echo ==============================================
echo [STAGE] SILVER TIER (REASONING ^& OUTREACH ACTIVE)
echo [VAULT] D:\Routine_Digital_Assistant\vault
echo.
echo [INFO] Perception: Monitoring /Inbox
echo [INFO] Reasoning:  Generating /Plans
echo [INFO] Outreach:   Generating /Drafts
echo [INFO] Gmail:      Monitoring Incoming Mail
echo.
echo ----------------------------------------------
echo Press any key to shutdown all sub-agents...
pause > nul

echo [SYSTEM] Shutting down sub-agents...
taskkill /FI "WINDOWTITLE eq RDA Perception" /F > nul
taskkill /FI "WINDOWTITLE eq RDA Reasoning" /F > nul
taskkill /FI "WINDOWTITLE eq RDA Drafting" /F > nul
taskkill /FI "WINDOWTITLE eq RDA Gmail" /F > nul
echo [SUCCESS] System Offline.
pause
