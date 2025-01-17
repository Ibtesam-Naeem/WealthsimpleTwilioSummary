# Wealthsimple Twilio Summary

## Overview

This project automates the process of summarizing your Wealthsimple portfolio's daily performance and sending it to you via SMS using Twilio. The script retrieves portfolio data, calculates changes in value, and delivers key insights in a concise, user-friendly format.

Additionally, it compares the performance of your portfolio to the S&P 500 for the day, offering valuable context about your investments' relative performance.

The script also includes an earnings feature that monitors companies with a market capitalization over $500 million for upcoming earnings reports, providing valuable information like ticker, market cap, EPS forecast, and the reporting time (before market open or after market close).

---

## Key Features

- **Portfolio Summary**:
  - Retrieves daily portfolio performance and total value.
- **Holdings Breakdown**:
  - Total value of each position.
  - Current price and percentage change.
  - All-time return for each holding.
- **Daily Change**:
  - Calculates the change in portfolio value from the previous day.
- **Performance Comparison**:
  - Compares your portfolio's daily performance against the S&P 500 index.
- **Earnings Alerts**:
  - Monitors companies with a market cap over $500 million.
  - Retrieves ticker, market cap, EPS forecast, and reporting time.
  - Sends a summary via SMS for earnings on the current day.
- **SMS Delivery**:
  - Sends the portfolio and earnings summary via Twilio SMS in an easy-to-read format.

---

## Setup and Configuration

### Prerequisites

- Python 3.7 or later.
- A Wealthsimple account.
- A Twilio account for SMS delivery.
- Required Python packages (listed in `requirements.txt`).

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/IbtesamNaeem/WealthsimpleTwilioSummary.git
   cd WealthsimpleTwilioSummary
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:

   - Create a `.env` file in the root directory with the following keys:
     ```env
     WEALTHSIMPLE_USERNAME=your_username
     WEALTHSIMPLE_PASSWORD=your_password
     WEALTHSIMPLE_2FA_SECRET=your_2fa_secret
     TWILIO_SID=your_twilio_sid
     TWILIO_AUTH_TOKEN=your_twilio_auth_token
     TWILIO_PHONE_NUMBER=your_twilio_phone
     TARGET_PHONE_NUMBER=recipient_phone
     ```

4. **Run the Script**:

   ```bash
   python main.py
   ```

---

## Usage Instructions

- The script will log in to Wealthsimple using the provided credentials and generate a 2FA code using PyOTP.
- It will scrape the portfolio data, calculate daily changes, and summarize your holdings.
- It will compare your portfolio's performance with the S&P 500 index for the day.
- It will check for earnings reports of companies with a market capitalization over $500 million and include their ticker, market cap, EPS forecast, and reporting time.
- An SMS containing the portfolio summary and earnings alerts will be sent to the target phone number using Twilio.

### Example SMS Output

```
Wealthsimple Portfolio Summary:
- Total Value: $50,000
- Daily Change: +$500 (+1.0%)
- S&P 500 Change: +$400 (+0.8%)

Top Holdings:
1. AAPL: $15,000 (+2.5%)
2. TSLA: $10,000 (-1.0%)
3. AMZN: $25,000 (+3.0%)

Earnings Alerts:
- MSFT: Market Cap $2.5T, EPS Forecast $2.31, Reporting After Market Close
- GOOGL: Market Cap $1.7T, EPS Forecast $1.42, Reporting Before Market Open
```

---

## Security Best Practices

- Store sensitive information (e.g., passwords, 2FA secrets, API keys) securely in the `.env` file.
- Avoid committing your `.env` file to the repository by including it in `.gitignore`.
- Rotate credentials periodically to maintain security.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
