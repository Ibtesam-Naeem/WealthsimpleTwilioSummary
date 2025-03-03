from auth.ws_login import login, logout
from wealthsimple.ws_data import total_port_value, scrape_holdings, format_summary_message
from analysis.sp500 import get_spy_daily_performance
from wealthsimple.performance import read_previous_data, write_current_data, calculate_change
from notifier.twilio_sms import send_sms
from notifier.sendgrid import send_weekly_email
from config.logging_info import setup_logging
from config.db_manager import insert_portfolio, insert_holding
import logging
import schedule
import time

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
        previous_value = previous_data["total_portfolio_value"]

        if isinstance(total_value, str):
            total_value = float(total_value.replace("$", "").replace(",", ""))
        if isinstance(previous_value, str):
            previous_value = float(previous_value.replace("$", "").replace(",", ""))

        change = total_value - previous_value
        percentage_change = (change / previous_value) * 100 if previous_value != 0 else 0
        return change, percentage_change
    
    return None, None

def daily_job():
    """
    Executes the daily job to fetch data, calculate changes, and
    send a summary message.
    """
    try:
        logging.info("Fetching portfolio data...")
        previous_data = read_previous_data()
        total_value, holdings = fetch_portfolio_data()
        logging.info("Fetched portfolio")

        portfolio_id = insert_portfolio(float(total_value.replace("$", "").replace(",", "")))
        
        for stock in holdings:
            try:
                total_value_parts = stock["Total Value"].split()
                shares_parts = stock["Total Value"].split("\n")

                total_value = float(total_value_parts[0].replace("$", "").replace(",", "")) if total_value_parts else 0.0
                shares_owned = float(shares_parts[1].split()[0]) if len(shares_parts) > 1 else 0.0
                price_per_share = float(stock["Today's Price"].split()[0].replace("$", "")) if "Today's Price" in stock else 0.0
                all_time_return = float(
                    stock["All Time Return"].split()[0]
                    .replace("$", "")
                    .replace(",", "")
                    .replace("−", "-")
                ) if "All Time Return" in stock else 0.0

                insert_holding(
                    portfolio_id=portfolio_id,
                    stock_symbol=stock.get("Position", "UNKNOWN"),
                    total_value=total_value,
                    shares_owned=shares_owned,
                    price_per_share=price_per_share,
                    all_time_return=all_time_return
                )
            except (IndexError, ValueError, KeyError) as e:
                logging.error(f"Error processing stock data: {stock}, Error: {e}")

        logging.info("Fetching S&P 500 data...")
        sp500_data = fetch_sp500_data()
        logging.info("Fetched S&P 500 data")

        change, percentage = calculate_portfolio_change(total_value, previous_data)

        final_message = format_summary_message(
            total_value, holdings, sp500_data, change, percentage, previous_data
        )

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
        logging.info(f"SMS sent successfully. {final_message}")
    
    except Exception as e:
        logging.error(f"Error in daily job: {e}")
        
def weekly_job():
    """
    Executes the weekly job to fetch performance and send a summary email.
    """
    logging.info("Fetching weekly performance...")
    send_weekly_email()
    logging.info("Weekly email sent successfully.")

def main():
    """
    Main function to schedule daily and weekly jobs for immediate testing.
    """
    setup_logging()
    logging.info("Scheduler started.")
    
    schedule.every().day.at("09:30").do(daily_job)
    schedule.every().day.at("16:30").do(daily_job)

    schedule.every().sunday.at("20:00").do(weekly_job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()