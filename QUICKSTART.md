# Quick Start Guide

Get started with SportsMole Scraper in 5 minutes!

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Internet connection

## Installation

### Option 1: Standard Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/foyem/sportsmole-scraper.git
   cd sportsmole-scraper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API**:
   ```bash
   python api.py
   ```
   
   Or use the startup script:
   ```bash
   ./start_api.sh
   ```

4. **Test the API**:
   ```bash
   curl http://localhost:5000/api/health
   ```

### Option 2: Docker Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/foyem/sportsmole-scraper.git
   cd sportsmole-scraper
   ```

2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Test the API**:
   ```bash
   curl http://localhost:5000/api/health
   ```

## Basic Usage

### Using the Scraper Directly

```python
from scraper import SportsMoleScraper

# Initialize scraper
scraper = SportsMoleScraper()

# Get upcoming matches
matches = scraper.get_upcoming_matches()
print(f"Found {len(matches)} matches")

# Get matches with predictions
matches_with_predictions = scraper.get_all_matches_with_predictions()
for match in matches_with_predictions[:5]:
    print(f"{match['home_team']} vs {match['away_team']}")
    if 'predicted_score' in match:
        print(f"  Predicted: {match['predicted_score']}")
```

### Using the REST API

#### Get All Matches
```bash
curl http://localhost:5000/api/matches
```

#### Get Limited Results
```bash
curl http://localhost:5000/api/matches?limit=5
```

#### Filter by Team
```bash
curl http://localhost:5000/api/matches?team=chelsea
```

#### Filter by Competition
```bash
curl http://localhost:5000/api/matches?competition=premier
```

#### Get Match Count
```bash
curl http://localhost:5000/api/matches/count
```

#### Get Specific Match
```bash
curl http://localhost:5000/api/matches/0
```

#### Refresh Cache
```bash
curl -X POST http://localhost:5000/api/refresh
```

#### Health Check
```bash
curl http://localhost:5000/api/health
```

## Python Client Example

```python
import requests

# Base URL
BASE_URL = "http://localhost:5000"

# Get all matches
response = requests.get(f"{BASE_URL}/api/matches")
data = response.json()

if data['success']:
    print(f"Total matches: {data['count']}")
    
    for match in data['matches'][:5]:  # Show first 5
        home = match['home_team']
        away = match['away_team']
        date = match.get('date', 'TBD')
        
        print(f"\n{home} vs {away}")
        print(f"Date: {date}")
        
        if 'predicted_score' in match:
            print(f"Prediction: {match['predicted_score']}")
        
        if 'competition' in match:
            print(f"Competition: {match['competition']}")

# Filter by specific team
team = "Liverpool"
response = requests.get(f"{BASE_URL}/api/matches?team={team}")
data = response.json()

print(f"\n\nMatches for {team}: {data['count']}")
for match in data['matches']:
    print(f"- {match['home_team']} vs {match['away_team']}")
```

## JavaScript/Node.js Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:5000';

async function getMatches() {
  try {
    const response = await axios.get(`${BASE_URL}/api/matches?limit=5`);
    const data = response.data;
    
    if (data.success) {
      console.log(`Found ${data.count} matches:`);
      
      data.matches.forEach((match, index) => {
        console.log(`\n${index + 1}. ${match.home_team} vs ${match.away_team}`);
        console.log(`   Date: ${match.date || 'TBD'}`);
        
        if (match.predicted_score) {
          console.log(`   Prediction: ${match.predicted_score}`);
        }
      });
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}

getMatches();
```

## Configuration

Edit `config.py` to customize:

```python
# API settings
API_HOST = "0.0.0.0"  # Listen on all interfaces
API_PORT = 5000        # API port
DEBUG_MODE = True      # Enable debug mode

# Cache settings
CACHE_DURATION_MINUTES = 30  # Cache duration

# Scraper settings
REQUEST_TIMEOUT = 30    # Request timeout in seconds
MAX_RETRIES = 3         # Maximum retry attempts
RETRY_DELAY = 2         # Delay between retries
```

## Troubleshooting

### Problem: Dependencies not found
**Solution**: Install dependencies with `pip install -r requirements.txt`

### Problem: Port 5000 already in use
**Solution**: Change `API_PORT` in `config.py` to a different port (e.g., 8080)

### Problem: No matches returned
**Solution**: 
1. Check your internet connection
2. Verify SportsMole.co.uk is accessible
3. Check logs for error messages

### Problem: API not responding
**Solution**:
1. Check if the API is running: `curl http://localhost:5000/api/health`
2. Check firewall settings
3. Verify the correct host and port in `config.py`

## Testing

Run the offline tests:
```bash
python test_offline.py
```

Run example usage:
```bash
python example_usage.py
```

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference
- Explore [example_usage.py](example_usage.py) for more examples
- Customize [config.py](config.py) for your needs

## Need Help?

- Check the [API Documentation](API_DOCUMENTATION.md)
- Read the [README](README.md)
- Open an issue on GitHub

---

Happy scraping! 🏆⚽
