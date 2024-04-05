import configparser
import sqlite3
import streamlit_app as st
import pandas as pd

# ------------------------ CONFIGURATIONS ------------------------
page_title = "NUSHI GENEALOGY"
layout = "centered"
# ----------------------------------------------------------------

st.set_page_config(
    page_title=page_title,
    layout=layout
)

# Print page title
st.title(page_title)


class DatabasePage:
    def __init__(self, database_path: str, table_name: str) -> None:
        self.database_path = database_path
        self.table_name = table_name

    def load_data(self, table_name: str) -> pd.DataFrame:
        conn = sqlite3.connect(self.database_path)
        query = f"SELECT * FROM {self.table_name};"
        db_page_df = pd.read_sql_query(sql=query, con=conn)
        return db_page_df
    
    def run(self):
        db_page_df = self.load_data(self.table_name)
        st.dataframe(db_page_df)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    family_echo_config = config['family_echo']
    database_page = DatabasePage(database_path='family_trees.db',
                                 table_name=family_echo_config['family_name'])
    database_page.run()
