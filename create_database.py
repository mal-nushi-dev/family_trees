import sys
import sqlite3
import pandas as pd


def connect_to_sqlite3(dbFile, dataframe):
    conn = None
    try:
        conn = sqlite3.connect(dbFile)
        create_database(dataframe=dataframe, connection=conn)
    except sqlite3.Error as e:
        print(f"Failed to create a connection to sqlite3: {e}")
        sys.exit(1)
    finally:
        conn.close()


def create_database(dataframe, connection):
    dataframe.to_sql('family_tree', connection, if_exists='replace')
