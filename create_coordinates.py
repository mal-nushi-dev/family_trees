import configparser
from cachetools import cached, LRUCache
import pandas as pd
import googlemaps
import create_database


config = configparser.ConfigParser()
config.read('config.ini')

# Create instance of LRU cache
# This is used so that we are not making too many API requests for the same
#   location.
cache = LRUCache(maxsize=1000)


@cached(cache)
def geocode_place(birth_place, gmaps):
    """
    This function takes a place name as input and returns the geocoded
        latitude and longitude of the place.
    The function uses Google Maps API for geocoding. The results are cached
        using an LRU cache to optimize repeated requests.

    Args:
        birth_place (str): The name of the place to geocode.

    Returns:
        str: A string representation of a tuple containing the latitude and
            longitude of the place.
        If the geocoding fails, it returns None.
    """
    geocode_result = gmaps.geocode(birth_place)
    if geocode_result:
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
        return str((latitude, longitude))
    print(f"No geocode result for {birth_place}")
    return None


def add_coordinates():
    """
    This function reads a CSV file containing genealogy data,
        adds a new column 'coordinates' to the dataframe,
    which contains the geocoded latitude and longitude of the birth place
        of each individual in the data.
    The function uses the geocode_place function to geocode the birth places.

    Returns:
        None. The function modifies the dataframe in-place.
    """
    df = pd.read_csv('data/csv/Nushi-Genealogy-3-Apr-2024-160324198.csv')
    api_key = config['DEFAULT']['API_KEY']
    gmaps = googlemaps.Client(key=api_key)
    df['coordinates'] = df['Birth place'].apply(
        lambda x: geocode_place(x, gmaps) if pd.notnull(x) else None)
    create_database.connect_to_sqlite3(
        dataframe=df, db_file='data/sqlite3/database.db')


add_coordinates()
