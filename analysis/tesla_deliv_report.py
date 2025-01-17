from config.chrome_options import chrome_option
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import logging

driver = chrome_option()

def tesla_ir_page():
    """
    Navigates to Teslas Investor Relations
    Page
    """
    try:
        driver.get("https://ir.tesla.com/#quarterly-disclosure")
        logging.info("Navigated to Tesla IR page.")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//table"))
        )
    except Exception as e:
         logging.critical("Error navigating to IR Page!")
        
def tesla_delivery_report():
    """
    Continuously checks Tesla's Investor Relations page for
    the latest press release.
    Extracts total production and delivery numbers when found.
    """
    while True:
        try:
            tesla_ir_page()
            rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

            press_release_link = None
            for row in rows:
                try:
                    press_release_link = row.find_element(By.XPATH, ".//a[contains(text(), 'Press Release')]")
                    break  
                
                except NoSuchElementException:
                    continue

            if not press_release_link:
                logging.error("Press Release link not found. Retrying in 1 minute...")
                time.sleep(60)
                continue

            link = press_release_link.get_attribute("href")
            driver.get(link)
            logging.info(f"Opened press release page: {link}")

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
                    return message

        except Exception as e:
            logging.error(f"Error: {e}")
            driver.quit
