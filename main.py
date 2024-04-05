import configparser
import pandas as pd
# from create_coordinates import GeocodeManager
from create_database import CreateDatabase
from create_csv import FamilyEchoDownloader
from dataframe_manager import CreateDataFrame, GeocodeManager, ColumnManager
from rename_file import rename_file


def run_family_echo_downloader(username: str, password: str, url: str) -> None:
    """
    Initializes and runs the FamilyEchoDownloader to download family data.

    Parameters:
    ------
    username (str): The username for FamilyEcho.
    password (str): The password for FamilyEcho.
    url (str): The target URL from where the family data is to be
               downloaded.

    Side Effects:
    ------
    Will create and overwrite files in the current directory.
    """
    downloader = FamilyEchoDownloader(
        username=username, password=password, url=url)
    downloader.run()


def run_create_dataframe(file_path: str) -> pd.DataFrame:
    return CreateDataFrame(file=file_path).create_dataframe()


def run_column_manager(dataframe: pd.DataFrame) -> pd.DataFrame:
    cm = ColumnManager(dataframe=dataframe).upper_case_columns().whitespace_management()
    return cm.df


def run_geocode_manager(file_path: str) -> pd.DataFrame:
    """
    Processes a CSV file through GeocodeManager to add geocode coordinates.

    Parameters:
    ------
    file_path (str): Path to the CSV file containing addresses.

    Returns:
    ------
    pd.DataFrame: Enhanced DataFrame with added latitude and longitude
                  coordinates.
    """
    geocode_manager = GeocodeManager(file=file_path)
    return geocode_manager.run()


def run_database_manager(database_name: str, table_name: str, dataframe) -> None:
    """
    Saves a DataFrame to a database using DatabaseManager.

    Parameters:
    ------
    database_name (str): Name of the SQLite database file.
    table_name (str): Name of the table within the database.
    dataframe (pd.DataFrame): DataFrame to be saved.

    Side Effects:
    ------
    Modifies the database by creating or replacing a table with the
    provided DataFrame.
    """
    with CreateDatabase(database=database_name,
                        table=table_name,
                        dataframe=dataframe) as create_db:
        create_db.create_table_from_dataframe()


def run_rename_files(family_name: str) -> str:
    """
    Renames CSV files in the current directory based on a provided family name.

    Parameters:
    ------
    family_name (str): Family name used to identify and rename relevant CSV files.

    Returns:
    ------
    str | None: New filename if a file was renamed, otherwise None.

    Side Effects:
    ------
    May rename one or more files in the current directory.
    """
    return rename_file(family_name)


def main() -> None:
    config = configparser.ConfigParser()
    config.read('config.ini')

    family_echo_config = config['family_echo']
    run_family_echo_downloader(
        username=family_echo_config['username'],
        password=family_echo_config['password'],
        url=family_echo_config['url']
    )

    csv_file = run_rename_files(family_name=family_echo_config['family_name'])
    # coordinates_df = run_geocode_manager(file_path=csv_file)
    # Create the Pandas DataFrame
    df = run_create_dataframe(file_path=csv_file)
    # Alter column names
    df = run_column_manager(dataframe=df)

    run_database_manager(
        database_name=family_echo_config['database_name'],
        table_name=family_echo_config['family_name'],
        dataframe=df
    )


if __name__ == "__main__":
    main()
