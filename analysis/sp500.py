import requests
from dotenv import load_dotenv
import os
import logging
import pandas as pd 
from concurrent.futures import ThreadPoolExecutor, as_completed
load_dotenv()

FINNHUB_API = os.getenv("FINNHUB_API")

def get_spy_daily_performance():
    """
    Fetches the daily performance of the SPDR S&P 500 ETF (SPY).
    """
    SPY_TICKER = "SPY"
    BASE_URL = "https://finnhub.io/api/v1/quote"
    
    params = {
        "symbol": SPY_TICKER,
        "token": FINNHUB_API
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        current_price = data.get("c")
        previous_close = data.get("pc")
        
        if current_price is not None and previous_close is not None:
            daily_change = current_price - previous_close
            daily_percent_change = (daily_change / previous_close) * 100
            return {
                "current_price": current_price,
                "previous_close": previous_close,
                "daily_change": daily_change,
                "daily_percent_change": daily_percent_change
            }
        else:
            logging.error("Incomplete data in API response.")
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
