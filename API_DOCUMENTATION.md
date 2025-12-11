# SportsMole Scraper API Documentation

## Overview

The SportsMole Scraper API provides REST endpoints to access upcoming football matches, predictions, and statistics scraped from SportsMole.co.uk.

**Base URL**: `http://localhost:5000`

**Version**: 1.0.0

## Authentication

Currently, the API does not require authentication. This may be added in future versions.

## Rate Limiting

The API implements intelligent caching with a 30-minute cache duration to minimize requests to SportsMole. Cached data is automatically refreshed when it expires.

## Endpoints

### 1. API Information

**Endpoint**: `GET /`

**Description**: Returns API information and available endpoints.

**Example Request**:
```bash
curl http://localhost:5000/
```

**Example Response**:
```json
{
  "name": "SportsMole Scraper API",
  "version": "1.0.0",
  "description": "API for scraping upcoming matches and predictions from SportsMole.co.uk",
  "endpoints": {
    "/": "API information",
    "/api/matches": "Get all upcoming matches with predictions",
    "/api/matches/count": "Get count of upcoming matches",
    "/api/matches/<int:match_id>": "Get specific match by index",
    "/api/refresh": "Force refresh the cache",
    "/api/health": "Health check endpoint"
  }
}
```

---

### 2. Health Check

**Endpoint**: `GET /api/health`

**Description**: Check the health status of the API and cache.

**Example Request**:
```bash
curl http://localhost:5000/api/health
```

**Example Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-11T05:00:00.000Z",
  "cache_valid": true,
  "matches_cached": 25
}
```

---

### 3. Get All Matches

**Endpoint**: `GET /api/matches`

**Description**: Retrieve all upcoming matches with predictions and statistics.

**Query Parameters**:
- `limit` (optional, integer): Maximum number of matches to return
- `competition` (optional, string): Filter by competition name (case-insensitive partial match)
- `team` (optional, string): Filter by team name (home or away, case-insensitive partial match)

**Example Requests**:

Get all matches:
```bash
curl http://localhost:5000/api/matches
```

Get first 5 matches:
```bash
curl http://localhost:5000/api/matches?limit=5
```

Filter by competition:
```bash
curl http://localhost:5000/api/matches?competition=premier
curl http://localhost:5000/api/matches?competition=champions%20league
```

Filter by team:
```bash
curl http://localhost:5000/api/matches?team=chelsea
curl http://localhost:5000/api/matches?team=manchester
```

Combine filters:
```bash
curl http://localhost:5000/api/matches?competition=premier&limit=10
```

**Example Response**:
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
      "preview_url": "https://www.sportsmole.co.uk/football/manchester-united/preview/...",
      "predicted_score": "2-1",
      "prediction_text": "Manchester United are expected to edge this encounter...",
      "statistics": {
        "Goals Scored (Home)": "28",
        "Goals Scored (Away)": "32",
        "Clean Sheets (Home)": "6",
        "Clean Sheets (Away)": "8"
      }
    },
    {
      "home_team": "Chelsea",
      "away_team": "Arsenal",
      "date": "Dec 13, 2025 17:30",
      "competition": "Premier League",
      "preview_url": "https://www.sportsmole.co.uk/football/chelsea/preview/...",
      "sm_predicted_score": "1-1"
    }
  ],
  "last_updated": "2025-12-11T05:00:00.000Z"
}
```

**Response Fields**:
- `success` (boolean): Whether the request was successful
- `count` (integer): Number of matches returned
- `matches` (array): Array of match objects
- `last_updated` (string): ISO timestamp of when cache was last updated

**Match Object Fields**:
- `home_team` (string): Name of the home team
- `away_team` (string): Name of the away team
- `date` (string): Match date and time
- `competition` (string): Competition/league name
- `preview_url` (string): URL to the match preview on SportsMole
- `predicted_score` (string, optional): Predicted final score
- `sm_predicted_score` (string, optional): SportsMole's predicted score
- `prediction_text` (string, optional): Text explanation of the prediction
- `statistics` (object, optional): Match statistics

---

### 4. Get Match Count

**Endpoint**: `GET /api/matches/count`

**Description**: Get the total count of cached upcoming matches.

**Example Request**:
```bash
curl http://localhost:5000/api/matches/count
```

**Example Response**:
```json
{
  "success": true,
  "count": 25,
  "last_updated": "2025-12-11T05:00:00.000Z"
}
```

