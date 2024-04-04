import sqlite3
import pandas as pd


class DatabaseManager:
    def __init__(self, db_file: str, dataframe: pd.DataFrame):
        self.db_file = db_file
        self.dataframe = dataframe
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_file)

    def create_table_from_dataframe(self):
        self.dataframe.to_sql(
            'family_tree', self.connection, if_exists='replace')

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Failed to create a connection to sqlite3: {exc_val}")
        if self.connection:
            self.connection.close()
