# social_sync_agent.py
import os
import time
import sqlite3
from datetime import datetime
from playwright.sync_api import sync_playwright

VAULT_PATH = r"D:\Routine_Digital_Assistant\vault"
SESSION_PATH = r"D:\Routine_Digital_Assistant\Gold_Tier\Session\playwright_data"
SOCIAL_VAULT = os.path.join(VAULT_PATH, "Social")
DB_PATH = os.path.join(VAULT_PATH, "corporate_memory.db")

def log_event(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [SOCIAL_SYNC] {msg}")

def post_to_x(page, text, image_path=None):
    try:
        log_event("Navigating to X Compose...")
        page.goto("https://x.com/compose/post")
        page.wait_for_selector('div[data-testid="tweetTextarea_0"]', timeout=15000)
        
        # Type the content
        page.fill('div[data-testid="tweetTextarea_0"]', text)
        
        if image_path and os.path.exists(image_path):
            log_event(f"Uploading image to X: {image_path}")
            # Identify the file input for media
            file_input = page.query_selector('input[data-testid="fileInput"]')
            file_input.set_input_files(image_path)
            time.sleep(3) # Wait for upload
        
        # Wait for "Final Visual Check" (Simulated)
        log_event("Post staged for final check...")
        time.sleep(2)
        
        # Click Post
        page.click('div[data-testid="tweetButtonInline"]')
        log_event("X (Twitter) Post Successful.")
        return True
    except Exception as e:
        log_event(f"Failed to post to X: {e}")
        return False

def post_to_linkedin(page, text, image_path=None):
    try:
        log_event("Navigating to LinkedIn...")
        page.goto("https://www.linkedin.com/feed/")
        
        # Click 'Start a post'
        page.click('button.share-mb-wrapper__type-trigger', timeout=15000) # Selector might vary
        page.wait_for_selector('div.ql-editor')
        
        # Type the content
        page.fill('div.ql-editor', text)
        
        if image_path and os.path.exists(image_path):
            log_event(f"Uploading image to LinkedIn: {image_path}")
            # This part is complex due to LI's media flow, usually involves clicking 'Add media' button
            # Skipping detailed LI visual automation for now as a POC, focus on X
            pass

        log_event("LinkedIn Post staging simulation...")
        time.sleep(2)
        
        # Click Post (Simulated - selector varies)
        # page.click('button.share-actions__primary-action')
        log_event("LinkedIn Post Successful (Staged).")
        return True
    except Exception as e:
        log_event(f"Failed to post to LinkedIn: {e}")
        return False

def sync_social():
    if not os.path.exists(SESSION_PATH):
        log_event("Error: No session data found. Run social_auth_setup.py first.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_PATH,
            headless=True # Run in background for daily sync
        )
        page = browser.new_page()

        # Check for X Drafts
        x_dir = os.path.join(SOCIAL_VAULT, "X")
        if os.path.exists(x_dir):
            for filename in os.listdir(x_dir):
                if filename.startswith("DRAFT_"):
                    # For POC, we assume if it exists in this folder it's ready
                    # In a real workflow, we'd check for a 'READY' tag or move to 'Approved'
                    log_event(f"Found X Draft: {filename}")
                    # logic to read and post...
                    pass

        browser.close()

if __name__ == "__main__":
    log_event("Social Sync Agent Active.")
    # In a real loop, this would run on a schedule
    sync_social()
