"""
Configuration settings for SportsMole Scraper
"""

import os

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
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))
# WARNING: Set DEBUG_MODE to False in production environments
# Debug mode can expose sensitive information and allow arbitrary code execution
# Can be overridden with environment variable: export DEBUG_MODE=false
DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() in ("true", "1", "yes")

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Scraper settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
