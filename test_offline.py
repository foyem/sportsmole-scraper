"""
Offline tests for SportsMole Scraper
Tests basic functionality without requiring internet access
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from scraper import SportsMoleScraper
from bs4 import BeautifulSoup


class TestSportsMoleScraperOffline(unittest.TestCase):
    """Test cases for SportsMoleScraper that don't require internet"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scraper = SportsMoleScraper()
    
    def test_scraper_initialization(self):
        """Test that scraper initializes correctly"""
        self.assertIsNotNone(self.scraper)
        self.assertIsNotNone(self.scraper.session)
        self.assertEqual(self.scraper.BASE_URL, "https://www.sportsmole.co.uk")
    
    def test_parse_match_element_with_teams(self):
        """Test parsing of match element with team names"""
        html = """
        <div class="match-preview">
            <span class="team-name">Manchester United</span>
            <span class="team-name">Liverpool</span>
            <span class="match-date">Dec 12, 2025 15:00</span>
            <span class="competition">Premier League</span>
            <a href="/football/match123/preview">Preview</a>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find('div', class_='match-preview')
        
        result = self.scraper._parse_match_element(element)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['home_team'], 'Manchester United')
        self.assertEqual(result['away_team'], 'Liverpool')
        self.assertEqual(result['date'], 'Dec 12, 2025 15:00')
        self.assertEqual(result['competition'], 'Premier League')
        self.assertIn('preview_url', result)
    
    def test_parse_match_element_with_links(self):
        """Test alternative parsing with team links"""
        html = """
        <div class="fixture">
            <a href="/football/manchester-united/">Manchester City</a>
            <a href="/football/chelsea/">Chelsea</a>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find('div', class_='fixture')
        
        result = self.scraper._parse_match_element(element)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['home_team'], 'Manchester City')
        self.assertEqual(result['away_team'], 'Chelsea')
    
    def test_parse_match_element_incomplete(self):
        """Test that incomplete elements return None"""
        html = """
        <div class="match-preview">
            <span class="team-name">Only One Team</span>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find('div', class_='match-preview')
        
        result = self.scraper._parse_match_element(element)
        
        self.assertIsNone(result)
    
    def test_parse_statistics(self):
        """Test parsing of statistics section"""
        html = """
        <div class="statistics">
            <div class="stat-row">
                <span class="stat-label">Goals Scored</span>
                <span class="stat-value">25</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Clean Sheets</span>
                <span class="stat-value">8</span>
            </div>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        stats_section = soup.find('div', class_='statistics')
        
        result = self.scraper._parse_statistics(stats_section)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('Goals Scored'), '25')
        self.assertEqual(result.get('Clean Sheets'), '8')
    
    def test_parse_statistics_table_format(self):
        """Test parsing of table-based statistics"""
        html = """
        <div class="statistics">
            <table>
                <tr><td>Possession</td><td>60%</td></tr>
                <tr><td>Shots</td><td>15</td></tr>
            </table>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        stats_section = soup.find('div', class_='statistics')
        
        result = self.scraper._parse_statistics(stats_section)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('Possession'), '60%')
        self.assertEqual(result.get('Shots'), '15')
    
    def test_parse_matches_from_tables(self):
        """Test parsing matches from table layout"""
        html = """
        <table class="fixtures">
            <tr>
                <td>Arsenal</td>
                <td>Dec 15, 2025</td>
                <td>Tottenham</td>
                <a href="/football/match456/preview">Preview</a>
            </tr>
            <tr>
                <td>Real Madrid</td>
                <td>Dec 16, 2025</td>
                <td>Barcelona</td>
            </tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.scraper._parse_matches_from_tables(soup)
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]['home_team'], 'Arsenal')
        self.assertEqual(result[0]['away_team'], 'Tottenham')
        self.assertIn('preview_url', result[0])


class TestAPIStructure(unittest.TestCase):
    """Test API structure without starting the server"""
    
    @patch('api.scraper')
    def test_api_imports(self, mock_scraper):
        """Test that API module imports correctly"""
        import api
        self.assertTrue(hasattr(api, 'app'))
        self.assertTrue(hasattr(api, 'get_matches'))
        self.assertTrue(hasattr(api, 'health'))
    
    def test_config_values(self):
        """Test that config has expected values"""
        import config
        self.assertTrue(hasattr(config, 'BASE_URL'))
        self.assertTrue(hasattr(config, 'API_PORT'))
        self.assertEqual(config.BASE_URL, "https://www.sportsmole.co.uk")
        self.assertEqual(config.API_PORT, 5000)


if __name__ == '__main__':
    print("Running offline tests for SportsMole Scraper")
    print("=" * 50)
    unittest.main(verbosity=2)
