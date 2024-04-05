import pandas as pd
import configparser
from cachetools import cached, LRUCache
import googlemaps


class CreateDataFrame:
    """
    A class used to create a pandas DataFrame from a CSV file.

    Attributes
    ----------
    - file (str): A string representing the path to the CSV file

    Methods
    -------
    - create_dataframe(): Returns a pandas DataFrame created from the CSV file.
    """

    def __init__(self, file: str) -> None:
        """
        Constructs all the necessary attributes for the CreateDataFrame object.

        Parameters
        ----------
        - file (str): A string representing the path to the CSV file
        """
        self.file = file

    def create_dataframe(self) -> pd.DataFrame:
        """
        Returns a pandas DataFrame created from the CSV file.

        Returns
        -------
        - pd.DataFrame: A pandas DataFrame created from the CSV file
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
    - df (pd.DataFrame): DataFrame containing birthplaces.
    - cache (LRUCache): A least-recently-used (LRU) cache to store geocoding
    results and minimize API calls.

    Methods
    -------
    - __init__(self, dataframe: pd.DataFrame): Constructs all the necessary attributes
    for the GeocodeManager object.
    - _geocode_place(self, birthplace: str, gmaps: googlemaps.Client) -> str:
    Geocodes a birthplace using the Google Maps API, with results cached to improve efficiency.
    - add_coordinates(self) -> pd.DataFrame: Adds coordinates to the DataFrame of
    birthplaces read from a CSV file.
    - split_coordinates(self, dataframe: pd.DataFrame) -> pd.DataFrame: Splits a string
    column in the DataFrame containing coordinate pairs into two separate columns
    for latitude and longitude.
    - run(self) -> pd.DataFrame: Executes the geocoding process, enhancing a DataFrame
    with geocoded coordinates for birthplaces.


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
        - birthplace (str): The birthplace to geocode.
        - gmaps (googlemaps.Client): The Google Maps client instance configured
        with an API key.

        Returns:
        ------
        - str | None: The coordinates of the birthplace as a string '(latitude, longitude)',
        or None if geocoding fails.
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
        - pd.DataFrame: The updated DataFrame with a new 'coordinates' column
        containing geocoded coordinates.
        """
        api_key = self.config['google_api']['api_key']
        gmaps = googlemaps.Client(key=api_key)
        self.df['Birth place coordinates'] = self.df['Birth place'].apply(
            lambda x: self._geocode_place(x, gmaps) if pd.notnull(x) else None)
        return self.df

    def split_coordinates(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Splits a string column in the DataFrame containing coordinate pairs into two
        separate columns for latitude and longitude.

        The method expects the DataFrame to have a column named 'Birth place coordinates'
        with coordinate pairs in the format '(latitude, longitude)'. It extracts these
        coordinates, splits them into two separate columns named 'birth place latitude'
        and 'birth place longitude', and converts the string representations to numeric (float)
        values. Any errors in conversion or missing values are handled gracefully,
        resulting in NaN values in the respective rows.

        Parameters:
        ------
        - dataframe (pd.DataFrame): The DataFrame containing the 'Birth place coordinates' column.

        Returns:
        ------
        - pd.DataFrame: The modified DataFrame with the original 'Birth place coordinates'
        column split into 'birth place latitude' and 'birth place longitude' columns,
        both containing numeric (float) values.

        Note:
        ------
        - The method operates on and modifies the DataFrame in-place, and also
        returns the modified DataFrame for convenience.
        - Ensure that the 'Birth place coordinates' column follows the expected
        format to avoid unexpected results.
        """
        # Extracting and splitting the values into two new columns
        self.df[['birth place latitude', 'birth place longitude']
                ] = self.df['Birth place coordinates'].str.extract(r'\(([^,]+),\s*([^)]+)\)')

        # Convert the new columns to numeric, handling errors for invalid parsing
        self.df['birth place latitude'] = pd.to_numeric(
            self.df['birth place latitude'], errors='coerce')
        self.df['birth place longitude'] = pd.to_numeric(
            self.df['birth place longitude'], errors='coerce')
        return self.df

    def run(self) -> pd.DataFrame:
        """
        Executes the geocoding process, enhancing a DataFrame with geocoded
        coordinates for birthplaces.

        This method orchestrates reading birthplace data, geocoding each
        location, and returning the enhanced DataFrame.

        Returns:
        ------
        - pd.DataFrame: The DataFrame augmented with a 'coordinates' column for geocoded birthplaces.
        """
        df = self.add_coordinates()
        return self.split_coordinates(dataframe=df)


class ColumnManager:
    """
    A class for managing columns in a DataFrame.

    Parameters:
    ------
    - dataframe (pd.DataFrame): The DataFrame to be managed.

    Attributes:
    ------
    - df (pd.DataFrame): The DataFrame being managed.
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Initializes a new instance of the ColumnManager class.

        Parameters:
        ------
        - dataframe (pd.DataFrame): The DataFrame to be managed.
        """
        self.df = dataframe

    def upper_case_columns(self) -> "ColumnManager":
        """
        Converts all column names to uppercase.

        Returns:
        ------
        - ColumnManager: The instance itself after modifying column names.
        """
        self.df.rename(columns=str.upper, inplace=True)
        return self

    def whitespace_management(self) -> "ColumnManager":
        """
        Manages whitespace in column names by replacing spaces with underscores.

        Returns:
        ------
        - ColumnManager: The instance itself after modifying column names.
        """
        self.df.columns = self.df.columns.str.strip().str.replace(' ', '_')
        return self
