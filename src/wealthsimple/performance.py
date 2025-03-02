import os
import json
import logging
from datetime import datetime, timedelta
from database.db_manager import SessionLocal
from database.db_manager import Portfolio, Holdings

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True) 

DEFAULT_JSON_PATH = os.path.join(DATA_DIR, "portfolio_data.json")

def read_previous_data(file_path=DEFAULT_JSON_PATH):
    """
    Reads the previously stored portfolio data from a JSON file.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def write_current_data(data, file_path=DEFAULT_JSON_PATH):
    """
    Writes the current portfolio data to a JSON file.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
        
def calculate_change(current_value, previous_value):
    """
    Calculates the change in portfolio value between current and previous data.
    """
    try:
        current = float(current_value.replace("$", "").replace(",", ""))
        previous = float(previous_value.replace("$", "").replace(",", ""))
        change = current - previous
        percentage_change = (change / previous) * 100
        return change, percentage_change
    except Exception as e:
        logging.error(f"Error calculating change: {e}")
        return None, None

def get_weekly_performance():
    db = SessionLocal()
    
    today = datetime.utcnow().date()
    monday = today - timedelta(days=today.weekday())  # Finds the last Monday
    friday = monday + timedelta(days=4)  # Finds the last Friday

    monday_entry = db.query(Portfolio).filter(Portfolio.date >= monday).order_by(Portfolio.date.asc()).first()
    friday_entry = db.query(Portfolio).filter(Portfolio.date >= friday).order_by(Portfolio.date.desc()).first()
    
    if not monday_entry or not friday_entry:
        db.close()
        return None, None, None, None, None

    starting_balance = monday_entry.total_value
    ending_balance = friday_entry.total_value

    weekly_change = ((ending_balance - starting_balance) / starting_balance) * 100

    friday_holdings = db.query(Holdings).filter(Holdings.portfolio_id == friday_entry.id).all()

    biggest_gainer = max(friday_holdings, key=lambda stock: stock.all_time_return, default=None)
    biggest_loser = min(friday_holdings, key=lambda stock: stock.all_time_return, default=None)

    db.close()

    return starting_balance, ending_balance, biggest_gainer, biggest_loser, weekly_change
