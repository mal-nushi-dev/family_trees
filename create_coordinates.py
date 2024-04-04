import configparser
from cachetools import cached, LRUCache
import pandas as pd
import googlemaps
from create_database import DatabaseManager


class GeocodeManager:
    """Manages geocoding operations"""
    cache = LRUCache(maxsize=1000)

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    @cached(cache)
    def _geocode_place(self, birthplace, gmaps):
        """
        Geocodes a birthplace using the Google Maps API.

        Args:
            birthplace (str): The birthplace to geocode.
            gmaps (googlemaps.Client): The Google Maps client.

        Returns:
            str: The coordinates of birthplace, or None if geocoding failed.
        """
        geocode_result = gmaps.geocode(birthplace)
        if geocode_result:
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            return str((latitude, longitude))

    def add_coordinates(self):
        """
        Adds coordinates to a DataFrame of birthplaces and saves it to a db.
        """
        df = pd.read_csv('data/csv/Nushi-Genealogy-3-Apr-2024-214612115.csv')
        api_key = self.config['google_api']['api_key']
        gmaps = googlemaps.Client(key=api_key)
        df['coordinates'] = df['Birth place'].apply(
            lambda x: self._geocode_place(x, gmaps) if pd.notnull(x) else None)
        with DatabaseManager(db_file='data/sqlite3/database.db',
                             dataframe=df) as db_manager:
            db_manager.create_table_from_dataframe()
