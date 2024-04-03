import sys
import sqlite3


def connect_to_sqlite3(db_file, dataframe):
    """
    Connects to a SQLite3 database and creates a table.

    Parameters:
    db_file (str): The database file to connect to.
    dataframe (pandas.DataFrame): The dataframe to convert into a SQL table.

    Raises:
    sqlite3.Error: If a connection error occurs.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        create_table(dataframe=dataframe, connection=conn)
    except sqlite3.Error as e:
        print(f"Failed to create a connection to sqlite3: {e}")
        raise
    finally:
        conn.close()


def create_table(dataframe, connection):
    """
    Creates a table in the SQLite3 database from a pandas DataFrame.

    Parameters:
    dataframe (pandas.DataFrame): The dataframe to convert into a SQL table.
    connection (sqlite3.Connection): The connection to the SQLite3 database.
    """
    dataframe.to_sql('family_tree', connection, if_exists='replace')
