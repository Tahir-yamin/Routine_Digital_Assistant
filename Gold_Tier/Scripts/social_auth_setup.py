# social_auth_setup.py
import sys
import os
from playwright.sync_api import sync_playwright

SESSION_PATH = r"D:\Routine_Digital_Assistant\Gold_Tier\Session\playwright_data"

def run_auth():
    print("--- 🛡️ ROUTINE SOCIAL AUTH SETUP ---")
    print(f"Storing session data in: {SESSION_PATH}")
    print("Action Required: Please log in to X (Twitter) and LinkedIn in the browser window.")
    print("Once logged in, close the browser window to save your session.")
    
    with sync_playwright() as p:
        # Launch persistent context
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_PATH,
            headless=False,
            args=["--start-maximized"]
        )
        
        page = browser.new_page()
        page.goto("https://x.com/login")
        print("Waiting for you to log in to X...")
        
        # New page for LinkedIn
        page2 = browser.new_page()
        page2.goto("https://www.linkedin.com/login")
        print("Waiting for you to log in to LinkedIn...")
        
        # Keep it open until user closes manually
        while len(browser.pages) > 0:
            try:
                # Need a small sleep to avoid 100% CPU
                browser.request.get("http://localhost:1") # Just a dummy to keep loop alive
            except:
                pass
            if not browser.is_connected():
                break
            # We just wait for the user to close the browser
            import time
            time.sleep(1)

    print("--- ✅ AUTH SETUP COMPLETE ---")
    print("Your sessions are now saved locally.")

if __name__ == "__main__":
    run_auth()
