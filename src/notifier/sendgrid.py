import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from wealthsimple.performance import get_weekly_performance
import logging

load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")
TO_EMAIL = os.getenv("SENDGRID_TO_EMAIL")

def send_weekly_email():
    """
    Formats the weekly email and sends it using SendGrid.
    """
    starting_balance, ending_balance, biggest_gainer, biggest_loser, weekly_change = get_weekly_performance()

    if starting_balance is None or ending_balance is None:
        print("No valid weekly data available.")
        return

    biggest_gainer_text = (
        f"<strong>{biggest_gainer.stock_symbol}</strong> saw the most growth, with an all-time return of "
        f"<strong>${biggest_gainer.all_time_return:,.2f}</strong>."
        if biggest_gainer else "No significant gainers this week."
    )

    biggest_loser_text = (
        f"Unfortunately, <strong>{biggest_loser.stock_symbol}</strong> took the biggest hit, dropping "
        f"<strong>${biggest_loser.all_time_return:,.2f}</strong>."
        if biggest_loser else "No significant losers this week."
    )

    email_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #2E86C1;">📊 Weekly Portfolio Summary</h2>
        
        <p>Hey there,</p>
        
        <p>Your portfolio started at <strong>${starting_balance:,.2f}</strong> and ended at 
        <strong>${ending_balance:,.2f}</strong>. That’s a <strong>{weekly_change:.2f}%</strong> change!</p>
        
        <h3 style="color: #27AE60;">🏆 Biggest Gainer</h3>
        <p>{biggest_gainer_text}</p>

        <h3 style="color: #E74C3C;">📉 Biggest Loser</h3>
        <p>{biggest_loser_text}</p>
        
        <p>Let's see what next week brings! 🚀</p>
        
        <p>Cheers,<br>Your Market Bot</p>
    </body>
    </html>
    """

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject="Your Weekly Portfolio Report",
        html_content=email_body,
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info(f"Email sent! Status Code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
