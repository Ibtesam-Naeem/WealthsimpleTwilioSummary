from wealthsimple.wealthsimple import login, navigate_to_home, total_port_value, scrape_holdings, format_holdings, send_sms, logout
from wealthsimple.performance import read_previous_data, write_current_data, calculate_change
from market_data.sp500 import sp500_performance
import time

if __name__ == "__main__":
    # Read previous data
    previous_data = read_previous_data()

    # Log in to Wealthsimple
    login()
    navigate_to_home()

    # Get the total portfolio value
    total_value = total_port_value()
    portfolio_message = f"💰 Portfolio Value: {total_value}" if total_value else "❌ Failed to retrieve portfolio value."

    # Gets the sp500 performance for the day
    sp500_data = sp500_performance()

    if "error" in sp500_data:
        sp500_message = sp500_data["error"]
    else:
        change_dollars = sp500_data["change_dollars"]
        change_percent = sp500_data["change_percent"]
        if change_dollars >= 0:
            sp500_message = f"📈 SP500 Change: {change_dollars:.2f} ({change_percent:.2f}%)"
        else:
            sp500_message = f"📉 SP500 Change: {change_dollars:.2f} ({change_percent:.2f}%)"
    
    # Calculate change if previous data exists
    if previous_data and "total_portfolio_value" in previous_data:
        change, percentage = calculate_change(total_value, previous_data["total_portfolio_value"])
        if change >= 0:
            change_message = f"📈 Change in Value: ${change:.2f} ({percentage:.2f}%)" if change is not None else "No change data available."
        elif change < 0:
            change_message = f"📉 Change in Value: ${change:.2f} ({percentage:.2f}%)" if change is not None else "No change data available."
    else:
        change_message = "No previous data available for comparison."
    
    # Scrape holdings
    holdings = scrape_holdings()
    holdings_message = format_holdings(holdings)
    
    # Wait for 5 seconds to ensure the page is loaded fully
    time.sleep(5)

    # Create the final message
    final_message = f"{portfolio_message}\n{change_message}\n{sp500_message}\nHoldings:\n{holdings_message}"

    # Save the current data for future comparisons
    current_data = {
        "total_portfolio_value": total_value,
        "holdings": holdings
    }
    write_current_data(current_data)

    # Logout from Wealthsimple securely
    logout()

    # Send the message using Twilio
    print(final_message)
    send_sms(final_message)
