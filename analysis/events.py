import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
import os
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from config.chrome_options import chrome_option
import logging
import time
from datetime import datetime, timedelta

driver = chrome_option()

TODAY = "Today"
TOMORROW = "Tomorrow"

def market_cap_filter(value):
    """
    Market Cap filter
    """
    MEGA_CAP = 200_000_000_000_000
    LARGE_CAP = 10_000_000_000_000
    MID_CAP = 2_000_000_000
    SMALL_CAP = 300_000_000
    MICRO_CAP = 50_000_000

    if value >= MEGA_CAP:
        return "Mega Cap"
    elif value >= LARGE_CAP:
        return "Large Cap"
    elif value >= MID_CAP:
        return "Mid Cap"
    elif value >= SMALL_CAP:
        return "Small Cap"
    elif value >= MICRO_CAP:
        return "Micro Cap"
    else:
        return "Nano Cap or smaller"
    
def navigate_and_load_page():
    try:
        driver.get("https://www.tradingview.com/markets/stocks-usa/earnings/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button'))  # Wait for any button
        )
        logging.info("Navigated to Trading View.")
        return True
    except Exception as e:
        logging.error(f"Failed to navigate: {e}")
        return False

navigate_and_load_page()
time.sleep(20)
