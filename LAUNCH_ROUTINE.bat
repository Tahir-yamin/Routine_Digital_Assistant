@echo off
TITLE Routine Digital Assistant - BRONZE TIER
cd /d "D:\Routine_Digital_Assistant"
echo [SUCCESS] Initializing Routine Perception Watcher...
echo [CONSOLE] Processing Vault: D:\Routine_Digital_Assistant\vault
C:\Python313\python.exe Silver_Tier\Scripts\perception_watcher.py
pause
