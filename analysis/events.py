
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
                # Extract Ticker
                ticker_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='name']")
                ticker_full = ticker_element.text.strip()
                ticker_d = ticker_full.split("\n")[0]
                ticker = "".join(ticker_d[:-1])

                # Extract Market Cap
                market_cap_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='market_cap_basic']")
                market_cap = market_cap_element.text.strip("USD")

                # Extract EPS Estimate
                eps_estimate_element = row.find_element(By.CSS_SELECTOR, "[data-field-key='earnings_per_share_forecast_next_fq']")
                eps_estimate = eps_estimate_element.text.strip("USD") if eps_estimate_element else "N/A"

                # Extract Revenue Forecast
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
            f"{data['Ticker']}, {data['Market Cap']} | {data['EPS Estimate']} | {data['Revenue Forecast']}"
            for data in earnings_data
            ]
        return earnings_messages
    
    finally:
        driver.quit()


        