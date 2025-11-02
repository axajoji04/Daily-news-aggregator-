"""
Notifier Module - FREE VERSION
Sends notifications via CallMeBot (WhatsApp), Gmail, and Telegram
All services are 100% free!
"""

import os
import logging
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Notifier:
    def __init__(self):
        # CallMeBot configuration (for WhatsApp) - FREE!
        self.callmebot_phone = os.getenv('CALLMEBOT_PHONE')  # Your phone number
        self.callmebot_apikey = os.getenv('CALLMEBOT_APIKEY')  # Your API key

        # Gmail SMTP configuration (for Email) - FREE!
        self.gmail_user = os.getenv('GMAIL_USER')  # Your Gmail address
        self.gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')  # App-specific password
        self.email_to = os.getenv('EMAIL_TO')  # Recipient email

        # Telegram Bot configuration (for Telegram) - FREE & EASIEST!
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    def send_whatsapp_callmebot(self, message):
        """
        Send WhatsApp message via CallMeBot (FREE!)
        Setup: https://www.callmebot.com/blog/free-api-whatsapp-messages/
        """
        if not self.callmebot_phone or not self.callmebot_apikey:
            logger.error("CallMeBot credentials not found. WhatsApp disabled.")
            return False

        try:
            # CallMeBot has a 3000 character limit
            if len(message) > 2900:
                message = message[:2900] + "...\n\n[Message truncated - check email for full digest]"

            # URL encode the message
            encoded_message = quote(message)

            # CallMeBot API endpoint
            url = f"https://api.callmebot.com/whatsapp.php?phone={self.callmebot_phone}&text={encoded_message}&apikey={self.callmebot_apikey}"

            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                logger.info("✓ WhatsApp message sent via CallMeBot")
                return True
            else:
                logger.error(f"CallMeBot error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error sending WhatsApp via CallMeBot: {e}")
            return False

    def send_email_gmail(self, subject, html_content):
        """
        Send email via Gmail SMTP (FREE!)
        Setup: Enable 2FA and create App Password in Google Account
        """
        if not self.gmail_user or not self.gmail_app_password:
            logger.error("Gmail credentials not found. Email disabled.")
            return False

        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.gmail_user
            msg['To'] = self.email_to
            msg['Subject'] = subject

            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Connect to Gmail SMTP server
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.gmail_user, self.gmail_app_password)
                server.send_message(msg)

            logger.info("✓ Email sent via Gmail")
            return True

        except Exception as e:
            logger.error(f"Error sending email via Gmail: {e}")
            return False

    def send_telegram(self, message):
        """
        Send message via Telegram Bot (FREE & EASIEST!)
        Setup: Create bot with @BotFather on Telegram
        """
        if not self.telegram_bot_token or not self.telegram_chat_id:
            logger.error("Telegram credentials not found. Telegram disabled.")
            return False

        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"

            # Telegram supports up to 4096 characters with Markdown
            chunks = []
            if len(message) > 4000:
                # Split into chunks
                for i in range(0, len(message), 4000):
                    chunks.append(message[i:i + 4000])
            else:
                chunks = [message]

            # Send each chunk
            for i, chunk in enumerate(chunks):
                payload = {
                    'chat_id': self.telegram_chat_id,
                    'text': chunk,
                    'parse_mode': 'Markdown',
                    'disable_web_page_preview': False
                }

                response = requests.post(url, json=payload, timeout=30)

                if response.status_code != 200:
                    logger.error(f"Telegram error: {response.text}")
                    return False

            logger.info("✓ Telegram message sent")
            return True

        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False

    def send_notifications(self, whatsapp_message=None, email_subject=None,
                           email_html=None, telegram_message=None):
        """Send notifications via all configured channels"""
        results = {
            'whatsapp': False,
            'email': False,
            'telegram': False
        }

        if whatsapp_message and self.callmebot_phone:
            results['whatsapp'] = self.send_whatsapp_callmebot(whatsapp_message)

        if email_subject and email_html and self.gmail_user:
            results['email'] = self.send_email_gmail(email_subject, email_html)

        if telegram_message and self.telegram_bot_token:
            results['telegram'] = self.send_telegram(telegram_message)

        return results


if __name__ == "__main__":
    # Test the notifier
    notifier = Notifier()

    test_message = """🧪 *Test Message*

This is a test notification from your Tech News Digest system!

If you're seeing this, it works! 🎉"""

    # Test WhatsApp (CallMeBot)
    print("Testing WhatsApp...")
    notifier.send_whatsapp_callmebot(test_message)

    # Test Email (Gmail)
    print("Testing Email...")
    test_html = """
    <html>
    <body>
        <h1>Test Email</h1>
        <p>This is a test notification from your Tech News Digest system!</p>
        <p>If you're seeing this, it works! 🎉</p>
    </body>
    </html>
    """
    notifier.send_email_gmail("Test - Tech News Digest", test_html)

    # Test Telegram
    print("Testing Telegram...")
    notifier.send_telegram(test_message)