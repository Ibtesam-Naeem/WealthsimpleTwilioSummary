from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.chrome_options import chrome_options
import logging

driver = chrome_options()

def total_port_value():
    """
    Gets the total portfolio value.
    """
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "goinvI"))
        )
        total_value = driver.find_element(By.CLASS_NAME, 'goinvI').text

        logging.info(f"Total portfolio value: {total_value}.")
        return total_value
    except Exception as e:
        logging.error(f"Unable to locate total porfolio value: {e}.")
        raise
    
def scrape_holdings():
    """
    Extract holdings data from the Wealthsimple Holdings page.
    Retries up to 2 times if the data is not scraped successfully.
    Returns a list of dictionaries containing holdings information.
    """
    max_retries = 2 

    for attempt in range(max_retries):
        try:
            logging.info(f"Attempt {attempt + 1} of {max_retries}: Waiting for the holdings table to load...")
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'iFDjPC')]"))
            )
            logging.info("Holdings table located!")

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
    
            if holdings_data:
                logging.info("Holdings data scraped successfully!")
                return holdings_data

            logging.warning("No data found, retrying...")

        except Exception as e:
            logging.error(f"Error during scraping attempt {attempt + 1}: {e}")

    logging.error("Failed to scrape holdings after multiple attempts.")
    return []

def format_holdings(holdings):
    """
    Formats the holdings data for Twilio's SMS with better readability and numbering.
    """
    if not holdings:
        return "No holdings data found."

    message = []
    for index, holding in enumerate(holdings, start=1): 
        try:
            all_time_return = float(holding['All Time Return'].replace('USD', '').strip())
        except ValueError:
            all_time_return = 0
        message.append(f"{index}. ${holding['Position']} | {holding['All Time Return'].replace('USD', '').strip()}")

    return "\n".join(message)

def format_summary_message(total_value, holdings, sp500_data, change, percentage, previous_data):
    title = ("Wealthsimple Portfolio Summary:")
    portfolio_message = f"- Total Value: {total_value}" if total_value else "Failed to retrieve portfolio value."
    
    if "error" in sp500_data:
        sp500_message = sp500_data["error"]
    else:
        change_dollars = sp500_data["daily_change"]
        change_percent = sp500_data["daily_percent_change"]
        sp500_message = f"- S&P 500 Change: ${change_dollars:.2f} ({change_percent:.2f}%)"
            
    
    change_message = f"- Change Since Last Update: ${change:.2f} ({percentage:.2f}%)"

    holdings_message = format_holdings(holdings)
    return f"{title}\n{portfolio_message}\n{change_message}\n{sp500_message}\n\nTop Holdings:\n{holdings_message}"

