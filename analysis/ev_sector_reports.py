import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
from notifications.twilio_sms import send_sms
from config.chrome_options import chrome_option

driver = chrome_option()

def tesla_delivery_report():
    """
    Continuously checks Tesla's Investor Relations page for
    the latest press release.
    Extracts total production and delivery numbers when found.
    """
    while True:
        try:
            driver.get("https://ir.tesla.com/#quarterly-disclosure")
            print("Navigated to Tesla IR page.")

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//table"))
            )
            rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

            press_release_link = None
            for row in rows:
                try:
                    press_release_link = row.find_element(By.XPATH, ".//a[contains(text(), 'Press Release')]")
                    break  
                
                except NoSuchElementException:
                    continue

            if not press_release_link:
                print("Press Release link not found. Retrying in 1 minute...")
                time.sleep(60)
                continue

            link = press_release_link.get_attribute("href")
            driver.get(link)
            print(f"Opened press release page: {link}")

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table[1]"))
            )

            table = driver.find_element(By.XPATH, "//table[1]")
            rows = table.find_elements(By.XPATH, ".//tr")

            for row in rows:
                columns = row.find_elements(By.XPATH, ".//td")
                if len(columns) >= 3 and "Total" in columns[0].text:
                    total_production = columns[1].text.strip()
                    total_deliveries = columns[2].text.strip()
                    message = f"Total Production: {total_production}\nTotal Deliveries: {total_deliveries}"
                    print(message)
                    return message
            time.sleep(60)

        except Exception as e:
            driver.quit

def nio_latest_news():
    """
    Continuously checks NIO's News Releases page for the latest
    article containing the current month and year.
    Extracts total production and delivery numbers when found.
    """
    driver.get("https://ir.nio.com/news-events/news-releases")
    print("Navigated to NIO News Releases page.")
    
    current_month = "December"
    current_year = datetime.now().year
    search_text = "Nio Inc Provides November 2024 delivery update"

    if current_month == "December":
        search_text = f"NIO Inc. Provides {current_month}, Fourth Quarter and Full Year 2024 Delivery Update"
    else:
        search_text = f"Nio Inc Provides {current_month} {current_year} delivery update"

    print(f"Looking for news containing: {search_text}")

    while True:
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.text-banner"))
            )

            news_items = driver.find_elements(By.CSS_SELECTOR, "div.text-banner a")

            for news_item in news_items:
                if search_text in news_item.text:
                    link = news_item.get_attribute("href")
                    print(f"Matching article found: {news_item.text}")
                    print(f"Opening link: {link}")

                    driver.get(link)
                    
                    print(f"Opened the matching article successfully: {link}")
                    return

            print("Matching article not found. Retrying in 1 minute...")
            time.sleep(30)
            driver.refresh()

        except StaleElementReferenceException:
            print("Stale element detected. Retrying...")
            continue

        except NoSuchElementException:
            print("No articles found on the page. Retrying in 1 minute...")
            time.sleep(30)
            driver.refresh()



