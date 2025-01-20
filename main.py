import os
import sys
from auth.ws_login import login, navigate_to_home, logout
from wealthsimple.ws_data import total_port_value, scrape_holdings, format_summary_message
from analysis.sp500 import get_spy_daily_performance
from wealthsimple.performance import read_previous_data, write_current_data, calculate_change
from config.twilio_sms import send_sms
from datetime import datetime
from analysis.events import trading_view_calendar
from config.logging_info import setup_logging
import logging

def fetch_portfolio_data():
    """
    Fetches the portfolio data
    """
    login()
    total_value = total_port_value()
    holdings = scrape_holdings()
    logout()
    return total_value, holdings

def fetch_sp500_data():
    """
    Gets the S&P 500 performance data
    """
    try:
        sp500_data = get_spy_daily_performance()
        return sp500_data
    except Exception as e:
        logging.error("Failed to fetch S&P 500 data")

def calculate_portfolio_change(total_value, previous_data):
    if previous_data and "total_portfolio_value" in previous_data:
        return calculate_change(total_value, previous_data["total_portfolio_value"])
    return None, None

def daily_job():
    """
    Executes the daily job to fetch data, calculate changes, and
    send a summary message.
    """
    try:
        logging.info("Starting daily job.")

        # Step 1: Fetch Portfolio Data
        logging.info("Fetching portfolio data...")
        previous_data = read_previous_data()
        total_value, holdings = fetch_portfolio_data()
        logging.info(f"Fethced portfolio")

        # Step 2: Fetch S&P 500 Data
        logging.info("Fetching S&P 500 data...")
        sp500_data = fetch_sp500_data()
        logging.info("Fetched S&P 500 data")

        # Step 3: Calculate Portfolio Change
        change, percentage = calculate_portfolio_change(total_value, previous_data)

        # Step 4: Generate Final Message
        final_message = format_summary_message(
            total_value, holdings, sp500_data, change, percentage, previous_data
        )

        logging.info("Scraping earnings data...")
        earnings_data = trading_view_calendar()
        earnings_summary = "\n".join(earnings_data) if earnings_data else "No significant earnings data for today or tomorrow."
        final_message += f"\n\nEarnings Summary:\n{earnings_summary}"
        
        # Step 6: Write Current Data and Send SMS
        logging.info("Writing current data...")
        current_data = {
            "total_portfolio_value": total_value,
            "holdings": holdings
        }

        try:
            write_current_data(current_data)
            logging.info("Current data written successfully.")
        except Exception as e:
            logging.error(f"Failed to write current data: {e}")
        
        logging.info("Sending SMS...")
        send_sms(final_message)
        logging.info("Daily job completed successfully.")

    except Exception as e:
        logging.error(f"Error in daily job: {e}")
        
def main():
    """
    Main function to execute the daily job
    """
    setup_logging()
    logging.info("Program started.")
    
    try:
        daily_job()
    except Exception as e:
        logging.error("Error running main job")

if __name__ == "__main__":
    main()