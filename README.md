# WealthsimpleTwilioSummary

A Python project that uses Selenium to scrape portfolio data from Wealthsimple and Twilio to send a concise daily summary of portfolio performance via SMS. 

## Features

- Retrieves and summarizes your portfolio value and daily performance.
- Extracts detailed holdings information, including:
  - Total value of each position.
  - Today's price and percentage change.
  - All-time return for each holding.
- Calculates the change in portfolio value from the previous day for actionable insights.
- Sends the summary via Twilio SMS in a user-friendly format.

---

## SMS Summary Template

The SMS sent by the project follows this format:

