from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

driver = webdriver.Safari()

def tesla_delivery_report():
    """
    Continuously checks Tesla's Investor Relations page for the latest press release.
    Extracts total production and delivery numbers when found.
    Uses Safari WebDrive as it is fater for this task.
    """
    while True:
        try:
            driver.get("https://ir.tesla.com/#quarterly-disclosure")

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//table"))
            )

            rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

            for row in rows:
                try:
                    press_release_link = row.find_element(By.XPATH, ".//a[contains(text(), 'Press Release')]")
                    link = press_release_link.get_attribute("href")

                    driver.get(link)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )

                    table = driver.find_element(By.XPATH, "//table[1]")
                    rows = table.find_elements(By.XPATH, ".//tr")

                    for data_row in rows:
                        columns = data_row.find_elements(By.XPATH, ".//td")
                        if len(columns) >= 3 and "Total" in columns[0].text:
                            total_production = columns[1].text.strip()
                            total_deliveries = columns[2].text.strip()

                            print(f"Total Production: {total_production}")
                            print(f"Total Deliveries: {total_deliveries}")
                            return
                except NoSuchElementException:
                    continue

        except TimeoutException:
            print("Table not found on the IR page. Retrying in 1 minute...")
            time.sleep(60)

        except Exception as e:
            print(f"Error occurred while checking: {e}")
            time.sleep(60)

tesla_delivery_report()
