"""
News Scraper Module
Scrapes AI and tech news from multiple sources
"""

import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timedelta
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.sources = {
            'techcrunch_ai': 'https://techcrunch.com/category/artificial-intelligence/feed/',
            'mit_news': 'https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml',
            'arxiv_ai': 'http://export.arxiv.org/rss/cs.AI',
            'venturebeat_ai': 'https://venturebeat.com/category/ai/feed/',
            'theverge_ai': 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml',
            'openai_blog': 'https://openai.com/blog/rss/',
        }

    def scrape_rss_feed(self, url, source_name):
        """Scrape news from RSS feed"""
        try:
            feed = feedparser.parse(url)
            articles = []

            # Get articles from last 24 hours
            cutoff_date = datetime.now() - timedelta(days=1)

            for entry in feed.entries[:10]:  # Limit to 10 most recent
                try:
                    # Parse publication date
                    pub_date = None
                    if hasattr(entry, 'published_parsed'):
                        pub_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed'):
                        pub_date = datetime(*entry.updated_parsed[:6])

                    # Skip old articles (optional - comment out to get all)
                    # if pub_date and pub_date < cutoff_date:
                    #     continue

                    article = {
                        'title': entry.title if hasattr(entry, 'title') else 'No title',
                        'link': entry.link if hasattr(entry, 'link') else '',
                        'summary': self._clean_html(entry.summary if hasattr(entry, 'summary') else ''),
                        'published': pub_date.strftime('%Y-%m-%d %H:%M') if pub_date else 'Unknown',
                        'source': source_name
                    }
                    articles.append(article)
                except Exception as e:
                    logger.warning(f"Error parsing entry from {source_name}: {e}")
                    continue

            logger.info(f"Scraped {len(articles)} articles from {source_name}")
            return articles

        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
            return []

    def _clean_html(self, html_text):
        """Remove HTML tags from text"""
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()[:300]  # Limit to 300 chars

    def scrape_all_sources(self):
        """Scrape all configured news sources"""
        all_articles = []

        for source_name, url in self.sources.items():
            logger.info(f"Scraping {source_name}...")
            articles = self.scrape_rss_feed(url, source_name)
            all_articles.extend(articles)

        # Sort by source and remove duplicates by title
        seen_titles = set()
        unique_articles = []
        for article in all_articles:
            title_lower = article['title'].lower()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique_articles.append(article)

        logger.info(f"Total unique articles scraped: {len(unique_articles)}")
        return unique_articles

    def save_articles(self, articles, filename='data/articles.json'):
        """Save articles to JSON file"""
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'articles': articles,
                    'count': len(articles)
                }, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(articles)} articles to {filename}")
        except Exception as e:
            logger.error(f"Error saving articles: {e}")


if __name__ == "__main__":
    scraper = NewsScraper()
    articles = scraper.scrape_all_sources()
    scraper.save_articles(articles)