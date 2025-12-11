"""
SportsMole Web Scraper
Scrapes upcoming matches, statistics, and predictions from sportsmole.co.uk
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import re
import time
import logging
from config import (
    BASE_URL, FOOTBALL_URL, FIXTURES_URL,
    REQUEST_TIMEOUT, USER_AGENT,
    MAX_RETRIES, RETRY_DELAY, LOG_LEVEL, LOG_FORMAT
)

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class SportsMoleScraper:
    """Scraper for SportsMole.co.uk website"""
    
    BASE_URL = BASE_URL
    FOOTBALL_URL = FOOTBALL_URL
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT
        })
        self.timeout = REQUEST_TIMEOUT
        logger.info("SportsMoleScraper initialized")
    
    def get_upcoming_matches(self) -> List[Dict]:
        """
        Fetch all upcoming matches from SportsMole
        
        Returns:
            List of dictionaries containing match information
        """
        matches = []
        
        for attempt in range(MAX_RETRIES):
            try:
                # Get the main football fixtures page
                logger.info(f"Fetching fixtures from {FIXTURES_URL} (attempt {attempt + 1}/{MAX_RETRIES})")
                response = self.session.get(FIXTURES_URL, timeout=self.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find all match containers - try multiple strategies
                match_elements = soup.find_all('div', class_='match-preview')
                
                if not match_elements:
                    logger.debug("No match-preview divs found, trying alternative selectors")
                    match_elements = soup.find_all('div', class_='fixture')
                
                if not match_elements:
                    match_elements = soup.find_all('div', class_='match')
                
                logger.info(f"Found {len(match_elements)} match elements")
                
                for match_elem in match_elements:
                    match_data = self._parse_match_element(match_elem)
                    if match_data:
                        matches.append(match_data)
                
                # If no matches found with preview divs, try table format
                if not matches:
                    logger.debug("Trying table-based parsing")
                    matches = self._parse_matches_from_tables(soup)
                
                logger.info(f"Successfully parsed {len(matches)} matches")
                break  # Success, exit retry loop
                    
            except requests.RequestException as e:
                logger.error(f"Error fetching matches (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error("Max retries reached, returning empty list")
        
        return matches
    
    def _parse_match_element(self, element) -> Optional[Dict]:
        """Parse a single match element into structured data"""
        try:
            match_data = {}
            
            # Extract teams - try multiple strategies
            teams = element.find_all('span', class_='team-name')
            if len(teams) >= 2:
                match_data['home_team'] = teams[0].get_text(strip=True)
                match_data['away_team'] = teams[1].get_text(strip=True)
            else:
                # Try alternative parsing with links
                team_links = element.find_all('a', href=re.compile(r'/football/[^/]+/'))
                if len(team_links) >= 2:
                    match_data['home_team'] = team_links[0].get_text(strip=True)
                    match_data['away_team'] = team_links[1].get_text(strip=True)
                else:
                    # Try finding by class patterns
                    home = element.find(class_=re.compile(r'home.*team', re.I))
                    away = element.find(class_=re.compile(r'away.*team', re.I))
                    if home and away:
                        match_data['home_team'] = home.get_text(strip=True)
                        match_data['away_team'] = away.get_text(strip=True)
            
            # Extract date/time
            date_elem = element.find('span', class_='match-date') or element.find('time')
            if not date_elem:
                date_elem = element.find(class_=re.compile(r'date|time', re.I))
            if date_elem:
                match_data['date'] = date_elem.get_text(strip=True)
            
            # Extract competition
            comp_elem = element.find('span', class_='competition') or element.find('a', class_='competition')
            if not comp_elem:
                comp_elem = element.find(class_=re.compile(r'competition|league', re.I))
            if comp_elem:
                match_data['competition'] = comp_elem.get_text(strip=True)
            
            # Extract match link for detailed info
            link_elem = element.find('a', href=re.compile(r'/football/.*?/preview'))
            if link_elem:
                href = link_elem.get('href', '')
                if not href.startswith('http'):
                    match_data['preview_url'] = self.BASE_URL + href
                else:
                    match_data['preview_url'] = href
            
            if 'home_team' in match_data and 'away_team' in match_data:
                logger.debug(f"Parsed match: {match_data['home_team']} vs {match_data['away_team']}")
                return match_data
            else:
                logger.debug("Could not extract both teams from element")
                return None
            
        except Exception as e:
            logger.error(f"Error parsing match element: {e}", exc_info=True)
            return None
    
    def _parse_matches_from_tables(self, soup) -> List[Dict]:
        """Alternative parsing method for table-based layouts"""
        matches = []
        
        try:
            # Look for fixture tables
            tables = soup.find_all('table', class_='fixtures')
            
            for table in tables:
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 3:
                        match_data = {
                            'home_team': cells[0].get_text(strip=True),
                            'away_team': cells[2].get_text(strip=True),
                            'date': cells[1].get_text(strip=True) if len(cells) > 1 else 'TBD'
                        }
                        
                        # Try to find preview link
                        link = row.find('a', href=re.compile(r'/preview'))
                        if link:
                            match_data['preview_url'] = self.BASE_URL + link['href']
                        
                        matches.append(match_data)
        
        except Exception as e:
            print(f"Error parsing table matches: {e}")
        
        return matches
    
    def get_match_prediction(self, preview_url: str) -> Optional[Dict]:
        """
        Fetch prediction details for a specific match
        
        Args:
            preview_url: URL to the match preview page
            
        Returns:
            Dictionary containing prediction information
        """
        for attempt in range(MAX_RETRIES):
            try:
                logger.debug(f"Fetching prediction from {preview_url} (attempt {attempt + 1}/{MAX_RETRIES})")
                response = self.session.get(preview_url, timeout=self.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                prediction_data = {}
                
                # Look for prediction section
                prediction_section = soup.find('div', class_='prediction') or soup.find('div', id='prediction')
                
                if prediction_section:
                    # Extract predicted score
                    score_elem = prediction_section.find('span', class_='score') or prediction_section.find('div', class_='predicted-score')
                    if score_elem:
                        prediction_data['predicted_score'] = score_elem.get_text(strip=True)
                        logger.debug(f"Found predicted score: {prediction_data['predicted_score']}")
                    
                    # Extract prediction text/reasoning
                    pred_text = prediction_section.find('p') or prediction_section.find('div', class_='prediction-text')
                    if pred_text:
                        prediction_data['prediction_text'] = pred_text.get_text(strip=True)
                
                # Look for statistics
                stats_section = soup.find('div', class_='statistics') or soup.find('div', id='statistics')
                if stats_section:
                    prediction_data['statistics'] = self._parse_statistics(stats_section)
                
                # Alternative: Look for SM Prediction box
                sm_prediction = soup.find('div', class_='sm-prediction')
                if sm_prediction:
                    score_text = sm_prediction.get_text(strip=True)
                    prediction_data['sm_predicted_score'] = score_text
                    logger.debug(f"Found SM predicted score: {score_text}")
                
                # Look for any element with "prediction" in class
                if not prediction_data:
                    pred_elements = soup.find_all(class_=re.compile(r'predict', re.I))
                    for elem in pred_elements:
                        text = elem.get_text(strip=True)
                        if text and len(text) > 0:
                            prediction_data['prediction_info'] = text
                            break
                
                if prediction_data:
                    logger.debug(f"Successfully parsed prediction data: {list(prediction_data.keys())}")
                else:
                    logger.debug("No prediction data found on page")
                
                return prediction_data if prediction_data else None
                
            except requests.RequestException as e:
                logger.error(f"Error fetching prediction for {preview_url} (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error("Max retries reached for prediction fetch")
                    return None
    
    def _parse_statistics(self, stats_section) -> Dict:
        """Parse statistics from a statistics section"""
        statistics = {}
        
        try:
            # Look for stat rows
            stat_rows = stats_section.find_all('div', class_='stat-row')
            
            for row in stat_rows:
                label = row.find('span', class_='stat-label')
                value = row.find('span', class_='stat-value')
                
                if label and value:
                    statistics[label.get_text(strip=True)] = value.get_text(strip=True)
            
            # Alternative: Look for table-based statistics
            if not statistics:
                stat_tables = stats_section.find_all('table')
                for table in stat_tables:
                    rows = table.find_all('tr')
                    for row in rows:
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 2:
                            key = cells[0].get_text(strip=True)
                            value = cells[1].get_text(strip=True)
                            statistics[key] = value
        
        except Exception as e:
            print(f"Error parsing statistics: {e}")
        
        return statistics
    
    def get_all_matches_with_predictions(self) -> List[Dict]:
        """
        Get all upcoming matches with their predictions and statistics
        
        Returns:
            List of dictionaries containing complete match information
        """
        matches = self.get_upcoming_matches()
        
        for match in matches:
            if 'preview_url' in match:
                prediction = self.get_match_prediction(match['preview_url'])
                if prediction:
                    match.update(prediction)
        
        return matches


if __name__ == "__main__":
    # Test the scraper
    scraper = SportsMoleScraper()
    
    print("Fetching upcoming matches...")
    matches = scraper.get_all_matches_with_predictions()
    
    print(f"\nFound {len(matches)} matches:")
    for i, match in enumerate(matches[:5], 1):  # Show first 5
        print(f"\n{i}. {match.get('home_team', 'Unknown')} vs {match.get('away_team', 'Unknown')}")
        print(f"   Date: {match.get('date', 'TBD')}")
        print(f"   Competition: {match.get('competition', 'N/A')}")
        if 'predicted_score' in match:
            print(f"   Predicted Score: {match['predicted_score']}")
        if 'sm_predicted_score' in match:
            print(f"   SM Prediction: {match['sm_predicted_score']}")
