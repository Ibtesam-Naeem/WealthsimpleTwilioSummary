def format_holdings(holdings):
    """
    Formats the holdings data for Twilio's SMS with better readability.
    """
    if not holdings:
        return "No holdings data found."

    message = []
    for holding in holdings:
        try:
            all_time_return = float(holding['All Time Return'].strip('%'))
        except ValueError:
            all_time_return = 0  

        emoji = "📈" if all_time_return >= 0 else "📉"
        message.append(f"{emoji} Position: {holding['Position']}")
        message.append(f"   • Total Value: {holding['Total Value']}")
        message.append(f"   • Today's Price: {holding["Today's Price"]}")
        message.append(f"   • All Time Return: {holding['All Time Return']}")
        message.append("-" * 40)

    return "\n".join(message)

def format_summary_message(total_value, holdings, sp500_data, change, percentage, previous_data):
    portfolio_message = f"💰 Portfolio Value: {total_value}" if total_value else "❌ Failed to retrieve portfolio value."
    
    if "error" in sp500_data:
        sp500_message = sp500_data["error"]
    else:
        change_dollars = sp500_data["change_dollars"]
        change_percent = sp500_data["change_percent"]
        sp500_message = (
            f"📈 SP500 Change: {change_dollars:.2f} ({change_percent:.2f}%)"
            if change_dollars >= 0
            else f"📉 SP500 Change: {change_dollars:.2f} ({change_percent:.2f}%)"
        )
    
    change_message = (
        f"📈 Change in Value: ${change:.2f} ({percentage:.2f}%)"
        if change and change >= 0
        else f"📉 Change in Value: ${change:.2f} ({percentage:.2f}%)"
        if change
        else "No previous data available for comparison."
    )
    
    holdings_message = format_holdings(holdings)
    return f"{portfolio_message}\n{change_message}\n{sp500_message}\nHoldings:\n{holdings_message}"

