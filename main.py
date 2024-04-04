import configparser
import pandas as pd
from create_coordinates import GeocodeManager
from create_database import DatabaseManager
from create_csv import FamilyEchoDownloader
from rename_file import rename_file


def run_family_echo_downloader(username: str, password: str, url: str) -> None:
    """
    Initializes and runs the FamilyEchoDownloader to download family data.

    Parameters:
        username (str): The username for FamilyEcho.
        password (str): The password for FamilyEcho.
        url (str): The target URL from where the family data is to be
                   downloaded.

    Side Effects:
        Will create and overwrite files in the current directory.
    """
    downloader = FamilyEchoDownloader(
        username=username, password=password, url=url)
    downloader.run()


def run_geocode_manager(file_path: str) -> pd.DataFrame:
    """
    Processes a CSV file through GeocodeManager to add geocode coordinates.

    Parameters:
        file_path (str): Path to the CSV file containing addresses.

    Returns:
        pd.DataFrame: Enhanced DataFrame with added latitude and longitude
                      coordinates.
    """
    geocode_manager = GeocodeManager(file=file_path)
    return geocode_manager.run()


def run_database_manager(database_name: str, table_name: str, dataframe) -> None:
    """
    Saves a DataFrame to a database using DatabaseManager.

    Parameters:
        database_name (str): Name of the SQLite database file.
        table_name (str): Name of the table within the database.
        dataframe (pd.DataFrame): DataFrame to be saved.

    Side Effects:
        Modifies the database by creating or replacing a table with the
        provided DataFrame.
    """
    with DatabaseManager(database=database_name,
                         table=table_name,
                         dataframe=dataframe) as db_manager:
        db_manager.create_table_from_dataframe()


def run_rename_files(family_name: str) -> str:
    """
    Renames CSV files in the current directory based on a provided family name.

    Parameters:
        family_name (str): Family name used to identify and rename relevant
                           CSV files.

    Returns:
        str | None: New filename if a file was renamed, otherwise None.

    Side Effects:
        May rename one or more files in the current directory.
    """
    return rename_file(family_name)


def main() -> None:
    """
    Orchestrate the execution of scripts to download, process,
    and store family data.

    Reads configuration from 'config.ini', downloads family data from
    FamilyEcho, renames the downloaded file, adds geocode coordinates to
    address data in the file, and saves the enhanced data
    into a SQLite database.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    family_echo_config = config['family_echo']
    run_family_echo_downloader(
        username=family_echo_config['username'],
        password=family_echo_config['password'],
        url=family_echo_config['url']
    )

    csv_file = run_rename_files(family_name=family_echo_config['family_name'])
    coordinates_df = run_geocode_manager(file_path=csv_file)
    run_database_manager(
        database_name=family_echo_config['database_name'],
        table_name=family_echo_config['family_name'],
        dataframe=coordinates_df
    )


if __name__ == "__main__":
    main()
