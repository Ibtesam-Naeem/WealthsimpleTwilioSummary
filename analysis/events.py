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

def navigate_and_scrape_earnings():
    try:
        driver.get("https://www.investing.com/earnings-calendar/")
        
        table = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "earningsCalendarData"))
        )
        logging.info("Earnings table loaded.")

        today_date = datetime.now().strftime("%A, %B %d, %Y")  # e.g., "Monday, January 13, 2025"
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%A, %B %d, %Y")  # e.g., "Tuesday, January 14, 2025"

        rows = driver.find_elements(By.XPATH, "//table[@id='earningsCalendarData']//tbody/tr")
        logging.info(f"Found {len(rows)} rows.")

        current_date = None

        for row in rows:
            try:
                
                if "colspan" in row.get_attribute("outerHTML"):
                    header_text = row.text.strip()
                    if header_text in [today_date, tomorrow_date]:
                        current_date = header_text
                    else:
                        current_date = None 
                    continue

                # Skip rows which are not todays date or tomorrows
                if current_date not in [today_date, tomorrow_date]:
                    continue

                ticker_element = row.find_element(By.XPATH, ".//td[contains(@class, 'earnCalCompany')]/a")
                ticker = ticker_element.text.strip()

                market_cap_element = row.find_element(By.XPATH, ".//td[contains(@class, 'right')][position()=last()-1]")
                market_cap = market_cap_element.text.strip() if market_cap_element else "N/A"

                if market_cap == "N/A":
                    continue

                # Converts Market Cap to a number for filter process
                multiplier = 1
                if market_cap.endswith("B"):
                    multiplier = 1_000_000_000
                elif market_cap.endswith("M"):
                    multiplier = 1_000_000
                
                numeric_market_cap = float(market_cap[:-1]) * multiplier  

                # Filters out those under 100M in mkt cap
                if numeric_market_cap >= 100_000_000:
                    print(f"${ticker} - {market_cap}")

            except Exception as e:
                logging.warning(f"Error processing row: {e}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    navigate_and_scrape_earnings()
