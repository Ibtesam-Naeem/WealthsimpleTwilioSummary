import os
import sys
from wealthsimple.auth import login, navigate_to_home, logout
from wealthsimple.ws_data import total_port_value, scrape_holdings, format_summary_message
from analysis.sp500 import get_spy_daily_performance
from wealthsimple.performance import read_previous_data, write_current_data, calculate_change
from notifications.twilio_sms import send_sms
from datetime import datetime
from analysis.events import navigate_and_scrape_earnings
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
    Gets the sp500 performance data
    """
    sp500_data = get_spy_daily_performance()
    return sp500_data

def calculate_portfolio_change(total_value, previous_data):
    if previous_data and "total_portfolio_value" in previous_data:
        return calculate_change(total_value, previous_data["total_portfolio_value"])
    return None, None

def daily_job():
    """
    Executes the daily job to fetch data, calculate changes, and
    send a summary message.
    """
    previous_data = read_previous_data()
    total_value, holdings = fetch_portfolio_data()
    sp500_data = fetch_sp500_data()
    change, percentage = calculate_portfolio_change(total_value, previous_data)

    final_message = format_summary_message(
        total_value, holdings, sp500_data, change, percentage, previous_data
    )

    earnings_data = navigate_and_scrape_earnings()
    earnings_summary = "\n".join(earnings_data) if earnings_data else "No significant earnings data for today or tomorrow."
    final_message += f"\n\nEarnings Summary:\n{earnings_summary}"

    write_current_data({"total_portfolio_value": total_value, "holdings": holdings})
    send_sms(final_message)

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