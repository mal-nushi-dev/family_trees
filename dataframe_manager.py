import pandas as pd
import configparser
from cachetools import cached, LRUCache
import googlemaps


class CreateDataFrame:
    """
    A class used to create a pandas DataFrame from a CSV file.

    Attributes
    ----------
    file (str): A string representing the path to the CSV file

    Methods
    -------
    create_dataframe(): Returns a pandas DataFrame created from the CSV file.
    """

    def __init__(self, file: str) -> None:
        """
        Constructs all the necessary attributes for the CreateDataFrame object.

        Parameters
        ----------
        file (str): A string representing the path to the CSV file
        """
        self.file = file

    def create_dataframe(self) -> pd.DataFrame:
        """
        Returns a pandas DataFrame created from the CSV file.

        Returns
        -------
        pd.DataFrame: A pandas DataFrame created from the CSV file
        """
        df = pd.read_csv(self.file)
        return df


class GeocodeManager:
    """
    Manages the geocoding of birthplaces using the Google Maps API,
    employing caching to optimize API usage.

    This class takes a DataFrame containing birthplaces, utilizes the
    Google Maps API to geocode these locations, and appends the results as
    coordinates to the DataFrame. Caching is used to minimize repeat API calls
    for the same locations, enhancing efficiency and reducing cost.

    Attributes:
    ------
    df (pd.DataFrame): DataFrame containing birthplaces.
    cache (LRUCache): A least-recently-used (LRU) cache to store geocoding
                      results and minimize API calls.

    Usage:
    ------
    >>> geocode_manager = GeocodeManager(df)
    >>> coordinates_df = geocode_manager.run()
    """
    cache = LRUCache(maxsize=1000)

    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.df = dataframe

    @cached(cache)
    def _geocode_place(self, birthplace: str, gmaps: googlemaps.Client) -> str:
        """
        Geocodes a birthplace using the Google Maps API, with results
        cached to improve efficiency.

        Parameters:
        ------
        birthplace (str): The birthplace to geocode.
        gmaps (googlemaps.Client): The Google Maps client instance configured with an API key.

        Returns:
        ------
        str | None: The coordinates of the birthplace as a string
                    '(latitude, longitude)', or None if geocoding fails.
        """
        geocode_result = gmaps.geocode(birthplace)
        if geocode_result:
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            return str((latitude, longitude))

    def add_coordinates(self) -> pd.DataFrame:
        """
        Adds coordinates to the DataFrame of birthplaces read from a CSV file.

        Utilizes the Google Maps API to geocode each birthplace and
        appends the result as a new column. Caching is employed to minimize
        repeat API calls for previously geocoded locations.

        Returns:
        ------
        pd.DataFrame: The updated DataFrame with a new 'coordinates' column containing geocoded coordinates.
        """
        api_key = self.config['google_api']['api_key']
        gmaps = googlemaps.Client(key=api_key)
        self.df['Birth place coordinates'] = self.df['Birth place'].apply(
            lambda x: self._geocode_place(x, gmaps) if pd.notnull(x) else None)
        return self.df

    def run(self) -> pd.DataFrame:
        """
        Executes the geocoding process, enhancing a DataFrame with geocoded
        coordinates for birthplaces.

        This method orchestrates reading birthplace data, geocoding each
        location, and returning the enhanced DataFrame.

        Returns:
        ------
        pd.DataFrame: The DataFrame augmented with a 'coordinates' column for geocoded birthplaces.
        """
        return self.add_coordinates()


class ColumnManager:
    """
    A class for managing columns in a DataFrame.

    Parameters:
    ------
    dataframe (pd.DataFrame): The DataFrame to be managed.

    Attributes:
    ------
    df (pd.DataFrame): The DataFrame being managed.
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Initializes a new instance of the ColumnManager class.

        Parameters:
        ------
        dataframe (pd.DataFrame): The DataFrame to be managed.
        """
        self.df = dataframe

    def upper_case_columns(self) -> "ColumnManager":
        """
        Converts all column names to uppercase.

        Returns:
        ------
        ColumnManager: The instance itself after modifying column names.
        """
        self.df.rename(columns=str.upper, inplace=True)
        return self

    def whitespace_management(self) -> "ColumnManager":
        """
        Manages whitespace in column names by replacing spaces with underscores.

        Returns:
        ------
        ColumnManager: The instance itself after modifying column names.
        """
        self.df.columns = self.df.columns.str.strip().str.replace(' ', '_')
        return self
