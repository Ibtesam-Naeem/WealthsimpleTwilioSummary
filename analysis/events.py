import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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

def navigate_and_scrape_earnings():
    logging.info("Starting the earnings scraping process.")
    driver = chrome_option()
    try:
        driver.get("https://www.investing.com/earnings-calendar/")
        logging.info("Navigated to Investing.com earnings calendar.")

        table = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "earningsCalendarData"))
        )
        logging.info("Earnings table successfully loaded.")

        today_date = datetime.now().strftime("%A, %B %d, %Y")
        logging.debug(f"Today's date: {today_date}")

        rows = driver.find_elements(By.XPATH, "//table[@id='earningsCalendarData']//tbody/tr")
        logging.info(f"Found {len(rows)} rows in the table.")

        current_date = None
        earnings_data = []

        for row in rows:
            try:
                if "colspan" in row.get_attribute("outerHTML"):
                    header_text = row.text.strip()
                    if header_text in [today_date]:
                        current_date = header_text
                        logging.info(f"Processing data for date: {current_date}")
                    else:
                        current_date = None
                    continue

                if current_date not in [today_date]:
                    logging.debug("Skipping row not matching today's date.")
                    continue

                ticker_element = row.find_element(By.XPATH, ".//td[contains(@class, 'earnCalCompany')]/a")
                ticker = ticker_element.text.strip()
                logging.debug(f"Extracted ticker: {ticker}")

                market_cap_element = row.find_element(By.XPATH, ".//td[contains(@class, 'right')][position()=last()-1]")
                market_cap = market_cap_element.text.strip() if market_cap_element else "N/A"
                logging.debug(f"Extracted market cap: {market_cap}")

                if market_cap == "N/A":
                    logging.warning("Market cap is unavailable; skipping row.")
                    continue

                if market_cap.endswith("T"):
                    multiplier = 1_000_000_000_000
                elif market_cap.endswith("B"):
                    multiplier = 1_000_000_000
                elif market_cap.endswith("M"):
                    multiplier = 1_000_000
                else:
                    multiplier = 1

                numeric_market_cap = float(market_cap[:-1]) * multiplier
                logging.debug(f"Numeric market cap: {numeric_market_cap}")

                if numeric_market_cap >= 500_000_000:
                    data_entry = f"${ticker} - {market_cap}"
                    earnings_data.append(data_entry)
                    logging.info(f"Added earnings data: {data_entry}")
                else:
                    logging.debug(f"Company {ticker} below minimum market cap threshold; skipping.")
            except Exception as e:
                logging.warning(f"Error processing row: {e}")

        if not earnings_data:
            logging.info("No significant earnings data found for today.")
        else:
            logging.info(f"Earnings data collected: {earnings_data}")
        return earnings_data

    except Exception as e:
        logging.error(f"An error occurred during scraping: {e}")
        return []
    finally:
        driver.quit()
        logging.info("Browser closed.")