import configparser
import pandas as pd
# from create_coordinates import GeocodeManager
from scripts.create_database import CreateDatabase
from scripts.create_csv import FamilyEchoDownloader
from scripts.dataframe_manager import CreateDataFrame, GeocodeManager, ColumnManager
from scripts.rename_file import rename_file


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
    """
    Runs the CreateDataFrame class to create a pandas DataFrame from a given file.

    Args:
    ------
    file_path (str): The path to the file.

    Returns:
    ------
    pd.DataFrame: The created DataFrame.
    """
    return CreateDataFrame(file=file_path).create_dataframe()


def run_column_manager(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Applies column management operations to the input dataframe.

    Args:
    ------
    dataframe (pd.DataFrame): The input dataframe to be processed.

    Returns:
    ------
    pd.DataFrame: The processed dataframe after applying column management operations.
    """
    cm = ColumnManager(
        dataframe=dataframe).upper_case_columns().whitespace_management()
    return cm.df


def run_geocode_manager(dataframe: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Processes a CSV file through GeocodeManager to add geocode coordinates.

    Parameters:
    ------
    dataframe (pd.DataFrame): DataFrame to be altered.

    Returns:
    ------
    pd.DataFrame: Enhanced DataFrame with added latitude and longitude
                  coordinates.
    """
    geocode_manager = GeocodeManager(dataframe=dataframe, column=column)
    return geocode_manager.run()


def run_create_database(database_name: str, table_name: str, dataframe: pd.DataFrame) -> None:
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

    # Donwload csv family tree file
    family_echo_config = config['family_echo']
    run_family_echo_downloader(
        username=family_echo_config['username'],
        password=family_echo_config['password'],
        url=family_echo_config['url']
    )

    # Rename csv file
    csv_file = run_rename_files(family_name=family_echo_config['family_name'])
    # Create the Pandas DataFrame
    df = run_create_dataframe(file_path=csv_file)
    # Add 'coordinates' column(s) to existing Pandas DataFrame
    df = run_geocode_manager(dataframe=df, column='Birth place')
    df = run_geocode_manager(dataframe=df, column='Address')
    df = run_geocode_manager(dataframe=df, column='Burial place')
    df = run_geocode_manager(dataframe=df, column='Death place')
    # Alter column names of existing Pandas DataFrame
    df = run_column_manager(dataframe=df)

    # Create sqlite3 database & table
    run_create_database(
        database_name=family_echo_config['database_name'],
        table_name=family_echo_config['family_name'],
        dataframe=df
    )


if __name__ == "__main__":
    main()
