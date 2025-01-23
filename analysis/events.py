from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from config.chrome_options import chrome_option
import logging
import time
from datetime import datetime

def trading_view_calendar():
    """
    Navigates to Trading View's Earnings Calendar page and scrapes data for stocks with Market Cap > 500M.
    """
    try:
        driver = chrome_option()
        logging.info("Beginning scraping process")
        driver.get("https://www.tradingview.com/markets/stocks-usa/earnings/")
        logging.info("Navigated to Trading View's earnings calendar page")
    except Exception as e:
        logging.error("Failed to navigate to Trading View's earnings calendar page")
        return []

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tv-data-table"))
    )
    rows = driver.find_elements(By.CLASS_NAME, "tv-data-table__row")

    try:
        earnings_data = []
        for row in rows:
            try:
                ticker_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='name']")
                ticker_full = ticker_element.text.strip()
                ticker_d = ticker_full.split("\n")[0]
                ticker = "".join(ticker_d[:-1])

                market_cap_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='market_cap_basic']")
                market_cap = market_cap_element.text.strip("USD")

                # Convert Market Cap to a numeric value
                if market_cap in ["—", "", None]:
                    market_cap_value = 0
                elif market_cap.endswith("K"):
                    market_cap_value = float(market_cap[:-1]) * 1_000
                elif market_cap.endswith("M"):
                    market_cap_value = float(market_cap[:-1]) * 1_000_000
                elif market_cap.endswith("B"):
                    market_cap_value = float(market_cap[:-1]) * 1_000_000_000
                elif market_cap.endswith("T"):
                    market_cap_value = float(market_cap[:-1]) * 1_000_000_000_000
                else:
                    market_cap_value = float(market_cap)

                if market_cap_value <= 100_000_000_000:
                    continue

                eps_estimate_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_per_share_forecast_next_fq']")
                eps_estimate = eps_estimate_element.text.strip("USD") if eps_estimate_element else "N/A"

                revenue_forecast_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='revenue_forecast_next_fq']")
                revenue_forecast = revenue_forecast_element.text.strip("USD") if revenue_forecast_element else "N/A"
                                
                earnings_data.append({
                    "Ticker": ticker,
                    "Market Cap": market_cap,
                    "EPS Estimate": eps_estimate,
                    "Revenue Forecast": revenue_forecast
                    })

            except Exception as e:
                logging.error(f"Error processing row: {e}")

            earnings_messages = [
            f"{data['Ticker']} | {data['Market Cap']} | {data['EPS Estimate']} | {data['Revenue Forecast']}"
            for data in earnings_data
            ]
        return earnings_messages
    
    finally:
        driver.quit()
        logging.info("Scraping process completed.")