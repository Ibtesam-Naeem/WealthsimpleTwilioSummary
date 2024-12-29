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
from wealthsimple.chrome_options import chrome_option
load_dotenv()


email = os.getenv("WEALTHSIMPLE_EMAIL")
password = os.getenv("WEALTHSIMPLE_PASSWORD")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECIPIENT_PHONE_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")


driver = chrome_option()

def send_sms(message):
    """
    Sends an SMS using Twilio.
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE_NUMBER
        )
        print("Message sent successfully!")
    except Exception as e:
        print(f"Failed to send SMS: {e}")


def login():
    """
    Logs in to Welthsimple
    """

    try:
        # Navigate to WealthSimple
        driver.get("https://my.wealthsimple.com/app/login?locale=en-ca")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@inputmode='email']"))
        )

        email_element = driver.find_element(By.XPATH, "//input[@inputmode='email']")

        # Clears any pre-existing text in the box
        email_element.clear()

        email_element.send_keys(email)

        WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='password']"))
        )

        password_element = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        # Clears any pre-existing text in the box
        password_element.clear()

        # After entering in the password, it will click enter to sign in
        password_element.send_keys(password + Keys.ENTER)

        print("Sucessfully Logged in!")

    except Exception as e:
        print(f"Failed to log in: {e}")

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
        print('Sucessfully logged out)')
        return True
    except Exception as e:
        print(f'Error logging out: {e}')
        return False
        
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

        print("Navigated to home page.")
    except Exception as e:
        print(f"Error navigating to home page: {e}.")

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

def format_holdings(holdings):
    """
    Formats the holdings data for Twilio's SMS with better readability.
    """
    if not holdings:
        return "No holdings data found."

    message = []
    for holding in holdings:
        message.append(f"📈 Position: {holding['Position']}")
        message.append(f"   • Total Value: {holding['Total Value']}")
        message.append(f"   • Today's Price: {holding["Today's Price"]}")
        message.append(f"   • All Time Return: {holding['All Time Return']}")
        message.append("-" * 40)  # Separator for each holding

    return "\n".join(message)
    
if __name__ == "__main__":
    login()
    navigate_to_home()

    # Get the total portfolio value
    total_value = total_port_value()
    portfolio_message = f"💰 Portfolio Value: {total_value}" if total_value else "❌ Failed to retrieve portfolio value."

    # Scrape holdings
    holdings = scrape_holdings()
    holdings_message = format_holdings(holdings)

    # Create the final message
    final_message = f"{portfolio_message}\n\n🔍 Holdings:\n{holdings_message}"

    # Send the message using Twilio
    print(final_message)
    send_sms(final_message)

    driver.quit()


