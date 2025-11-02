@echo off
echo Starting Tech News Digest...
echo.

cd /d C:\Users\axajo\OneDrive\Desktop\tech-news-digest

echo Checking/installing all required packages...
venv\Scripts\python.exe -m pip install --quiet requests beautifulsoup4 feedparser python-dotenv schedule

echo.
echo Running digest script...
venv\Scripts\python.exe src\main.py --once

echo.
echo Done! Check your email.
pause