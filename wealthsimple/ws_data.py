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
load_dotenv()

driver = chrome_option()

def total_port_value():
    """
    Gets the total portfolio value.
    """
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "goinvI"))
        )
        total_value = driver.find_element(By.CLASS_NAME, 'goinvI').text

        print(f"Total portfolio value: {total_value}.")
        return total_value
    except Exception as e:
        print(f"Unable to locate total porfolio value: {e}.")
    
def scrape_holdings():
    """
    Extract holdings data from the Wealthsimple Holdings page.
    Returns a list of dictionaries containing holdings information.
    """
    try:
        print("Waiting for the holdings table to load...")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'iFDjPC')]"))
        )
        print("Holdings table located!")

        # Locates the holdings table
        holdings_table = driver.find_element(By.XPATH, "//table[contains(@class, 'iFDjPC')]")
        rows = holdings_table.find_elements(By.XPATH, ".//tbody/tr")

        holdings_data = []
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) >= 4:  
                position = columns[0].find_element(By.TAG_NAME, "p").text
                total_value = columns[1].text
                todays_price = columns[2].text
                all_time_return = columns[3].text

                holdings_data.append({
                    "Position": position,
                    "Total Value": total_value,
                    "Today's Price": todays_price,
                    "All Time Return": all_time_return,
                })
        return holdings_data

    except Exception as e:
        print(f"Failed to scrape holdings: {e}")
        return []
