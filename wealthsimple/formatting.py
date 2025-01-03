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