---

### 5. Get Specific Match

**Endpoint**: `GET /api/matches/<match_id>`

**Description**: Retrieve a specific match by its index (0-based).

**Path Parameters**:
- `match_id` (integer): Index of the match (0 to count-1)

**Example Request**:
```bash
curl http://localhost:5000/api/matches/0
curl http://localhost:5000/api/matches/5
```

**Example Response** (Success):
```json
{
  "success": true,
  "match": {
    "home_team": "Manchester United",
    "away_team": "Liverpool",
    "date": "Dec 12, 2025 15:00",
    "competition": "Premier League",
    "preview_url": "https://www.sportsmole.co.uk/football/...",
    "predicted_score": "2-1"
  }
}
```

**Example Response** (Not Found):
```json
{
  "success": false,
  "error": "Match not found",
  "valid_range": "0 to 24"
}
```

**Status Codes**:
- `200 OK`: Match found
- `404 Not Found`: Match index out of range

---

### 6. Force Refresh Cache

**Endpoint**: `POST /api/refresh`

**Description**: Force a refresh of the cached match data by fetching fresh data from SportsMole.

**Example Request**:
```bash
curl -X POST http://localhost:5000/api/refresh
```

**Example Response** (Success):
```json
{
  "success": true,
  "message": "Cache refreshed successfully",
  "matches_count": 25,
  "last_updated": "2025-12-11T05:15:00.000Z"
}
```

**Example Response** (Error):
```json
{
  "success": false,
  "error": "Failed to refresh cache"
}
```

**Status Codes**:
- `200 OK`: Cache refreshed successfully
- `500 Internal Server Error`: Failed to refresh cache

---

## Error Responses

### 404 Not Found
```json
{
  "success": false,
  "error": "Endpoint not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## Using the API with Python

### Example: Get All Matches
```python
import requests

response = requests.get('http://localhost:5000/api/matches')
data = response.json()

if data['success']:
    for match in data['matches']:
        print(f"{match['home_team']} vs {match['away_team']}")
        if 'predicted_score' in match:
            print(f"Prediction: {match['predicted_score']}")
```

### Example: Filter by Team
```python
import requests

team = "Chelsea"
response = requests.get(f'http://localhost:5000/api/matches?team={team}')
data = response.json()

print(f"Found {data['count']} matches for {team}")
for match in data['matches']:
    print(f"{match['home_team']} vs {match['away_team']} - {match['date']}")
```

### Example: Get Limited Results
```python
import requests

response = requests.get('http://localhost:5000/api/matches?limit=5')
data = response.json()

print(f"Next 5 matches:")
for i, match in enumerate(data['matches'], 1):
    print(f"{i}. {match['home_team']} vs {match['away_team']}")
```

---

## Using the API with JavaScript

### Example: Fetch Matches
```javascript
fetch('http://localhost:5000/api/matches?limit=10')
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      data.matches.forEach(match => {
        console.log(`${match.home_team} vs ${match.away_team}`);
        if (match.predicted_score) {
          console.log(`Prediction: ${match.predicted_score}`);
        }
      });
    }
  })
  .catch(error => console.error('Error:', error));
```

### Example: Filter by Competition
```javascript
async function getMatchesByCompetition(competition) {
  try {
    const response = await fetch(
      `http://localhost:5000/api/matches?competition=${encodeURIComponent(competition)}`
    );
    const data = await response.json();
    
    if (data.success) {
      console.log(`Found ${data.count} matches in ${competition}`);
      return data.matches;
    }
  } catch (error) {
    console.error('Error fetching matches:', error);
  }
}

getMatchesByCompetition('Premier League');
```

---

## Caching Behavior

The API implements automatic caching with the following behavior:

1. **Cache Duration**: 30 minutes (configurable in `config.py`)
2. **Automatic Refresh**: Cache is automatically refreshed when:
   - First request is made and cache is empty
   - A request is made after cache has expired
3. **Manual Refresh**: Use the `/api/refresh` endpoint to force a cache refresh
4. **Cache Status**: Check cache validity with the `/api/health` endpoint

---

## Notes

- The scraper depends on SportsMole's HTML structure. If the website changes, the scraper may need updates.
- Be respectful of SportsMole's servers. The caching mechanism helps reduce unnecessary requests.
- Some matches may not have predictions available.
- Statistics availability varies by match.

---

## Support

For issues or questions, please open an issue on the GitHub repository.
