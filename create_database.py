import sqlite3
import pandas as pd


class DatabaseManager:
    """
    A class used to manage a SQLite database.

    ...

    Attributes
    ----------
    db_file : str
        a formatted string to print out the database file path
    dataframe : pd.DataFrame
        the pandas DataFrame to be written to the SQLite database
    connection : sqlite3.Connection
        the SQLite database connection

    Methods
    -------
    connect():
        Connects to the SQLite database.
    create_table_from_dataframe():
        Writes the DataFrame to the SQLite database.
    """
    def __init__(self, db_file: str, dataframe: pd.DataFrame):
        """
        Constructs all the necessary attributes for the DatabaseManager object.

        Parameters
        ----------
            db_file : str
                the database file path
            dataframe : pd.DataFrame
                the pandas DataFrame to be written to the SQLite database
        """
        self.db_file = db_file
        self.dataframe = dataframe
        self.connection = None

    def connect(self):
        """Connects to the SQLite database."""
        self.connection = sqlite3.connect(self.db_file)

    def create_table_from_dataframe(self):
        """
        Writes the DataFrame to the SQLite database, replacing the
            existing table if it exists.
        """
        self.dataframe.to_sql(
            'family_tree', self.connection, if_exists='replace')

    def __enter__(self):
        """
        Makes DatabaseManager usable with 'with' statement
            and connects to the database.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the connection to the database and handles any exceptions
            that occurred while the 'with' block was running.
        """
        if exc_type is not None:
            print(f"Failed to create a connection to sqlite3: {exc_val}")
        if self.connection:
            self.connection.close()
