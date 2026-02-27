@echo off
TITLE Routine Social Auth Setup
cd /d "D:\Routine_Digital_Assistant"
echo [SYSTEM] Launching Social Auth Browser using Global Python...
C:\Python313\python.exe Gold_Tier\Scripts\social_auth_setup.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to launch with Global Python. Trying default...
    python Gold_Tier\Scripts\social_auth_setup.py
)
echo [SUCCESS] Session saved. You can now use LAUNCH_GOLD.bat.
pause
