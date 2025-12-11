"""
Flask API for SportsMole Scraper
Provides REST endpoints to access scraped match data
"""

from flask import Flask, jsonify, request
from scraper import SportsMoleScraper
from datetime import datetime
import logging
from config import (
    API_HOST, API_PORT, DEBUG_MODE,
    CACHE_DURATION_MINUTES, LOG_LEVEL, LOG_FORMAT
)

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
scraper = SportsMoleScraper()

# Cache for storing scraped data (in production, use Redis or similar)
cache = {
    'matches': [],
    'last_updated': None
}


def is_cache_valid():
    """Check if cached data is still valid"""
    if not cache['last_updated']:
        return False
    
    elapsed = (datetime.now() - cache['last_updated']).total_seconds() / 60
    return elapsed < CACHE_DURATION_MINUTES


def update_cache():
    """Update the cache with fresh data"""
    logger.info("Updating cache with fresh match data...")
    try:
        matches = scraper.get_all_matches_with_predictions()
        cache['matches'] = matches
        cache['last_updated'] = datetime.now()
        logger.info(f"Cache updated successfully with {len(matches)} matches")
        return True
    except Exception as e:
        logger.error(f"Error updating cache: {e}")
        return False


@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        'name': 'SportsMole Scraper API',
        'version': '1.0.0',
        'description': 'API for scraping upcoming matches and predictions from SportsMole.co.uk',
        'endpoints': {
            '/': 'API information',
            '/api/matches': 'Get all upcoming matches with predictions',
            '/api/matches/count': 'Get count of upcoming matches',
            '/api/matches/<int:match_id>': 'Get specific match by index',
            '/api/refresh': 'Force refresh the cache',
            '/api/health': 'Health check endpoint'
        }
    })


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'cache_valid': is_cache_valid(),
        'matches_cached': len(cache['matches'])
    })


@app.route('/api/matches', methods=['GET'])
def get_matches():
    """
    Get all upcoming matches with predictions and statistics
    
    Query parameters:
        - limit: Maximum number of matches to return (default: all)
        - competition: Filter by competition name
        - team: Filter by team name (home or away)
    """
    # Check cache and update if needed
    if not is_cache_valid():
        logger.info("Cache expired, fetching fresh data...")
        update_cache()
    
    matches = cache['matches']
    
    # Apply filters
    limit = request.args.get('limit', type=int)
    competition = request.args.get('competition', type=str)
    team = request.args.get('team', type=str)
    
    if competition:
        matches = [m for m in matches if competition.lower() in m.get('competition', '').lower()]
    
    if team:
        matches = [m for m in matches if 
                  team.lower() in m.get('home_team', '').lower() or 
                  team.lower() in m.get('away_team', '').lower()]
    
    if limit:
        matches = matches[:limit]
    
    return jsonify({
        'success': True,
        'count': len(matches),
        'matches': matches,
        'last_updated': cache['last_updated'].isoformat() if cache['last_updated'] else None
    })


@app.route('/api/matches/count', methods=['GET'])
def get_matches_count():
    """Get the count of upcoming matches"""
    if not is_cache_valid():
        update_cache()
    
    return jsonify({
        'success': True,
        'count': len(cache['matches']),
        'last_updated': cache['last_updated'].isoformat() if cache['last_updated'] else None
    })


@app.route('/api/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """Get a specific match by its index"""
    if not is_cache_valid():
        update_cache()
    
    if 0 <= match_id < len(cache['matches']):
        return jsonify({
            'success': True,
            'match': cache['matches'][match_id]
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Match not found',
            'valid_range': f'0 to {len(cache["matches"]) - 1}'
        }), 404


@app.route('/api/refresh', methods=['POST'])
def refresh_cache():
    """Force refresh the cache"""
    success = update_cache()
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Cache refreshed successfully',
            'matches_count': len(cache['matches']),
            'last_updated': cache['last_updated'].isoformat()
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to refresh cache'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Initialize cache on startup
    logger.info("Starting SportsMole Scraper API...")
    
    # Security warning for debug mode
    if DEBUG_MODE:
        logger.warning("=" * 60)
        logger.warning("WARNING: Running in DEBUG mode!")
        logger.warning("Debug mode should NEVER be used in production.")
        logger.warning("Set DEBUG_MODE=False in config.py for production use.")
        logger.warning("=" * 60)
    
    update_cache()
    
    # Run the Flask app
    logger.info(f"API will run on {API_HOST}:{API_PORT}")
    app.run(host=API_HOST, port=API_PORT, debug=DEBUG_MODE)
