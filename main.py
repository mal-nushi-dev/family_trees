import configparser
from create_coordinates import GeocodeManager
from create_database import DatabaseManager
from create_csv import FamilyEchoDownloader
from rename_file import rename_file


def run_family_echo_downloader(config):
    """
    Runs the FamilyEchoDownloader script.

    Parameters:
        config (ConfigParser): The application configuration.
    """
    usr = config['family_echo']['username']
    pswrd = config['family_echo']['password']
    url = config['family_echo']['url']
    downloader = FamilyEchoDownloader(username=usr,
                                      password=pswrd,
                                      url=url)
    downloader.run()


def run_geocode_manager(file):
    """
    Runs the GeocodeManager script and returns the DataFrame it creates.

    Returns:
        DataFrame: The DataFrame with added coordinates.
    """
    geocode_manager = GeocodeManager(file)
    coordinates_df = geocode_manager.run()
    return coordinates_df


def run_database_manager(df):
    """
    Runs the DatabaseManager script.

    Parameters:
        coordinates_df (DataFrame): The DataFrame to be stored in the db.
    """
    with DatabaseManager(db_file='family_trees.db',
                         dataframe=df) as db_manager:
        db_manager.create_table_from_dataframe()


def run_rename_files(config):
    """
    Runs the rename_files function to rename any csv files in the directory.

    Parameters:
        config (ConfigParser): The application configuration.
    """
    family_name = config['family_echo']['family_name']
    return rename_file(family_name)


def main():
    """
    The main function that runs all scripts.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')

    run_family_echo_downloader(config=config)
    csv_file = run_rename_files(config=config)
    coordinates_df = run_geocode_manager(file=csv_file)
    run_database_manager(df=coordinates_df)


if __name__ == "__main__":
    main()
