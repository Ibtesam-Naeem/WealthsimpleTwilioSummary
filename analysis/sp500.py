import yfinance as yf
from datetime import datetime, timedelta

def sp500_performance():
    """
    Gets the performance of the SP500 for the latest trading day.
    Uses the previous trading day's close and the latest available close price.
    Handles gaps in trading days (e.g., weekends, holidays).
    """
    sp500 = yf.Ticker("^GSPC")

    # Fetch data for the past 7 days to ensure coverage of holidays and weekends does not return an error
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    hist = sp500.history(start=start_date, end=end_date)

    if len(hist) < 2:
        return {"error": "Insufficient data for SP500 performance"}

    # Get the last two trading days' close prices
    last_two_closes = hist["Close"].iloc[-2:]
    if len(last_two_closes) < 2:
        return {"error": "Unable to retrieve two valid trading days"}

    prev_close, today_close = last_two_closes.iloc[0], last_two_closes.iloc[1]

    change_dollars = today_close - prev_close
    change_percent = (change_dollars / prev_close) * 100

    return {
        "change_dollars": change_dollars,
        "change_percent": change_percent
    }

