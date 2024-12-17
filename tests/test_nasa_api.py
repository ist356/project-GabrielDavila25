import pytest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import pandas as pd
from code.nasa_api import NasaAPI

@pytest.fixture
def api():
    """Fixture to create NasaAPI instance for each test."""
    return NasaAPI("test_key")

@pytest.mark.parametrize("mock_get", [
    pytest.param(Mock(), id="success")
])
def test_get_feed_success(mock_get, api):
    """Test successful asteroid feed retrieval"""
    # Mock response data
    mock_response = Mock()
    mock_response.json.return_value = {
        'near_earth_objects': {
            '2023-01-01': [{
                'id': '1',
                'name': 'Test Asteroid',
                'estimated_diameter': {
                    'kilometers': {
                        'estimated_diameter_min': 0.1,
                        'estimated_diameter_max': 0.2
                    }
                },
                'is_potentially_hazardous_asteroid': False,
                'close_approach_data': [{
                    'close_approach_date': '2023-01-01',
                    'miss_distance': {'kilometers': '100000'},
                    'relative_velocity': {'kilometers_per_hour': '50000'}
                }]
            }]
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    with patch('requests.get', return_value=mock_response):
        # Test the method
        df = api.get_feed('2023-01-01')
        
        # Assertions
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert df.iloc[0]['id'] == '1'
        assert df.iloc[0]['name'] == 'Test Asteroid'
        assert df.iloc[0]['miss_distance_km'] == 100000.0
        assert df.iloc[0]['relative_velocity_kph'] == 50000.0

def test_get_feed_with_end_date(api):
    """Test asteroid feed retrieval with specific end date"""
    mock_response = Mock()
    mock_response.json.return_value = {'near_earth_objects': {}}
    mock_response.raise_for_status.return_value = None
    
    with patch('requests.get', return_value=mock_response) as mock_get:
        api.get_feed('2023-01-01', '2023-01-07')
        
        # Verify correct parameters were used
        mock_get.assert_called_with(
            f"{api.base_url}/feed",
            params={
                'start_date': '2023-01-01',
                'end_date': '2023-01-07',
                'api_key': 'test_key',
                'detailed': 'true'
            }
        )

def test_get_feed_error(api):
    """Test error handling in get_feed"""
    with patch('requests.get', side_effect=Exception("API Error")):
        with pytest.raises(Exception) as exc_info:
            api.get_feed('2023-01-01')
        assert "Error fetching asteroid feed" in str(exc_info.value)

def test_get_asteroid_success(api):
    """Test successful individual asteroid retrieval"""
    mock_response = Mock()
    mock_response.json.return_value = {
        'id': '2',
        'name': 'Specific Asteroid',
        'nasa_jpl_url': 'http://example.com'
    }
    mock_response.raise_for_status.return_value = None
    
    with patch('requests.get', return_value=mock_response):
        result = api.get_asteroid('2')
        assert result['id'] == '2'
        assert result['name'] == 'Specific Asteroid'

def test_get_asteroid_error(api):
    """Test error handling in get_asteroid"""
    with patch('requests.get', side_effect=Exception("API Error")):
        with pytest.raises(Exception) as exc_info:
            api.get_asteroid('invalid_id')
        assert "Error fetching asteroid details" in str(exc_info.value)

def test_browse_asteroids_success(api):
    """Test successful asteroid browsing"""
    mock_response = Mock()
    mock_response.json.return_value = {
        'near_earth_objects': [{
            'id': '3',
            'name': 'Browse Asteroid',
            'estimated_diameter': {
                'kilometers': {
                    'estimated_diameter_min': 0.3,
                    'estimated_diameter_max': 0.4
                }
            },
            'is_potentially_hazardous_asteroid': True,
            'orbital_data': {
                'orbit_class': {'orbit_class_type': 'AMO'}
            }
        }]
    }
    mock_response.raise_for_status.return_value = None
    
    with patch('requests.get', return_value=mock_response):
        df = api.browse_asteroids()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert df.iloc[0]['id'] == '3'
        assert df.iloc[0]['name'] == 'Browse Asteroid'
        assert df.iloc[0]['is_potentially_hazardous'] == True

def test_browse_asteroids_error(api):
    """Test error handling in browse_asteroids"""
    with patch('requests.get', side_effect=Exception("API Error")):
        with pytest.raises(Exception) as exc_info:
            api.browse_asteroids()
        assert "Error browsing asteroids" in str(exc_info.value)
