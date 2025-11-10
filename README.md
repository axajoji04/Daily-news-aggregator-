# 🚀 Daily Tech News Digest

An automated news aggregator system that scrapes AI and tech news from multiple sources, intelligently filters and ranks articles, and delivers personalized digests via WhatsApp, Email, and Telegram.

## ✨ Features

- *Multi-Source Scraping*: Aggregates news from 6+ premium tech sources
  - TechCrunch AI
  - MIT News
  - ArXiv AI Papers
  - VentureBeat AI
  - The Verge AI
  - OpenAI Blog

- *Intelligent Filtering*: Smart keyword-based ranking system that prioritizes relevant content
- *Multi-Channel Delivery*: Get your digest via:
  - 📧 Email (Gmail SMTP)
  - 💬 WhatsApp (CallMeBot API)
  - 📱 Telegram Bot
- *Automated Scheduling*: Daily digests at your preferred time
- *GitHub Actions Integration*: Run automatically in the cloud
- *100% Free*: All services used are completely free

## 📋 Table of Contents

- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Scheduling](#-scheduling)
- [Customization](#-customization)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## 🔧 Installation

### Prerequisites

- Python 3.10 or higher
- Git (optional)
- A Gmail account
- A phone with WhatsApp (optional)
- A Telegram account (optional)

### Step 1: Clone the Repository

bash
git clone https://github.com/axajoji04/Daily-news-aggregator-.git
cd  Daily-news-aggregator


### Step 2: Create Virtual Environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate


### Step 3: Install Dependencies

bash
pip install -r requirements.txt


### Step 4: Create Required Directories

bash
mkdir data logs


## ⚙️ Configuration

### 1. Create .env File

Create a .env file in the project root:

env
# Gmail Configuration (Required for Email)
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password
EMAIL_TO=recipient@email.com

# CallMeBot Configuration (Optional - for WhatsApp)
CALLMEBOT_PHONE=+1234567890
CALLMEBOT_APIKEY=your_callmebot_api_key

# Telegram Configuration (Optional - Recommended!)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here


### 2. Setup Gmail (Required)

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable *2-Step Verification*
3. Go to *App Passwords* section
4. Generate a new app password for "Mail"
5. Copy the 16-character password to your .env file

### 3. Setup WhatsApp via CallMeBot (Optional)

1. Add *CallMeBot* to your WhatsApp contacts: +34 644 44 01 99
2. Send this message: I allow callmebot to send me messages
3. You'll receive your API key
4. Add your phone number (with country code) and API key to .env

Full guide: [CallMeBot WhatsApp API](https://www.callmebot.com/blog/free-api-whatsapp-messages/)

### 4. Setup Telegram Bot (Optional but Recommended)

1. Open Telegram and search for @BotFather
2. Send /newbot and follow instructions
3. Copy the *bot token*
4. Start a chat with your new bot
5. Get your chat ID:
   - Send a message to your bot
   - Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   - Find your chat_id in the response
6. Add both to your .env file

## 🚀 Usage

### Run Once (Manual Test)

bash
python main.py --once


This will:
1. Scrape all news sources
2. Filter and rank articles
3. Send notifications via all configured channels
4. Save logs to logs/tech_news_digest.log

### Run on Schedule (Continuous)

bash
# Run daily at 9:00 AM (default)
python main.py --schedule

# Run daily at custom time
python main.py --schedule 14:30


### Test Notifications

Test if your notification channels are working:

bash
python notifier.py


### Test Individual Modules

bash
# Test scraper only
python news_scraper.py

# Test content processor only
python content_processor.py


## 📁 Project Structure


tech-news-digest/
├── .github/
│   └── workflows/
│       └── daily-digest.yml      # GitHub Actions workflow
├── data/
│   └── articles.json             # Scraped articles (generated)
├── logs/
│   └── tech_news_digest.log      # Application logs (generated)
├── src/                          # Alternative source directory
│   ├── content_processor.py
│   ├── main.py
│   ├── news_scraper.py
│   └── notifier.py
├── .env                          # Environment variables (create this)
├── .gitignore                    # Git ignore rules
├── content_processor.py          # Article filtering & ranking
├── main.py                       # Main orchestrator
├── news_scraper.py               # RSS feed scraper
├── notifier.py                   # Notification sender
├── requirements.txt              # Python dependencies
└── README.md                     # This file


## 🔄 How It Works

### 1. News Scraping (news_scraper.py)

- Fetches RSS feeds from multiple tech news sources
- Parses articles with title, link, summary, and publication date
- Removes duplicates based on article titles
- Saves raw data to data/articles.json

### 2. Content Processing (content_processor.py)

- *Ranking Algorithm*: Assigns relevance scores based on keywords
  - +3 points for priority keywords in title
  - +1 point for priority keywords in summary
  - -10 points for excluded keywords (ads, sponsored content)
- *Filtering*: Removes low-scoring articles (score < 1)
- *Selection*: Picks top 10-15 articles
- *Formatting*: Generates HTML email and Markdown text formats

### 3. Notification Delivery (notifier.py)

- *Email*: Sends beautifully formatted HTML email via Gmail SMTP
- *WhatsApp*: Sends text digest via CallMeBot API (3000 char limit)
- *Telegram*: Sends Markdown-formatted message (supports long messages)

### 4. Orchestration (main.py)

- Coordinates the entire pipeline
- Handles scheduling with schedule library
- Provides CLI interface for manual runs
- Logs all activities

## 📅 Scheduling

### Local Scheduling

The built-in scheduler runs the digest at your specified time:

bash
python main.py --schedule 09:00  # Runs daily at 9:00 AM


### GitHub Actions (Cloud Automation)

The project includes a GitHub Actions workflow that runs automatically:

*Current Schedule*: 4:30 UTC (10:00 AM IST)

To use GitHub Actions:

1. Fork this repository
2. Go to *Settings* → *Secrets and variables* → *Actions*
3. Add all your environment variables as *Repository Secrets*:
   - GMAIL_USER
   - GMAIL_APP_PASSWORD
   - EMAIL_TO
   - CALLMEBOT_PHONE (optional)
   - CALLMEBOT_APIKEY (optional)
   - TELEGRAM_BOT_TOKEN (optional)
   - TELEGRAM_CHAT_ID (optional)
4. Enable GitHub Actions in your repository

The workflow will:
- Run daily at the scheduled time
- Create logs as artifacts (downloadable for 7 days)
- Send notifications automatically
- Require zero maintenance

### Change Schedule

Edit .github/workflows/daily-digest.yml:

yaml
schedule:
  - cron: '30 4 * * *'  # 4:30 UTC


Use [crontab.guru](https://crontab.guru/) to generate cron expressions.

## 🎨 Customization

### Add New News Sources

Edit news_scraper.py:

python
self.sources = {
    'your_source': 'https://example.com/rss',
    # ... other sources
}


### Modify Ranking Keywords

Edit content_processor.py:

python
self.priority_keywords = [
    'your', 'custom', 'keywords',
    # ... more keywords
]


### Change Article Limit

Edit main.py:

python
processed_articles = self.processor.filter_and_rank(
    articles, 
    max_articles=20  # Change from 10 to 20
)


### Customize Email Template

Edit the format_for_email() method in content_processor.py to change:
- Colors
- Fonts
- Layout
- Content structure

## 🐛 Troubleshooting

### Email Not Sending

- ✅ Verify 2FA is enabled on your Google account
- ✅ Ensure you're using an *App Password*, not your regular password
- ✅ Check if "Less secure app access" is needed (usually not with app passwords)

### WhatsApp Not Working

- ✅ Verify you sent the authorization message to CallMeBot
- ✅ Check phone number format (include country code: +1234567890)
- ✅ API key should be exactly as received (no extra spaces)

### Telegram Not Working

- ✅ Ensure bot token is correct
- ✅ Send at least one message to your bot first
- ✅ Verify chat ID matches your personal chat

### No Articles Scraped

- ✅ Check your internet connection
- ✅ Some RSS feeds may be temporarily down
- ✅ Check logs: logs/tech_news_digest.log

### GitHub Actions Failing

- ✅ Verify all secrets are added correctly
- ✅ Check workflow logs in the Actions tab
- ✅ Ensure repository has Actions enabled

## 📊 Logs

Logs are saved to logs/tech_news_digest.log:

bash
# View recent logs
tail -f logs/tech_news_digest.log

# View last 50 lines
tail -n 50 logs/tech_news_digest.log


## 🔒 Security Notes

- ✅ Never commit .env file (already in .gitignore)
- ✅ Use GitHub Secrets for sensitive data in Actions
- ✅ Regularly rotate your API keys and app passwords
- ✅ Keep dependencies updated: pip install --upgrade -r requirements.txt

## 📈 Future Enhancements

Potential features to add:

- [ ] Web dashboard for viewing articles
- [ ] Machine learning-based article ranking
- [ ] Sentiment analysis
- [ ] Multi-language support
- [ ] Discord/Slack integration
- [ ] Custom user preferences
- [ ] Article summarization with AI
- [ ] Read-later integration (Pocket, Instapaper)

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: git checkout -b feature-name
3. Commit changes: git commit -am 'Add new feature'
4. Push to branch: git push origin feature-name
5. Submit a Pull Request

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

- GitHub: [Axa Joji](https://github.com/axajoji04)
- Email: axajoji2004@gmail.com

## 🙏 Acknowledgments

- [TechCrunch](https://techcrunch.com) for AI news
- [MIT News](https://news.mit.edu) for research articles
- [CallMeBot](https://www.callmebot.com) for free WhatsApp API
- [Telegram](https://telegram.org) for excellent bot API
- All RSS feed providers

## 💡 Tips

- *Best Time to Run*: Early morning to get news from the previous day
- *Notification Preferences*: Telegram is fastest and most reliable
- *Article Quality*: Adjust min_score in filtering for more/fewer articles
- *Customization*: Fork and personalize keywords for your interests

## 📞 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review logs in logs/tech_news_digest.log
3. Open an issue on GitHub with:
   - Error message
   - Log excerpts
   - Steps to reproduce

---

*Happy Reading! Stay informed about AI and technology! 🚀🧠*
