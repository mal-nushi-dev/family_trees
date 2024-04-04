import sqlite3
import pandas as pd


class DatabaseManager:
    """
    Manages interactions with a SQLite database, specifically for writing
    pandas DataFrames to a specified table.

    This class simplifies the process of connecting to a SQLite database,
    writing data from a DataFrame to a table, and ensuring that the database
    connection is properly managed and closed. It is designed to be used in a
    'with' context to guarantee that resources are cleanly released after use.

    Attributes:
        database (str): File path to the SQLite database.
                        The '.db' extension is not automatically appended
                        and should be included if required.
        table (str): Name of the table where the DataFrame will be written.
        dataframe (pd.DataFrame): The pandas DataFrame to write to the db.
        connection (sqlite3.Connection, optional): Connection to the SQLite db,
                                                   set when the class is used
                                                   in a 'with' statement.

    Examples:
    ---------
    >>> df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})
    >>> with DatabaseManager('my_database.db', 'my_table', df) as db_manager:
    ...     db_manager.create_table_from_dataframe()
    """

    def __init__(self, database: str, table: str, dataframe: pd.DataFrame) -> None:
        """
        Initializes the DatabaseManager with the specified database,
        table name, and DataFrame.

        Parameters:
            database (str): Path to the SQLite database file.
                            Include the '.db' extension if needed.
            table (str): Name of the table to write the DataFrame to.
            dataframe (pd.DataFrame): DataFrame containing the data to
                                      write to the table.
        """
        self.database = database
        self.table = table
        self.dataframe = dataframe
        self.connection = None

    def connect(self) -> None:
        """
        Establishes a connection to the SQLite database specified
        during initialization.

        The connection is stored in the `connection` attribute.
        If the connection is already established, this method will do nothing.

        Raises:
            sqlite3.Error: If there is an issue connecting to the database.
        """
        self.connection = sqlite3.connect(self.database.upper() + '.db')

    def create_table_from_dataframe(self) -> None:
        """
        Writes the DataFrame to the specified table in the SQLite database.

        If the table already exists, it will be replaced. The database
        connection must be established prior to calling this method,
        typically by using the class in a 'with' statement.

        Raises:
            ValueError: If the connection has not been established.
        """
        self.dataframe.to_sql(
            self.table.upper(), self.connection, if_exists='replace')

    def __enter__(self) -> "DatabaseManager":
        """
        Establishes the database connection when entering a
        'with' statement context.

        Returns:
            self: Returns an instance of itself, allowing the class to
                  be used in a 'with' statement.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Ensures the database connection is closed when exiting a
        'with' statement context.

        If an exception occurred within the 'with' block, it prints an
        error message. Regardless of whether an exception occurred,
        it attempts to close the database connection.

        Parameters:
            exc_type, exc_val, exc_tb: Exception type, value, and
            traceback provided by the 'with' context for handling exceptions.
            Not used in this method but required by the context
            manager protocol.
        """
        if exc_type is not None:
            print(f"Failed to create a connection to sqlite3: {exc_val}")
        if self.connection:
            self.connection.close()
            self.connection = None
