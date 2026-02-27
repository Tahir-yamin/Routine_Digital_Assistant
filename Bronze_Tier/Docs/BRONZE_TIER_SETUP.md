# BRONZE TIER SETUP GUIDE

To initialize the baseline Routine Digital Assistant (Bronze Tier):

1. **Vault Setup**:
   - Ensure the folder `D:\Routine_Digital_Assistant\vault` exists.
   - Verify `Company_Handbook.md` contains the basic operational logic.
   
2. **Environment**:
   - Install dependencies: `pip install google-api-python-client google-auth-oauthlib watchdog requests`.
   - Place `credentials.json` in the Scripts directory.

3. **Execution**:
   - Run the foundation watcher:
     ```powershell
     python Bronze_Tier/Scripts/gmail_watcher_foundation.py
     ```

4. **Monitoring**:
   - Open Obsidian at `D:\Routine_Digital_Assistant\vault`.
   - Monitor `Dashboard.md` for AI activity.
