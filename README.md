# SportsMole Scraper

A Python-based web scraper and REST API for fetching upcoming football matches, statistics, and predictions from [SportsMole.co.uk](https://www.sportsmole.co.uk/).

## Features

- 🏟️ **Scrape Upcoming Matches**: Fetches all upcoming football matches from SportsMole
- 📊 **Match Statistics**: Retrieves detailed statistics for each match
- 🔮 **Predictions**: Fetches predicted scores and match predictions from SportsMole
- 🚀 **REST API**: Provides a Flask-based API to access all scraped data
- ⚡ **Caching**: Implements intelligent caching to reduce unnecessary requests
- 🔍 **Filtering**: Filter matches by competition or team name

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/foyem/sportsmole-scraper.git
cd sportsmole-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### As a Scraper (Command Line)

Run the scraper directly to test functionality:

```bash
python scraper.py
```

This will fetch and display the first 5 upcoming matches with their predictions.

### As an API (REST Service)

Start the Flask API server:

```bash
python api.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Base Information

**GET /**
```
Returns API information and available endpoints
```

### Health Check

**GET /api/health**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-11T04:56:29.639Z",
  "cache_valid": true,
  "matches_cached": 25
}
```

### Get All Matches

**GET /api/matches**

Query Parameters:
- `limit` (optional): Maximum number of matches to return
- `competition` (optional): Filter by competition name
- `team` (optional): Filter by team name (home or away)

Example:
```bash
curl http://localhost:5000/api/matches
curl http://localhost:5000/api/matches?limit=5
curl http://localhost:5000/api/matches?competition=premier
curl http://localhost:5000/api/matches?team=chelsea
```

Response:
```json
{
  "success": true,
  "count": 25,
  "matches": [
    {
      "home_team": "Manchester United",
      "away_team": "Liverpool",
      "date": "Dec 12, 2025 15:00",
      "competition": "Premier League",
      "preview_url": "https://www.sportsmole.co.uk/football/.../preview",
      "predicted_score": "2-1",
      "prediction_text": "...",
      "statistics": {...}
    }
  ],
  "last_updated": "2025-12-11T04:56:29.639Z"
}
```

### Get Match Count

**GET /api/matches/count**
```json
{
  "success": true,
  "count": 25,
  "last_updated": "2025-12-11T04:56:29.639Z"
}
```

### Get Specific Match

**GET /api/matches/{match_id}**

Returns a specific match by its index (0-based).

Example:
```bash
curl http://localhost:5000/api/matches/0
```

### Refresh Cache

**POST /api/refresh**

Forces a refresh of the cached match data.

Example:
```bash
curl -X POST http://localhost:5000/api/refresh
```

## Project Structure

```
sportsmole-scraper/
├── scraper.py              # Main scraper logic
├── api.py                  # Flask REST API
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── test_offline.py         # Unit tests
├── example_usage.py        # Usage examples
├── start_api.sh            # Startup script
├── Dockerfile              # Docker container definition
├── docker-compose.yml      # Docker Compose configuration
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── API_DOCUMENTATION.md   # Complete API reference
└── QUICKSTART.md          # Quick start guide
```

## How It Works

### Scraper (`scraper.py`)

The `SportsMoleScraper` class handles all web scraping operations:

1. **Fetching Matches**: Connects to SportsMole's fixtures page and parses HTML to extract match information
2. **Parsing Predictions**: For each match with a preview URL, fetches the preview page and extracts predictions
3. **Statistics Extraction**: Parses match statistics from preview pages
4. **Error Handling**: Implements robust error handling for network issues and parsing failures

### API (`api.py`)

The Flask API provides a REST interface to the scraper:

1. **Caching**: Implements a 30-minute cache to avoid excessive requests to SportsMole
2. **Endpoints**: Exposes various endpoints for accessing match data
3. **Filtering**: Supports filtering by competition and team
4. **Logging**: Comprehensive logging for debugging and monitoring

## Configuration

You can configure the scraper by editing `config.py` or using environment variables:

### Environment Variables

```bash
# API settings
export API_HOST="0.0.0.0"
export API_PORT="5000"
export DEBUG_MODE="false"  # Always false for production!

# Then run the API
python api.py
```

### Configuration File

Edit `config.py` to change default settings:
- Base URLs
- Request timeout and retry settings
- Cache duration
- API host and port
- Debug mode (set to False for production)

**Security Note**: Never run with `DEBUG_MODE=true` in production environments. Debug mode can expose sensitive information and allow arbitrary code execution.

## Development

### Adding New Features

To extend the scraper:

1. Modify `scraper.py` to add new parsing methods
2. Update `api.py` to expose new data through endpoints
3. Test thoroughly with `python scraper.py` and `python api.py`

### Error Handling

The scraper includes multiple fallback strategies:
- Alternative CSS selectors for different page layouts
- Graceful degradation if certain data is unavailable
- Comprehensive error logging

## Dependencies

- **requests**: HTTP library for making requests to SportsMole
- **beautifulsoup4**: HTML parsing and extraction
- **flask**: REST API framework
- **lxml**: Fast XML/HTML parser
- **python-dateutil**: Date parsing utilities

## Limitations

- The scraper depends on SportsMole's HTML structure, which may change
- Rate limiting: Be respectful of SportsMole's servers (caching helps)
- Some statistics may not be available for all matches
- Predictions are only available for matches with preview pages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational purposes. Please respect SportsMole's terms of service when using this scraper.

## Disclaimer

This scraper is for educational and personal use only. Always respect the website's robots.txt and terms of service. Consider using official APIs when available.