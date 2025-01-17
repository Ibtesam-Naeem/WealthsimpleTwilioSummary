from dotenv import load_dotenv
import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_option
from auth.otp import generate_otp
import pyotp

load_dotenv()

email = os.getenv("WEALTHSIMPLE_EMAIL")
password = os.getenv("WEALTHSIMPLE_PASSWORD")
secret_key = os.getenv("SECRET_KEY")

otp_code = generate_otp(secret_key)

driver = chrome_option()

def login():
    """
    Logs in to Welthsimple
    """
    try:
        # Navigate to WealthSimple
        driver.get("https://my.wealthsimple.com/app/login?locale=en-ca")
        logging.info("Navigated to login page.")
        
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@inputmode='email']"))
        )

        email_element = driver.find_element(By.XPATH, "//input[@inputmode='email']")

        # Clears any pre-existing text in the box
        email_element.clear()

        email_element.send_keys(email)
        logging.info("Email entered.")

        WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='password']"))
        )

        password_element = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        # Clears any pre-existing text in the box
        password_element.clear()

        # After entering in the password, it will click enter to sign in
        password_element.send_keys(password + Keys.ENTER)
        logging.info("Password entered.")

        handle_otp()

        logging.info("Sucessfully Logged in!")
    
        # Navigates to home page upon logging in
        navigate_to_home()

    except Exception as e:
        logging.error(f"Failed to log in: {e}")
        raise
   
def handle_otp():
    """
    Handles the OTP input for the 2fa
    """
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='one-time-code']"))
        )

        otp_element = driver.find_element(By.CSS_SELECTOR, "input[autocomplete='one-time-code']")

        otp_element.clear()

        otp_element.send_keys(otp_code + Keys.ENTER)
        logging.info(f"Successfully entered OTP")

    except Exception as e:
        logging.critical(f"UNABLE TO ENTER OTP: {e}")
        raise

def navigate_to_home():
    """
    Navigates to the home page, where 
    all the menus and accounts are located.
    """
    try:
        # Navigate to home page where all the info is located, default page.
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Home'))
        )

        home_page = driver.find_element(By.LINK_TEXT, 'Home')

        home_page.click()

        logging.info("Navigated to home page.")

    except Exception as e:
        logging.error(f"Error navigating to home page: {e}.")
        raise
    
def logout():
    """
    Logs out of Wealthsimple securely.
    Args:
        driver: Selenium WebDriver instance.
    """
    navigate_to_home()

    try:
        logout_menu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Profile and settings" and @role="button"]'))
        )

        logout_menu.click()

        logout_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='Log out']"))
        )
        logout_button.click()
        logging.info('Sucessfully logged out')
        return True
    
    except Exception as e:
        logging.error(f'Error logging out: {e}')
        raise