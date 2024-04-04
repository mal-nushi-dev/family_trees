import configparser
from cachetools import cached, LRUCache
import pandas as pd
import googlemaps


class GeocodeManager:
    """Manages geocoding operations"""
    cache = LRUCache(maxsize=1000)

    def __init__(self, file):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.file = file

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
        df = pd.read_csv(self.file)
        api_key = self.config['google_api']['api_key']
        gmaps = googlemaps.Client(key=api_key)
        df['coordinates'] = df['Birth place'].apply(
            lambda x: self._geocode_place(x, gmaps) if pd.notnull(x) else None)
        return df

    def run(self):
        """
        Runs the geocoding process by calling the add_coordinates method.
        This method adds coordinates to a DataFrame of birthplaces and
            returns the DataFrame.

        Returns:
            DataFrame: The DataFrame with added coordinates.
        """
        return self.add_coordinates()
