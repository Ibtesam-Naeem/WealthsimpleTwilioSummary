from wealthsimple.auth import login, navigate_to_home, logout
from wealthsimple.ws_data import total_port_value, scrape_holdings
from wealthsimple.performance import read_previous_data, write_current_data, calculate_change
from analysis.sp500 import sp500_performance
from wealthsimple.formatting import format_summary_message
from notifications.twilio_sms import send_sms

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
    sp500_data = sp500_performance()
    return sp500_data

def calculate_portfolio_change(total_value, previous_data):
    if previous_data and "total_portfolio_value" in previous_data:
        return calculate_change(total_value, previous_data["total_portfolio_value"])
    return None, None

def main():
    """
    The main function orchestrates the data fetching, change calculation, and message sending.

    Workflow:
        1. Reads previous portfolio data.
        2. Logs in, fetches portfolio data, and logs out.
        3. Fetches S&P 500 performance data.
        4. Calculates changes in portfolio value.
        5. Formats the final summary message.
        6. Saves the current portfolio data for future comparisons.
        7. Sends the summary message via SMS.

    Raises:
        Exception: If any step in the workflow fails.
    """
    previous_data = read_previous_data()
    total_value, holdings = fetch_portfolio_data()
    sp500_data = fetch_sp500_data()
    change, percentage = calculate_portfolio_change(total_value, previous_data)

    final_message = format_summary_message(
        total_value, holdings, sp500_data, change, percentage, previous_data
    )

    write_current_data({"total_portfolio_value": total_value, "holdings": holdings})
    send_sms(final_message)

if __name__ == "__main__":
    main()