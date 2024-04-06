import sqlite3
import streamlit as st
import pandas as pd
import numpy as np


class CreateMap:
    def __init__(self, database: str, column: str) -> None:
        self.database = database
        self.lat_column = f'{column}_LATITUDE'
        self.long_column = f'{column}_LONGITUDE'

    def query_generator(self):
        query = f'''
            SELECT
                FULL_NAME,
                {self.lat_column},
                {self.long_column}
            FROM NUSHI
            WHERE {self.lat_column} IS NOT NULL
            AND {self.long_column} IS NOT NULL;
        '''
        return query

    def create_dataframe(self, query: str, database_connection: sqlite3.connect) -> pd.DataFrame:
        df = pd.read_sql_query(sql=query, con=database_connection)
        return df

    def scatter_plots(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        noise_scale = 0.001  # Adjust this value as needed

        # Make the column inputs in all caps
        self.lat_column = self.lat_column.upper()
        self.long_column = self.long_column.upper()

        dataframe[self.lat_column] += np.random.normal(
            0, noise_scale, size=len(dataframe))
        dataframe[self.long_column] += np.random.normal(
            0, noise_scale, size=len(dataframe))
        return dataframe

    def map_data(self, database: pd.DataFrame):
        st.map(data=database,
               latitude=self.lat_column,
               longitude=self.long_column,
               size=10)

    def __run__(self):
        query = self.query_generator()
        df = self.create_dataframe(query=query, database_connection=self.conn)
        df = self.scatter_plots(dataframe=df)
        self.map_data(database=df)

    def __enter__(self):
        self.conn = sqlite3.connect(self.database)
        return self

    def __exit__(self, exc_type, exc_val, ecx_tb):
        self.conn.close()


if __name__ == "__main__":
    pass
