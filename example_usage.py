"""
Example usage of the SportsMole Scraper API
This demonstrates how to use the scraper and API
"""

from scraper import SportsMoleScraper

def example_scraper_usage():
    """Example of using the scraper directly"""
    print("=" * 50)
    print("Example 1: Using the Scraper Directly")
    print("=" * 50)
    
    # Initialize the scraper
    scraper = SportsMoleScraper()
    
    # Get all upcoming matches
    print("\nFetching upcoming matches...")
    matches = scraper.get_upcoming_matches()
    
    print(f"Found {len(matches)} matches\n")
    
    # Display first few matches
    for i, match in enumerate(matches[:3], 1):
        print(f"{i}. {match.get('home_team', 'TBD')} vs {match.get('away_team', 'TBD')}")
        print(f"   Competition: {match.get('competition', 'N/A')}")
        print(f"   Date: {match.get('date', 'TBD')}")
        if 'preview_url' in match:
            print(f"   Preview: {match['preview_url']}")
        print()


def example_with_predictions():
    """Example of fetching matches with predictions"""
    print("=" * 50)
    print("Example 2: Fetching Matches with Predictions")
    print("=" * 50)
    
    scraper = SportsMoleScraper()
    
    # Get matches with predictions and statistics
    print("\nFetching matches with predictions...")
    matches = scraper.get_all_matches_with_predictions()
    
    print(f"Found {len(matches)} matches with prediction data\n")
    
    # Display matches with predictions
    for i, match in enumerate(matches[:3], 1):
        print(f"{i}. {match.get('home_team', 'TBD')} vs {match.get('away_team', 'TBD')}")
        
        if 'predicted_score' in match:
            print(f"   Predicted Score: {match['predicted_score']}")
        
        if 'sm_predicted_score' in match:
            print(f"   SM Prediction: {match['sm_predicted_score']}")
        
        if 'statistics' in match:
            print(f"   Statistics: {match['statistics']}")
        
        print()


def example_api_requests():
    """Example API requests using curl commands"""
    print("=" * 50)
    print("Example 3: API Usage")
    print("=" * 50)
    print("\nAfter starting the API with 'python api.py', you can use:\n")
    
    examples = [
        ("Get API info", "curl http://localhost:5000/"),
        ("Get all matches", "curl http://localhost:5000/api/matches"),
        ("Get first 5 matches", "curl http://localhost:5000/api/matches?limit=5"),
        ("Filter by competition", "curl http://localhost:5000/api/matches?competition=premier"),
        ("Filter by team", "curl http://localhost:5000/api/matches?team=chelsea"),
        ("Get match count", "curl http://localhost:5000/api/matches/count"),
        ("Get specific match", "curl http://localhost:5000/api/matches/0"),
        ("Force refresh cache", "curl -X POST http://localhost:5000/api/refresh"),
        ("Health check", "curl http://localhost:5000/api/health"),
    ]
    
    for title, command in examples:
        print(f"{title}:")
        print(f"  {command}\n")


def example_python_api_client():
    """Example of using the API from Python"""
    print("=" * 50)
    print("Example 4: Using API from Python")
    print("=" * 50)
    print("""
import requests

# Get all matches
response = requests.get('http://localhost:5000/api/matches')
data = response.json()

if data['success']:
    matches = data['matches']
    print(f"Found {data['count']} matches")
    
    for match in matches[:5]:
        home = match.get('home_team', 'TBD')
        away = match.get('away_team', 'TBD')
        pred = match.get('predicted_score', 'N/A')
        print(f"{home} vs {away} - Prediction: {pred}")

# Get matches for specific team
response = requests.get('http://localhost:5000/api/matches?team=Liverpool')
data = response.json()

print(f"\\nFound {data['count']} matches for Liverpool")

# Force refresh
response = requests.post('http://localhost:5000/api/refresh')
print(response.json())
""")


if __name__ == "__main__":
    print("SportsMole Scraper - Usage Examples")
    print("=" * 50)
    print()
    
    # Run examples
    try:
        example_scraper_usage()
    except Exception as e:
        print(f"Note: Scraper requires internet access. Error: {e}\n")
    
    example_with_predictions()
    example_api_requests()
    example_python_api_client()
    
    print("\n" + "=" * 50)
    print("For more information, see README.md")
    print("=" * 50)
