import sys
import os
import json
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

# Get project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extract_selected_emails():
    """
    Connects to Gmail using a persistent context and stealth mode to bypass security checks.
    """
    user_data_dir = os.path.join(PROJECT_ROOT, "data", "user_data")
    os.makedirs(user_data_dir, exist_ok=True)

    with sync_playwright() as p:
        # Launch with persistent context to save login state
        # We use common arguments to look like a regular browser
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        # Apply stealth to hide automation
        Stealth().apply_stealth_sync(page)
        
        print("Opening Gmail... If you are not logged in, please do so now.")
        print("The browser will save your session in data/user_data.")
        page.goto("https://mail.google.com")
        
        # Wait for user to navigate to an email or for the email body to appear
        print("Waiting for an email to be opened (looking for Gmail body selector)...")
        
        try:
            # Gmail body selector (broad)
            page.wait_for_selector(".a3s", timeout=120000) # Wait up to 2 minutes for user login/nav
            
            # Extract basic info
            subject = page.title()
            body = page.inner_text(".a3s")
            
            email_data = {
                "subject": subject,
                "body": body,
                "platform": "Gmail"
            }
            
            data_dir = os.path.join(PROJECT_ROOT, "data")
            os.makedirs(data_dir, exist_ok=True)
            output_path = os.path.join(data_dir, "extracted_email.json")
            
            with open(output_path, "w") as f:
                json.dump(email_data, f)
                
            print(f"Success! Extracted: {subject}")
            
        except Exception as e:
            print(f"Extraction failed or timed out: {e}")
            print("Make sure you have an email message open on the screen.")
        
        # Keep browser open for a few seconds so user sees the success/failure
        import time
        time.sleep(5)
        context.close()

if __name__ == "__main__":
    extract_selected_emails()
