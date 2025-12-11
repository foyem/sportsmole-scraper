"""
Configuration settings for SportsMole Scraper
"""

# Base URLs
BASE_URL = "https://www.sportsmole.co.uk"
FOOTBALL_URL = f"{BASE_URL}/football"
FIXTURES_URL = f"{FOOTBALL_URL}/fixtures/"

# Request settings
REQUEST_TIMEOUT = 30  # seconds
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Cache settings
CACHE_DURATION_MINUTES = 30

# API settings
API_HOST = "0.0.0.0"
API_PORT = 5000
DEBUG_MODE = True

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Scraper settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
