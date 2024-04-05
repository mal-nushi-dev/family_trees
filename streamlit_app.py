from streamlit_filter_dataframe import filtered_df
import configparser
import sqlite3
import streamlit as st
import pandas as pd

# Set page configurations
st.set_page_config(
    layout="centered"
)


class DatabasePage:
    def __init__(self, database_path: str, table_name: str) -> None:
        self.database_path = database_path
        self.table_name = table_name

    # Load data from the database
    def load_data(self) -> pd.DataFrame:
        conn = sqlite3.connect(self.database_path)
        query = f"SELECT * FROM {self.table_name};"
        db_page_df = pd.read_sql_query(sql=query, con=conn)
        df_filter = filtered_df(db_page_df)
        db = df_filter.filter_dataframe()
        return db

    # Display the data on the Streamlit page
    def run(self):
        db_page_df = self.load_data()
        st.dataframe(db_page_df)


def main():
    # Read configurations from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    family_echo_config = config['family_echo']
    table_name = family_echo_config['family_name'].upper()

    # Print page title
    st.title(f"{table_name} GENEALOGY")

    # Create a DatabasePage object and run it
    database_page = DatabasePage(database_path='family_trees.db',
                                 table_name=table_name)
    database_page.run()


if __name__ == "__main__":
    main()
