"""
Content Processor Module
Filters, ranks, and formats news articles
"""

import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentProcessor:
    def __init__(self):
        # Keywords that indicate important AI/tech news
        self.priority_keywords = [
            'breakthrough', 'launch', 'release', 'new model', 'gpt', 'claude',
            'gemini', 'llm', 'ai model', 'open source', 'announcement',
            'research', 'study', 'mit', 'stanford', 'deepmind', 'openai',
            'anthropic', 'meta ai', 'google ai', 'microsoft', 'nvidia',
            'transformer', 'neural', 'machine learning', 'deep learning',
            'robotics', 'autonomous', 'self-driving', 'quantum'
        ]

        self.exclude_keywords = [
            'sponsored', 'advertisement', 'ad:', 'promoted'
        ]

    def rank_article(self, article):
        """Assign relevance score to article"""
        score = 0
        title_lower = article['title'].lower()
        summary_lower = article['summary'].lower()

        # Check for priority keywords
        for keyword in self.priority_keywords:
            if keyword in title_lower:
                score += 3
            if keyword in summary_lower:
                score += 1

        # Penalize excluded content
        for keyword in self.exclude_keywords:
            if keyword in title_lower or keyword in summary_lower:
                score -= 10

        return score

    def filter_and_rank(self, articles, min_score=1, max_articles=15):
        """Filter and rank articles by relevance"""
        # Add scores to articles
        for article in articles:
            article['score'] = self.rank_article(article)

        # Filter by minimum score
        filtered = [a for a in articles if a['score'] >= min_score]

        # Sort by score (highest first)
        sorted_articles = sorted(filtered, key=lambda x: x['score'], reverse=True)

        # Limit number of articles
        return sorted_articles[:max_articles]

    def format_for_email(self, articles):
        """Format articles as HTML email"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                .article {{ margin-bottom: 30px; padding: 15px; background: #f8f9fa; border-left: 4px solid #3498db; }}
                .article h3 {{ margin-top: 0; color: #2980b9; }}
                .article a {{ color: #3498db; text-decoration: none; }}
                .article a:hover {{ text-decoration: underline; }}
                .meta {{ color: #7f8c8d; font-size: 0.9em; margin-top: 5px; }}
                .summary {{ margin-top: 10px; }}
                .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #7f8c8d; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <h1>🚀 Your Daily AI & Tech News Digest</h1>
            <p><strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
            <p>Here are today's top {len(articles)} AI and technology stories:</p>
        """

        for i, article in enumerate(articles, 1):
            html += f"""
            <div class="article">
                <h3>{i}. {article['title']}</h3>
                <div class="meta">
                    <strong>Source:</strong> {article['source'].replace('_', ' ').title()} | 
                    <strong>Published:</strong> {article['published']}
                </div>
                <div class="summary">{article['summary']}</div>
                <p><a href="{article['link']}" target="_blank">Read full article →</a></p>
            </div>
            """

        html += """
            <div class="footer">
                <p>You're receiving this because you subscribed to daily AI & Tech news updates.</p>
                <p>Stay curious! 🧠</p>
            </div>
        </body>
        </html>
        """
        return html

    def format_for_whatsapp(self, articles):
        """Format articles as plain text for WhatsApp"""
        text = f"🚀 *Daily AI & Tech News* - {datetime.now().strftime('%b %d, %Y')}\n\n"
        text += f"Top {len(articles)} stories today:\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n\n"

        for i, article in enumerate(articles, 1):
            text += f"*{i}. {article['title']}*\n"
            text += f"📰 {article['source'].replace('_', ' ').title()}\n"
            text += f"📅 {article['published']}\n\n"
            text += f"{article['summary'][:200]}...\n\n"
            text += f"🔗 {article['link']}\n"
            text += "━━━━━━━━━━━━━━━━━━━━\n\n"

        text += "Stay curious! 🧠"
        return text

    def process_articles(self, articles_file='data/articles.json'):
        """Main processing pipeline"""
        try:
            # Load articles
            with open(articles_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                articles = data['articles']

            # Filter and rank
            processed = self.filter_and_rank(articles)

            logger.info(f"Processed {len(processed)} articles from {len(articles)} total")

            return processed

        except FileNotFoundError:
            logger.error(f"Articles file not found: {articles_file}")
            return []
        except Exception as e:
            logger.error(f"Error processing articles: {e}")
            return []


if __name__ == "__main__":
    processor = ContentProcessor()
    articles = processor.process_articles()

    if articles:
        print("\n=== EMAIL FORMAT ===")
        print(processor.format_for_email(articles[:3]))

        print("\n=== WHATSAPP FORMAT ===")
        print(processor.format_for_whatsapp(articles[:3]))