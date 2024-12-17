import requests
import pandas as pd
from datetime import datetime, timedelta

class NasaAPI:
    """Class to handle interactions with NASA's NeoWs API"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nasa.gov/neo/rest/v1"
    
    def get_feed(self, start_date, end_date=None):
        """
        Get asteroid data for a date range
        
        Parameters:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format (optional)
        
        Returns:
        pandas.DataFrame: Processed asteroid data
        """
        if end_date is None:
            # If no end date is provided, use 7 days after start date (API limit)
            end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')
            
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'api_key': self.api_key,
            'detailed': 'true'  # Get detailed information
        }
        
        try:
            response = requests.get(f"{self.base_url}/feed", params=params)
            response.raise_for_status()
            
            data = response.json()
            asteroids = []
            
            for date in data['near_earth_objects']:
                for asteroid in data['near_earth_objects'][date]:
                    asteroid_data = {
                        'id': asteroid['id'],
                        'name': asteroid['name'],
                        'date': date,
                        'diameter_min_km': asteroid['estimated_diameter']['kilometers']['estimated_diameter_min'],
                        'diameter_max_km': asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'],
                        'is_potentially_hazardous': asteroid['is_potentially_hazardous_asteroid'],
                        'close_approach_date': asteroid['close_approach_data'][0]['close_approach_date'],
                        'miss_distance_km': float(asteroid['close_approach_data'][0]['miss_distance']['kilometers']),
                        'relative_velocity_kph': float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])
                    }
                    asteroids.append(asteroid_data)
            
            return pd.DataFrame(asteroids)
        except Exception as e:
            raise Exception(f"Error fetching asteroid feed: {str(e)}")
    
    def get_asteroid(self, asteroid_id):
        """
        Get detailed information about a specific asteroid
        
        Parameters:
        asteroid_id (str): NASA JPL small body ID
        
        Returns:
        dict: Asteroid information
        """
        try:
            response = requests.get(
                f"{self.base_url}/neo/{asteroid_id}",
                params={'api_key': self.api_key}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Error fetching asteroid details: {str(e)}")
    
    def browse_asteroids(self):
        """
        Get a list of all known near-Earth asteroids
        
        Returns:
        pandas.DataFrame: Processed asteroid data
        """
        try:
            response = requests.get(
                f"{self.base_url}/neo/browse",
                params={'api_key': self.api_key}
            )
            response.raise_for_status()
            
            data = response.json()
            asteroids = []
            
            for asteroid in data['near_earth_objects']:
                asteroid_data = {
                    'id': asteroid['id'],
                    'name': asteroid['name'],
                    'diameter_min_km': asteroid['estimated_diameter']['kilometers']['estimated_diameter_min'],
                    'diameter_max_km': asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'],
                    'is_potentially_hazardous': asteroid['is_potentially_hazardous_asteroid'],
                    'orbital_data': asteroid.get('orbital_data', {})
                }
                asteroids.append(asteroid_data)
            
            return pd.DataFrame(asteroids)
        except Exception as e:
            raise Exception(f"Error browsing asteroids: {str(e)}")
