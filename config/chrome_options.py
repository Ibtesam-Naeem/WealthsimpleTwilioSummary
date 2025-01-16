import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging

def chrome_option():
    """
    Configures and returns a Chrome WebDriver instance with a specific user profile.
    - Uses the main Chrome profile to avoid 2FA and retain cookies.
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  
    
    # Use main Chrome profile to retain cookies and avoid 2FA
    chrome_options.binary_location = os.getenv("CHROME_BINARY_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    chrome_options.add_argument(f"user-data-dir={os.getenv('CHROME_USER_DATA_PATH', '/default/path/to/user-data')}")
    chrome_options.add_argument(f"profile-directory={os.getenv('CHROME_PROFILE', 'Default')}")

    service = Service(executable_path='/usr/local/bin/chromedriver')
    
    return webdriver.Chrome(service=service, options=chrome_options)
