import json

def read_previous_data(file_path="portfolio_data.json"):
    """
    Reads the previously stored portfolio data from a JSON file.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def write_current_data(data, file_path="portfolio_data.json"):
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
        # Convert to numeric values (removing "$" and ",")
        current = float(current_value.replace("$", "").replace(",", ""))
        previous = float(previous_value.replace("$", "").replace(",", ""))
        change = current - previous
        percentage_change = (change / previous) * 100
        return change, percentage_change
    except Exception as e:
        print(f"Error calculating change: {e}")
        return None, None
