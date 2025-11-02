"""
Main Orchestrator
Coordinates scraping, processing, and notification delivery
"""

import schedule
import time
import logging
from datetime import datetime
from news_scraper import NewsScraper
from content_processor import ContentProcessor
from notifier import Notifier

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/tech_news_digest.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TechNewsDigest:
    def __init__(self):
        self.scraper = NewsScraper()
        self.processor = ContentProcessor()
        self.notifier = Notifier()

    def run_daily_digest(self):
        """Main function to run the complete news digest pipeline"""
        logger.info("=" * 50)
        logger.info("Starting daily tech news digest")
        logger.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 50)

        try:
            # Step 1: Scrape news
            logger.info("Step 1: Scraping news sources...")
            articles = self.scraper.scrape_all_sources()

            if not articles:
                logger.warning("No articles found. Exiting.")
                return

            # Save raw articles
            self.scraper.save_articles(articles)

            # Step 2: Process and filter
            logger.info("Step 2: Processing and filtering articles...")
            processed_articles = self.processor.filter_and_rank(articles, max_articles=10)

            if not processed_articles:
                logger.warning("No articles passed filtering. Exiting.")
                return

            logger.info(f"Selected {len(processed_articles)} top articles")

            # Step 3: Format content
            logger.info("Step 3: Formatting content...")
            whatsapp_message = self.processor.format_for_whatsapp(processed_articles)
            email_html = self.processor.format_for_email(processed_articles)
            email_subject = f"🚀 Your Daily AI & Tech Digest - {datetime.now().strftime('%b %d, %Y')}"

            # Step 4: Send notifications
            logger.info("Step 4: Sending notifications...")
            results = self.notifier.send_notifications(
                whatsapp_message=whatsapp_message,
                email_subject=email_subject,
                email_html=email_html,
                telegram_message=whatsapp_message  # Reuse WhatsApp format for Telegram
            )

            # Log results
            if results['whatsapp']:
                logger.info("✓ WhatsApp notification sent successfully")
            else:
                logger.warning("✗ WhatsApp notification failed or not configured")

            if results['email']:
                logger.info("✓ Email notification sent successfully")
            else:
                logger.warning("✗ Email notification failed or not configured")

            if results['telegram']:
                logger.info("✓ Telegram notification sent successfully")
            else:
                logger.warning("✗ Telegram notification failed or not configured")

            logger.info("=" * 50)
            logger.info("Daily digest completed successfully")
            logger.info("=" * 50)

        except Exception as e:
            logger.error(f"Error in daily digest: {e}", exc_info=True)

    def run_once(self):
        """Run the digest once (for testing)"""
        self.run_daily_digest()

    def start_scheduler(self, run_time="09:00"):
        """Start the scheduler to run daily at specified time"""
        logger.info(f"Scheduler started. Will run daily at {run_time}")

        # Schedule the job
        schedule.every().day.at(run_time).do(self.run_daily_digest)

        # Run immediately on startup (optional - comment out if not needed)
        logger.info("Running initial digest on startup...")
        self.run_daily_digest()

        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


def main():
    """Main entry point"""
    import sys

    digest = TechNewsDigest()

    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--once':
            # Run once and exit
            logger.info("Running in single-run mode")
            digest.run_once()
        elif sys.argv[1] == '--schedule':
            # Run on schedule
            run_time = sys.argv[2] if len(sys.argv) > 2 else "09:00"
            logger.info(f"Running in scheduled mode at {run_time}")
            digest.start_scheduler(run_time)
        else:
            print("Usage:")
            print("  python main.py --once              # Run once and exit")
            print("  python main.py --schedule [TIME]   # Run daily at TIME (default: 09:00)")
    else:
        # Default: run once
        logger.info("No arguments provided. Running once.")
        digest.run_once()


if __name__ == "__main__":
    main()