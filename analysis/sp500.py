import yfinance as yf
from datetime import datetime, timedelta


def sp500_performance():
    """
    Gets the performance of the SP500 for the day.
    uses the prevoius day's close and the current day's closing price.
    """
    sp500 = yf.Ticker("^GSPC")

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=3)

    hist = sp500.history(start=start_date, end=end_date)

    if len(hist) < 2:
        return "No data available"
    
    prev_close = hist["Close"].iloc[0]
    today_close = hist["Close"].iloc[1]

    change_dollars = today_close - prev_close
    change_percent = (change_dollars / prev_close) * 100

    return {
        "change_dollars": change_dollars,
        "change_percent": change_percent
    }
