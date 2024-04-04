import configparser
from create_coordinates import GeocodeManager
from create_database import DatabaseManager
from create_csv import FamilyEchoDownloader


def run_family_echo_downloader(config):
    """
    Runs the FamilyEchoDownloader script.

    Parameters:
        config (ConfigParser): The application configuration.
    """
    usr = config['family_echo']['username']
    pswrd = config['family_echo']['password']
    downloader = FamilyEchoDownloader(username=usr,
                                      password=pswrd)
    downloader.run()


def run_geocode_manager():
    """
    Runs the GeocodeManager script and returns the DataFrame it creates.

    Returns:
        DataFrame: The DataFrame with added coordinates.
    """
    geocode_manager = GeocodeManager()
    coordinates_df = geocode_manager.run()
    return coordinates_df


def run_database_manager(df):
    """
    Runs the DatabaseManager script.

    Parameters:
        coordinates_df (DataFrame): The DataFrame to be stored in the database.
    """
    with DatabaseManager(db_file='data/sqlite3/database.db',
                         dataframe=df) as db_manager:
        db_manager.create_table_from_dataframe()


def main():
    """
    The main function that runs all scripts.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    run_family_echo_downloader(config=config)
    coordinates_df = run_geocode_manager()
    run_database_manager(coordinates_df)


if __name__ == "__main__":
    main()
