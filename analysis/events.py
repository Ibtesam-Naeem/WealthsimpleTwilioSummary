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
driver = chrome_option()

def navigate_and_scrape_earnings():
    logging.info("Starting the earnings scraping process.")
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
                
                # Extracts Ticker / Company
                ticker_element = row.find_element(By.XPATH, ".//td[contains(@class, 'earnCalCompany')]/a")
                ticker = ticker_element.text.strip()
                logging.debug(f"Extracted ticker: {ticker}")

                # Extracts Forecast (eps)
                forecast_element = row.find_element(By.XPATH, ".//td[contains(@class, 'leftStrong')]")
                forecast = forecast_element.text.strip() if forecast_element else "N/A"
                logging.debug(f"Extracted Forecast: {forecast}")

                time_element = row.find_element(By.XPATH, ".//td[contains(@class, 'right time')]/span")
                # Check if the element exists and has the 'data-tooltip' attribute
                time_reporting = time_element.get_attribute("data-tooltip").strip() if time_element and time_element.get_attribute("data-tooltip") else "N/A"
                logging.debug(f"Extracted Time Reporting: {time_reporting}")

                # Extracts Market Cap
                market_cap_element = row.find_element(By.XPATH, ".//td[contains(@class, 'right')][position()=last()-1]")
                market_cap = market_cap_element.text.strip() if market_cap_element else "N/A"
                logging.debug(f"Extracted market cap: {market_cap}")

                # Markte Cap Filterer
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

                # Only Extract those which are >= 500B
                if numeric_market_cap >= 500_000_000:
                    data_entry = f"${ticker} - {market_cap} - {forecast} - {time_reporting}"
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

# def navigate_and_scrape_econ():
#     logging.info("Starting the economics scraping process.")
#     try:
#         driver.get("https://www.investing.com/economic-calendar/")
#         logging.info("Navigated to Investing.com economic calendar.")
#         driver.implicitly_wait(10)
#     except Exception as e:
#         logging.error(f"Error navigating to the website: {e}")
#         return  

#     try:
#         filter_button = driver.find_element(By.CLASS_NAME, "ecoButtonLine")
#         filter_button.click()
#         logging.info("Filter button clicked.")
#     except Exception as e:
#         logging.error(f"Error clicking the filter button: {e}")
#         return

#     try:
#         clear_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Clear')]"))
#         )
#         clear_button.click()
#         logging.info("Filters cleared.")
#     except Exception as e:
#         logging.error(f"Error clicking the Clear button: {e}")
#         return

#     try:
#         canada_checkbox = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//input[@name='country[]' and @value='6']"))
#         )
#         canada_checkbox.click()
#         logging.info("Canada checkbox selected.")
#     except Exception as e:
#         logging.error(f"Error selecting Canada checkbox: {e}")
#         return

#     try:
#         us_checkbox = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//input[@name='country[]' and @value='5']"))
#         )
#         us_checkbox.click()
#         logging.info("United States checkbox selected.")
#     except Exception as e:
#         logging.error(f"Error selecting United States checkbox: {e}")
#         return

#     try:
#         importance_checkbox = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//input[@name='importance[]' and @value='3']"))
#         )
#         importance_checkbox.click()
#         logging.info("Importance level 3 checkbox selected.")
#     except Exception as e:
#         logging.error(f"Error selecting importance level 3: {e}")
#         return

#     try:
#         apply_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Apply')]"))
#         )
#         apply_button.click()
#         logging.info("Filters applied successfully.")
#     except Exception as e:
#         logging.error(f"Error clicking the Apply button: {e}")
#         return

#     logging.info("Economic calendar filtering and scraping process completed.")

#     try:
#         # Wait for the table to load
#         table = WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "js-economic-table"))
#         )
#         logging.info("Economic calendar table successfully loaded.")

#         # Locate all rows in the table
#         rows = driver.find_elements(By.XPATH, "//table[contains(@class, 'js-economic-table')]//tbody/tr")
#         logging.info(f"Found {len(rows)} rows in the table.")

#         economic_data = []
#         current_date = None

#         for row in rows:
#             try:
#                 # Check if the row is a date header
#                 if "colspan" in row.get_attribute("outerHTML"):
#                     current_date = row.text.strip()
#                     logging.info(f"Processing data for date: {current_date}")
#                     continue  # Skip to the next row

#                 # Extract the columns for currency, event, forecast, and previous
#                 columns = row.find_elements(By.TAG_NAME, "td")

#                 # Ensure the row has enough columns
#                 if len(columns) < 4:
#                     logging.warning("Row doesn't have enough columns, skipping.")
#                     continue

#                 # Extract data
#                 currency = columns[0].text.strip()
#                 event = columns[1].text.strip()
#                 forecast = columns[2].text.strip() if len(columns) > 2 else "N/A"
#                 previous = columns[3].text.strip() if len(columns) > 3 else "N/A"

#                 # Append data to the list
#                 economic_data.append({
#                     "Date": current_date,
#                     "Currency": currency,
#                     "Event": event,
#                     "Forecast": forecast,
#                     "Previous": previous
#                 })

#                 logging.debug(f"Extracted row: {currency}, {event}, {forecast}, {previous}")

#             except Exception as e:
#                 logging.error(f"Error processing row: {e}")
#                 continue

#         logging.info(f"Scraped {len(economic_data)} entries from the economic calendar.")
#         return economic_data

#     except Exception as e:
#         logging.error(f"Error scraping the economic calendar table: {e}")
#         return []
    
# navigate_and_scrape_econ()
